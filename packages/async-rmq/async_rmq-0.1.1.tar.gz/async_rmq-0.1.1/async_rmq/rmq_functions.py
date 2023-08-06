import asyncio
import aio_pika
from typing import Optional
from aio_pika import Channel, Queue, ExchangeType
import constants.rmq_config as rmq_config
from .abstract_rmq_consumer import RabbitMQConsumer


# Create a consumed queue
async def _prepare_consumed_queue(channel: Channel,
                                  queue_name: str,
                                  exchange_name: str,
                                  exchange_type: ExchangeType,
                                  binding: str,
                                  default_queue_params: dict,
                                  default_exchange_params: dict,
                                  dead_letter_enabled: Optional[bool] = False,
                                  dead_letter_exchange: Optional[str] = None) -> Queue:
    if dead_letter_enabled:
        # auto reroute nacked messages to DLX
        default_queue_params["arguments"]["x-dead-letter-exchange"] = dead_letter_exchange
    queue = await channel.declare_queue(
        queue_name,
        **default_queue_params
    )
    await channel.declare_exchange(exchange_name, exchange_type, **default_exchange_params)
    await queue.bind(exchange_name, binding)

    return queue


# Create dead letter queue
async def _prepare_dead_letter_queue(channel: Channel,
                                     dead_letter_queue_name: str,
                                     dead_letter_exchange: str,
                                     default_queue_params: dict,
                                     bindings: Optional[list] = []) -> Queue:
    dead_letter_queue: Queue = await channel.declare_queue(
        dead_letter_queue_name,
        **default_queue_params
    )
    await channel.declare_exchange(dead_letter_exchange, ExchangeType.TOPIC)

    for routing_key in bindings:
        await dead_letter_queue.bind(dead_letter_exchange, routing_key)

    return dead_letter_queue


# Running a consumer
async def run_consumer(credentials: dict,
                       consumer_class: RabbitMQConsumer,
                       queue_name: str,
                       exchange_name: str,
                       exchange_type: ExchangeType,
                       bindings: str,
                       default_queue_params: dict,
                       default_exchange_params: dict,
                       dead_letter_enabled: Optional[bool] = False,
                       dead_letter_queue_name: Optional[str] = None,
                       dead_letter_exchange: Optional[str] = None,
                       dead_letter_bindings: Optional[list] = []) -> None:
    loop = asyncio.get_event_loop()

    rabbitmq_connection = await aio_pika.connect_robust(
        loop=loop,
        host=credentials["host"],
        port=credentials["port"],
        login=credentials["login"],
        password=credentials["password"],
        virtualhost=credentials["vhost"]
    )
    try:

        async with rabbitmq_connection.channel() as channel:
            await channel.set_qos(prefetch_count=1)
            if dead_letter_enabled:
                dead_letter_queue = await _prepare_dead_letter_queue(channel,
                                                                     dead_letter_queue_name,
                                                                     dead_letter_exchange,
                                                                     default_queue_params,
                                                                     dead_letter_bindings)
            queue = await _prepare_consumed_queue(channel,
                                                  queue_name,
                                                  exchange_name,
                                                  exchange_type,
                                                  bindings,
                                                  default_queue_params,
                                                  default_exchange_params,
                                                  dead_letter_enabled,
                                                  dead_letter_exchange)
            consumer = consumer_class(
                queue=queue
            )
            await consumer.consume()

    finally:
        await rabbitmq_connection.close()