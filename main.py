import asyncio
import json
import telethon
from telethon import TelegramClient


def load_config(path='config.ini'):
    from configparser import ConfigParser
    config = ConfigParser()
    config.read(path)

    return int(config['TELEGRAM']['api_id']), str(config['TELEGRAM']['api_hash']) 

 
async def save_user_dialogs(client, dialogs_list):
    dialogs = {}
    for dialog in dialogs_list:
        dialogs.update({dialog.name : dialog.entity.id})

    with open('dialogs_names.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(dialogs, ensure_ascii=False))


async def main():
    api_id, api_hash = load_config('config.ini')
    #Log in Telegram
    client = TelegramClient("Test", api_id, api_hash) 
    # Start Telegram client
    await client.start()  
    #try:
    with open('dialogs_names.json', encoding="utf8") as file:
        chosed_dialogs = json.load(file)
    await parse_data(client, chosed_dialogs)
    #except Exception as ex:
        #Get all dialogs
        #Saving name of each dialog to jsoncle
        #In json you can leave those channels whose data we need
    #dialogs_list = await client.get_dialogs() 
        #await save_user_dialogs(client, dialogs_list)
    

async def parse_data(client, chosed_dialogs):
    print('Parsing')
    data = {}
    await client.get_dialogs() 
    for id in chosed_dialogs.values():
        messages = []
        async for message in client.iter_messages(id):
            if message.media is None:
                messages.append(message.text)
            elif message.file is not None:
                await client.download_media(message = message.media, file=f"Media\\{id}\\{str(message.file.name)}")
        
                
        data.update({id : messages})

    print('All is done')
    with open("data.json", 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())