# commands.py

import requests
import random
import string
import time
from telegram import Update
from telegram.ext import CallbackContext

# Define the games and their respective details
games = {
    1: {
        'name': 'Riding Extreme 3D',
        'appToken': 'd28721be-fd2d-4b45-869e-9f253b554e50',
        'promoId': '43e35910-c168-4634-ad4f-52fd764a843f',
    },
    2: {
        'name': 'Chain Cube 2048',
        'appToken': 'd1690a07-3780-4068-810f-9f5bbf2931b2',
        'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3',
    },
    3: {
        'name': 'My Clone Army',
        'appToken': '74ee0b5b-775e-4bee-974f-63e7f4d5bacb',
        'promoId': 'fe693b26-b342-4159-8808-15e3ff7f8767',
    },
    4: {
        'name': 'Train Miner',
        'appToken': '82647f43-3f87-402d-88dd-09a90025313f',
        'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954',
    }
}

# Function to generate a client ID
def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join(random.choices(string.digits, k=19))
    return f'{timestamp}-{random_numbers}'

# Function to log in and get a client token
def login(client_id, app_token):
    response = requests.post('https://api.gamepromo.io/promo/login-client', json={
        'appToken': app_token,
        'clientId': client_id,
        'clientOrigin': 'deviceid'
    })
    response.raise_for_status()
    return response.json()['clientToken']

# Function to emulate progress
def emulate_progress(client_token, promo_id):
    response = requests.post('https://api.gamepromo.io/promo/register-event', headers={
        'Authorization': f'Bearer {client_token}',
        'Content-Type': 'application/json'
    }, json={
        'promoId': promo_id,
        'eventId': generate_uuid(),
        'eventOrigin': 'undefined'
    })
    return response.status_code == 200 and response.json().get('hasCode', False)

# Function to generate the promo code
def generate_key(client_token, promo_id):
    response = requests.post('https://api.gamepromo.io/promo/create-code', headers={
        'Authorization': f'Bearer {client_token}',
        'Content-Type': 'application/json'
    }, json={'promoId': promo_id})
    response.raise_for_status()
    return response.json()['promoCode']

# Generate a UUID
def generate_uuid():
    return ''.join([random.choice('0123456789abcdef') for _ in range(8)]) + '-' + \
           ''.join([random.choice('0123456789abcdef') for _ in range(4)]) + '-4' + \
           ''.join([random.choice('0123456789abcdef') for _ in range(3)]) + '-' + \
           ''.join([random.choice('89ab')]) + \
           ''.join([random.choice('0123456789abcdef') for _ in range(3)]) + '-' + \
           ''.join([random.choice('0123456789abcdef') for _ in range(12)])

# Handle the /generate command
def generate(update: Update, context: CallbackContext):
    game_choice = int(context.args[0])
    key_count = int(context.args[1])
    game = games[game_choice]

    keys = []
    for _ in range(key_count):
        client_id = generate_client_id()
        client_token = login(client_id, game['appToken'])
        for _ in range(11):
            time.sleep(random.uniform(20, 26))
            if emulate_progress(client_token, game['promoId']):
                break
        keys.append(generate_key(client_token, game['promoId']))

    update.message.reply_text('\n'.join(keys))
