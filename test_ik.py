import requests, os, json
from dotenv import load_dotenv
load_dotenv()
token = os.environ.get('INDIANKANOON_API_TOKEN')
headers = {'Authorization': f'Token {token}'}

# fetch full doc
tid = 31012763
doc_r = requests.post(f'https://api.indiankanoon.org/doc/{tid}/', headers=headers)
print('Doc status:', doc_r.status_code)
data = doc_r.json()
print('Doc keys:', data.keys())
print('Doc text preview:', str(data.get('doc', ''))[:500])