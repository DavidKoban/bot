import time
from telethon import TelegramClient, events

api_id = '24701494'
api_hash = '1cf4dd02bae31aff2769980f8576d17f'

client = TelegramClient('session', api_id, api_hash)
client.start()


@client.on(events.NewMessage(-1001720393795))
async def main(event):
    await client.forward_messages(-1001749214990, event.message, drop_author=True)

while True:
    try:
        client.run_until_disconnected()
    except Exception as e:
            print(e, 'error')
            time.sleep(5)
            continue