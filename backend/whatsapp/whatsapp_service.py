import requests
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    """
    WhatsApp Business API service for sending messages automatically
    """
    
    def __init__(self):
        # You can use different WhatsApp services:
        # 1. WhatsApp Business API (official)
        # 2. Twilio WhatsApp API
        # 3. MessageBird WhatsApp API
        # 4. Other third-party services
        
        # For this example, I'll use a generic approach that can be adapted
        self.api_url = getattr(settings, 'WHATSAPP_API_URL', 'https://api.whatsapp.com/send')
        self.api_token = getattr(settings, 'WHATSAPP_API_TOKEN', None)
        self.phone_number_id = getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', None)
        self.mock_mode = getattr(settings, 'WHATSAPP_MOCK_MODE', True)
        
    def send_message(self, to_phone: str, message: str) -> dict:
        """
        Send WhatsApp message automatically
        
        Args:
            to_phone (str): Recipient phone number (with country code)
            message (str): Message content
            
        Returns:
            dict: Response from WhatsApp API
        """
        try:
            # Clean and format phone number
            clean_phone = self._format_phone_number(to_phone)
            
            # Mock mode for development/testing
            if self.mock_mode:
                return self._send_via_mock(clean_phone, message)
            
            # For demonstration, I'll show how to implement with different services
            # You can choose one based on your needs:
            
            # Option 1: WhatsApp Business API (Official)
            return self._send_via_whatsapp_business_api(clean_phone, message)
            
            # Option 2: Twilio WhatsApp API
            # return self._send_via_twilio(clean_phone, message)
            
            # Option 3: MessageBird WhatsApp API
            # return self._send_via_messagebird(clean_phone, message)
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to send WhatsApp message'
            }
    
    def _format_phone_number(self, phone: str) -> str:
        """Format phone number for WhatsApp API"""
        # Remove all non-digit characters except +
        clean_phone = ''.join(filter(lambda x: x.isdigit() or x == '+', phone))
        
        # If no country code, assume US (+1)
        if not clean_phone.startswith('+'):
            clean_phone = '+1' + clean_phone.lstrip('0')
        
        # Remove + for API calls (some APIs don't need it)
        return clean_phone.replace('+', '')
    
    def _send_via_mock(self, phone: str, message: str) -> dict:
        """
        Mock WhatsApp sending for development/testing
        """
        logger.info(f"MOCK: WhatsApp message would be sent to {phone}")
        logger.info(f"MOCK: Message content: {message}")
        
        return {
            'success': True,
            'message_id': f'mock_{phone}_{hash(message)}',
            'message': 'WhatsApp message sent successfully (MOCK MODE)'
        }
    
    def _send_via_whatsapp_business_api(self, phone: str, message: str) -> dict:
        """
        Send message via WhatsApp Business API (Official)
        Requires WhatsApp Business API access
        """
        if not self.api_token or not self.phone_number_id:
            return {
                'success': False,
                'error': 'WhatsApp API credentials not configured',
                'message': 'Please configure WhatsApp Business API credentials'
            }
        
        url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            return {
                'success': True,
                'message_id': response.json().get('messages', [{}])[0].get('id'),
                'message': 'WhatsApp message sent successfully'
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"WhatsApp Business API error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to send WhatsApp message via Business API'
            }
    
    def _send_via_twilio(self, phone: str, message: str) -> dict:
        """
        Send message via Twilio WhatsApp API
        Requires Twilio account and WhatsApp sandbox
        """
        from twilio.rest import Client
        
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        whatsapp_from = getattr(settings, 'TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
        
        if not all([account_sid, auth_token]):
            return {
                'success': False,
                'error': 'Twilio credentials not configured',
                'message': 'Please configure Twilio credentials'
            }
        
        try:
            client = Client(account_sid, auth_token)
            
            message_obj = client.messages.create(
                body=message,
                from_=whatsapp_from,
                to=f'whatsapp:+{phone}'
            )
            
            return {
                'success': True,
                'message_id': message_obj.sid,
                'message': 'WhatsApp message sent successfully via Twilio'
            }
            
        except Exception as e:
            logger.error(f"Twilio WhatsApp error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to send WhatsApp message via Twilio'
            }
    
    def _send_via_messagebird(self, phone: str, message: str) -> dict:
        """
        Send message via MessageBird WhatsApp API
        """
        api_key = getattr(settings, 'MESSAGEBIRD_API_KEY', None)
        
        if not api_key:
            return {
                'success': False,
                'error': 'MessageBird API key not configured',
                'message': 'Please configure MessageBird API key'
            }
        
        url = "https://conversations.messagebird.com/v1/send"
        
        headers = {
            'Authorization': f'AccessKey {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "to": f"+{phone}",
            "type": "whatsapp",
            "content": {
                "text": message
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            return {
                'success': True,
                'message_id': response.json().get('id'),
                'message': 'WhatsApp message sent successfully via MessageBird'
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"MessageBird WhatsApp error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to send WhatsApp message via MessageBird'
            }
    
    def send_wish_message(self, customer_name: str, phone: str, special_date_type: str, 
                         custom_message: str = '', offer_details: str = '') -> dict:
        """
        Send a formatted wish message
        
        Args:
            customer_name (str): Customer's name
            phone (str): Customer's phone number
            special_date_type (str): Type of special date (Birthday, Anniversary, etc.)
            custom_message (str): Custom message from user
            offer_details (str): Special offer details
            
        Returns:
            dict: Response from WhatsApp API
        """
        # Format the wish message
        message = f"🎉 Happy {special_date_type}!\n\n"
        message += f"Dear {customer_name},\n\n"
        message += "We're thinking of you on your special day and wanted to send our warmest wishes!\n\n"
        
        if offer_details:
            message += f"🎁 {offer_details}\n\n"
        
        if custom_message:
            message += f"💝 {custom_message}\n\n"
        
        message += "Best wishes from your friends at [Hotel Name]! 🏨\n\n"
        message += "Thank you for being a valued customer! 🙏"
        
        return self.send_message(phone, message)
