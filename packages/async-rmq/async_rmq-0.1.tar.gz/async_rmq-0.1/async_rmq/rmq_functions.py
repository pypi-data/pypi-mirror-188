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
                                  dead_queue_exchange: Optional[str] = None) -> Queue:
    if dead_queue_exchange:
        # auto reroute nacked messages to DLX
        default_queue_params["arguments"]["x-dead-letter-exchange"] = dead_queue_exchange
    queue = await channel.declare_queue(
        queue_name,
        **default_queue_params
    )
    await channel.declare_exchange(exchange_name, exchange_type, **default_exchange_params)
    await queue.bind(exchange_name, binding)

    return queue


# Create dead letter queue
async def _prepare_dead_letter_queue(channel: Channel, dead_letter_exchange: str, bindings: list) -> Queue:
    dead_letter_queue: Queue = await channel.declare_queue(
        rmq_config.RABBITMQ_DEAD_LETTER_QUEUE,
        # **default_queue_params
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
                       binding: str,
                       default_queue_params: dict,
                       default_exchange_params: dict) -> None:
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
            queue = await _prepare_consumed_queue(channel,
                                                  queue_name,
                                                  exchange_name,
                                                  exchange_type,
                                                  binding,
                                                  default_queue_params,
                                                  default_exchange_params)
            consumer = consumer_class(
                queue=queue
            )
            await consumer.consume()

    finally:
        await rabbitmq_connection.close()
