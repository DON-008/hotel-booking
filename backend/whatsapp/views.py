from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import logging
from .whatsapp_service import WhatsAppService

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_whatsapp_wish(request):
    """
    Send WhatsApp wish message automatically
    
    Expected payload:
    {
        "customer_name": "John Doe",
        "phone": "+1234567890",
        "special_date_type": "Birthday",
        "custom_message": "Hope you have an amazing day!",
        "offer_details": "Special 20% off offer"
    }
    """
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['customer_name', 'phone', 'special_date_type']
        for field in required_fields:
            if field not in data:
                return Response({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract data
        customer_name = data['customer_name']
        phone = data['phone']
        special_date_type = data['special_date_type']
        custom_message = data.get('custom_message', '')
        offer_details = data.get('offer_details', '')
        
        # Initialize WhatsApp service
        whatsapp_service = WhatsAppService()
        
        # Send the wish message
        result = whatsapp_service.send_wish_message(
            customer_name=customer_name,
            phone=phone,
            special_date_type=special_date_type,
            custom_message=custom_message,
            offer_details=offer_details
        )
        
        if result['success']:
            logger.info(f"WhatsApp wish sent successfully to {customer_name} ({phone})")
            return Response({
                'success': True,
                'message': 'WhatsApp wish sent successfully',
                'message_id': result.get('message_id'),
                'details': {
                    'customer_name': customer_name,
                    'phone': phone,
                    'special_date_type': special_date_type
                }
            }, status=status.HTTP_200_OK)
        else:
            logger.error(f"Failed to send WhatsApp wish to {customer_name}: {result.get('error')}")
            return Response({
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'message': result.get('message', 'Failed to send WhatsApp message')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Error in send_whatsapp_wish: {str(e)}")
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_whatsapp_message(request):
    """
    Send custom WhatsApp message
    
    Expected payload:
    {
        "phone": "+1234567890",
        "message": "Your custom message here"
    }
    """
    try:
        data = request.data
        
        # Validate required fields
        if 'phone' not in data or 'message' not in data:
            return Response({
                'success': False,
                'error': 'Missing required fields: phone and message'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        phone = data['phone']
        message = data['message']
        
        # Initialize WhatsApp service
        whatsapp_service = WhatsAppService()
        
        # Send the message
        result = whatsapp_service.send_message(phone, message)
        
        if result['success']:
            logger.info(f"WhatsApp message sent successfully to {phone}")
            return Response({
                'success': True,
                'message': 'WhatsApp message sent successfully',
                'message_id': result.get('message_id')
            }, status=status.HTTP_200_OK)
        else:
            logger.error(f"Failed to send WhatsApp message to {phone}: {result.get('error')}")
            return Response({
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'message': result.get('message', 'Failed to send WhatsApp message')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Error in send_whatsapp_message: {str(e)}")
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
