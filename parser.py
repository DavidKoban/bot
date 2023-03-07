import time
from telethon import TelegramClient, events

api_id = '24701494'
api_hash = '1cf4dd02bae31aff2769980f8576d17f'

client = TelegramClient('session', api_id, api_hash)
client.start()


@client.on(events.NewMessage(-1001720393795))
async def main(event):
    print(event)
    await client.send_message(-1001761229044, event.meessage)


@client.on(events.NewMessage(-1001394521081))
async def main(event):
    print(event)
    await client.send_message(-1001854214387, event.message)


@client.on(events.NewMessage(-1001455185560))
async def main(event):
    print(event)
    await client.send_message(-1001668289354, event.message)


@client.on(events.NewMessage(-1001638369964))
async def main(event):
    print(event)
    await client.send_message(-1001878712248, event.message)

while True:
    try:
        client.run_until_disconnected()
    except Exception as e:
            print(e, 'error')
            time.sleep(5)
            continue