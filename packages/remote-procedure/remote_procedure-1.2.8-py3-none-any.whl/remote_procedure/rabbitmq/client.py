import asyncio  # noqa
import logging
from asyncio import AbstractEventLoop
from typing import (
    MutableMapping,
    Union,
)

from aio_pika import (
    Channel,
    Message,
)
from aio_pika.abc import (
    AbstractIncomingMessage,
    TimeoutType,
)
from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import ChannelClosedByBroker

from remote_procedure.rabbitmq.base import (
    AsyncConnector,
    Connector,
    MessageConverter,
    get_correlation_id,
)
from remote_procedure.rabbitmq.error import ChannelClosedByBrokerError
from remote_procedure.rabbitmq.pool import (
    PoolCtx,
    PoolProtocol,
)
from remote_procedure.rabbitmq.protocols import (
    RPCAsyncClientProtocol,
    RPCSyncClientProtocol,
)

LOGGER = logging.getLogger(__name__)


class RPCAsyncClient(RPCAsyncClientProtocol, AsyncConnector, MessageConverter):

    def __init__(self, *args, **kwargs):
        self.loop: Union[AbstractEventLoop, None] = None
        self.futures: MutableMapping[str, asyncio.Future] = {}
        super().__init__(*args, **kwargs)

    def on_response(self, message: AbstractIncomingMessage) -> None:
        if message.correlation_id is None:
            LOGGER.info(f"Bad message {message!r}")
            return
        future: asyncio.Future = self.futures.pop(message.correlation_id)
        resp: dict = self.convert_message_to_dict(message=message.body)
        future.set_result(resp)

    async def rpc_call(
            self,
            body: dict,
            queue_name,
            timeout: TimeoutType,
            expiration: bool = True,
    ):
        """https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/6-rpc.html#"""
        async with self.channel_pool.acquire() as channel:  # type: Channel
            result = await channel.declare_queue(exclusive=True)
            await result.consume(self.on_response)

            correlation_id = get_correlation_id()
            future = self.loop.create_future()
            self.futures[correlation_id] = future

            expiration: str | None = (expiration and timeout) or None

            body = self.convert_dict_to_bytes(obj=body)

            await channel.default_exchange.publish(
                message=Message(
                    body=body,
                    content_type='application/json',
                    correlation_id=correlation_id,
                    reply_to=result.name,
                    expiration=expiration,
                ),
                routing_key=queue_name,
                timeout=timeout,
            )
            try:
                return await asyncio.wait_for(future, timeout)
            except asyncio.TimeoutError:
                return None


class RPCSyncClient(RPCSyncClientProtocol, Connector, MessageConverter):

    def __init__(self, *args, max_size: int = 5, **kwargs):
        super().__init__(*args, **kwargs)
        self.correlation_id_data: dict = {}
        self.response: Union[dict, None] = None
        self.channel_pool: PoolProtocol = PoolCtx(
            self.open_channel, max_size=max_size,
        )

    def on_response(self, ch: BlockingChannel, method, props, body):
        if self.correlation_id_data.pop(props.correlation_id, None):
            self.response = self.convert_message_to_dict(body)
            ch.stop_consuming()

    def consume(self, queue, channel: BlockingChannel):
        try:
            channel.basic_consume(
                queue=queue, on_message_callback=self.on_response,
                auto_ack=True,
            )
        except ChannelClosedByBroker as exc:
            raise ChannelClosedByBrokerError(exc)

    def rpc_call(
            self,
            routing_key,
            body: dict,
            timeout: TimeoutType,
            expiration: bool = True,
    ):
        """https://www.rabbitmq.com/tutorials/tutorial-six-python.html"""
        with self.channel_pool as channel:  # type: BlockingChannel
            self.consume(queue=self.callback_queue, channel=channel)

            correlation_id = get_correlation_id()
            self.correlation_id_data[correlation_id] = correlation_id

            expiration: str | None = (expiration and str(timeout)) or None

            body = self.convert_dict_to_bytes(obj=body)

            channel.basic_publish(
                exchange=self._exchange,
                routing_key=routing_key,
                body=body,
                properties=BasicProperties(
                    content_type='application/json',
                    reply_to=self.callback_queue,
                    correlation_id=correlation_id,
                    expiration=expiration,
                ),
            )
            self._connection.process_data_events(time_limit=timeout)
            return self.response
