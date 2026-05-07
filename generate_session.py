from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv

load_dotenv()

try:
    api_id = int(os.getenv('API_ID'))
except (TypeError, ValueError):
    api_id = None
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE')

if not api_id or not api_hash or not phone:
    print('Missing API_ID, API_HASH, or PHONE in .env')
    print('Please add them to .env (see the repository root .env) and re-run')
    raise SystemExit(1)

print('Using PHONE:', phone)
print('Starting Telegram login flow. You will be prompted for the code sent to the phone number.')

with TelegramClient(StringSession(), api_id, api_hash) as client:
    client.start(phone=phone)
    session_string = client.session.save()
    print('\nSESSION_STRING=' + session_string)
    # Optionally write to file
    out_path = '.session_string'
    with open(out_path, 'w') as f:
        f.write(session_string)
    print(f'Also saved session string to {out_path}')

print('Done.')
