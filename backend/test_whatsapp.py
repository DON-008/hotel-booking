import requests
import json

# Test WhatsApp API endpoint
url = 'http://localhost:8000/api/whatsapp/send-wish/'
data = {
    'customer_name': 'Test User',
    'phone': '+1234567890',
    'special_date_type': 'Birthday',
    'custom_message': 'Test message'
}

try:
    response = requests.post(url, json=data)
    print('WhatsApp API Response:')
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f'Error: {e}')
