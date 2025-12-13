import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frontend.settings')
django.setup()

from django.test import Client

client = Client()

url = '/staff-admin/settings/'

print('GET', url)
resp = client.get(url)
print('Status code:', resp.status_code)
content_snippet = resp.content.decode('utf-8')[:400]
print('Content snippet:', content_snippet.replace('\n',' ')[:300])

print('\nPOSTing new settings...')
data = {
    'booking_auto_confirm': 'on',
    # leave notify_on_pending unchecked to test false
    'currency': 'EUR',
    'occupancy_alert_threshold': '50',
    'items_per_page': '5'
}

post_resp = client.post(url, data)
print('POST status:', post_resp.status_code)

# Check settings file written by the view
expected_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'admin_settings.json')
print('Expect settings file at:', expected_path)

if os.path.exists(expected_path):
    try:
        with open(expected_path, 'r', encoding='utf-8') as fh:
            loaded = json.load(fh)
        print('Saved JSON:', json.dumps(loaded, indent=2))
    except Exception as e:
        print('Error reading JSON file:', e)
else:
    print('Settings file not found.')
