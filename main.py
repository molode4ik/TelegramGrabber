import asyncio
import json
import os
import sys
from telethon import TelegramClient


def load_config(path='config.ini'):
    from configparser import ConfigParser
    config = ConfigParser()
    config.read(path)

    return int(config['TELEGRAM']['api_id']), str(config['TELEGRAM']['api_hash']) 

#Get all dialogs
#Saving name of each dialog to json
async def save_user_dialogs(dialogs_list):
    dialogs = {}
    for dialog in dialogs_list:
        if dialog.name != "":
            dialogs.update({dialog.entity.id : dialog.name})
        else:
            dialogs.update({dialog.entity.id : dialog.entity.id})

    with open('dialogs_names.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(dialogs, ensure_ascii=False))
#In json you can leave those channels whose data we need


async def main(path):
    try:
        api_id, api_hash = load_config('config.ini')
    except:
        print('You dont have a config file\nCreate it before working')
    #Log in Telegram
    client = TelegramClient("Telegram", api_id, api_hash) 
    # Start Telegram client
    await client.start()  
    try:
        with open('dialogs_names.json', encoding="utf8") as file:
            chosed_dialogs = json.load(file)
    except:
        print('You havent a dialogs list \n'
        'This file will create now\n'
        'Check this and remove extra dialogs')
        dialogs_list = await client.get_dialogs()
        await save_user_dialogs(dialogs_list)   
    
    await parse_data(client, chosed_dialogs, path)
    
        
   
#Parcing data from chosed dialogs
#Save messages and media to folder of channel
async def parse_data(client, chosed_dialogs, path):
    print('Parsing')
    await client.get_dialogs() 
    for id in chosed_dialogs.keys():
        data = {}
        os.makedirs(f"{path}Media\\{chosed_dialogs.get(id)}\\", mode=0o777)
        async for message in client.iter_messages(int(id)):
            if message.media is None:
                data.update({str(message.date).split('+')[0] : message.text})
            elif message.file is not None:
                await client.download_media(message = message.media, file=f"{path}Media\\{chosed_dialogs.get(id)}\\{(str(message.date).split('+')[0]).replace(':', '-')} {str(message.file.name)}")
        
        save_data = {v: k for k, v in data.items()}
        with open(f"{path}Media\\{chosed_dialogs.get(id)}\\messages.json", 'w', encoding='utf-8') as file:
            file.write(json.dumps(save_data, ensure_ascii=False))

    print('All is done')
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('You didnt set the path to saved files')
        sys.exit()
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(path=sys.argv[1]))