# Generated manually

from django.db import migrations

def create_default_prizes(apps, schema_editor):
    """Create default prizes for the spin wheel game"""
    Prize = apps.get_model('spin_wheel', 'Prize')
    
    # Only create prizes if none exist
    if not Prize.objects.exists():
        default_prizes = [
            {
                'name': 'Free Drink',
                'description': 'Get a free drink of your choice!',
                'icon': '🥤',
                'probability': 30,
                'is_active': True
            },
            {
                'name': '10% Discount',
                'description': 'Enjoy 10% off your next meal!',
                'icon': '💰',
                'probability': 25,
                'is_active': True
            },
            {
                'name': 'Free Appetizer',
                'description': 'Complimentary appetizer with your meal!',
                'icon': '🍤',
                'probability': 20,
                'is_active': True
            },
            {
                'name': 'Dessert on Us',
                'description': 'Free dessert with your order!',
                'icon': '🍰',
                'probability': 15,
                'is_active': True
            },
            {
                'name': '20% Discount',
                'description': 'Get 20% off your entire bill!',
                'icon': '🎯',
                'probability': 8,
                'is_active': True
            },
            {
                'name': 'Free Meal',
                'description': 'Win a completely free meal!',
                'icon': '🎉',
                'probability': 2,
                'is_active': True
            }
        ]
        
        for prize_data in default_prizes:
            Prize.objects.create(**prize_data)

def remove_default_prizes(apps, schema_editor):
    """Remove default prizes"""
    Prize = apps.get_model('spin_wheel', 'Prize')
    Prize.objects.filter(name__in=[
        'Free Drink', '10% Discount', 'Free Appetizer', 
        'Dessert on Us', '20% Discount', 'Free Meal'
    ]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('spin_wheel', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_prizes, remove_default_prizes),
    ]
