import asyncio
import json
import asyncio_redis
import aiosmtplib


async def publish():
    connection = await asyncio_redis.Connection.create()
    subscriber = await connection.start_subscribe()
    await subscriber.subscribe(['registration_email_channel'])

    while True:
        reply = await subscriber.next_published()
        await send_email(reply)
        print('Received: ', repr(reply.value), 'on channel', reply.channel)

    connection.close()

async def send_email(reply):

    smtp = aiosmtplib.SMTP(hostname='localhost', port=25, loop=loop)
    sender = 'sender'
    try:
        data = json.loads(reply.value)
        await smtp.sendmail(sender, [data.get('email')], data.get('message'))
    except AttributeError as e:
        print(e)


loop = asyncio.get_event_loop()

loop.run_until_complete(publish())
