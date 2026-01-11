"""
Toast POS Integration Service
Mock implementation with comments for real API integration
"""
import random
from datetime import datetime, timedelta


class ToastPOSService:
    """Service for integrating with Toast POS system"""
    
    def __init__(self, api_key=None, api_url=None):
        self.api_key = api_key
        self.api_url = api_url
        self.mock_mode = not api_key  # Use mock if no API key provided
    
    def fetch_orders(self, since=None):
        """
        Fetch orders from Toast POS
        
        Real API implementation would look like:
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(f'{self.api_url}/orders', headers=headers, params={'since': since})
        return response.json()
        """
        
        if self.mock_mode:
            return self._generate_mock_orders()
        
        # TODO: Implement real Toast POS API call
        # import requests
        # headers = {'Authorization': f'Bearer {self.api_key}'}
        # response = requests.get(
        #     f'{self.api_url}/orders',
        #     headers=headers,
        #     params={'since': since}
        # )
        # return response.json()
        
        return []
    
    def update_order_status(self, order_id, status):
        """
        Update order status in Toast POS
        
        Real API implementation:
        headers = {'Authorization': f'Bearer {self.api_key}'}
        data = {'status': status}
        response = requests.put(f'{self.api_url}/orders/{order_id}', headers=headers, json=data)
        return response.json()
        """
        
        if self.mock_mode:
            return {
                'success': True,
                'order_id': order_id,
                'status': status,
                'updated_at': datetime.utcnow().isoformat()
            }
        
        # TODO: Implement real Toast POS API call
        return {'success': False, 'error': 'Not implemented'}
    
    def handle_webhook(self, webhook_data):
        """
        Handle incoming webhook from Toast POS for new orders
        
        This would be called by a webhook endpoint when Toast receives a new order
        """
        
        if self.mock_mode:
            # Mock webhook processing
            return {
                'processed': True,
                'order_id': webhook_data.get('orderId'),
                'action': 'new_order_received'
            }
        
        # TODO: Implement real webhook processing
        # Validate webhook signature
        # Process order data
        # Trigger internal order creation
        
        return {'processed': False}
    
    def _generate_mock_orders(self):
        """Generate mock orders for development/demo"""
        
        menu_items = [
            {'name': 'Signature Burger', 'price': 14.99},
            {'name': 'Grilled Salmon', 'price': 22.99},
            {'name': 'Caesar Salad', 'price': 10.99},
            {'name': 'Ribeye Steak', 'price': 32.99},
            {'name': 'Chicken Pasta', 'price': 16.99},
            {'name': 'Margherita Pizza', 'price': 13.99},
            {'name': 'Fish & Chips', 'price': 15.99},
            {'name': 'Veggie Wrap', 'price': 11.99}
        ]
        
        customers = [
            {'name': 'Sarah Johnson', 'phone': '(555) 123-4567', 'address': '123 Main St, Apt 4B'},
            {'name': 'Mike Chen', 'phone': '(555) 987-6543', 'address': '456 Oak Ave'},
            {'name': 'Emma Davis', 'phone': '(555) 456-7890', 'address': '789 Elm Street'},
            {'name': 'John Smith', 'phone': '(555) 234-5678', 'address': '321 Pine Road'}
        ]
        
        mock_orders = []
        
        # Generate 2-3 mock orders
        for i in range(random.randint(2, 3)):
            customer = random.choice(customers)
            items = random.sample(menu_items, random.randint(1, 3))
            
            total = sum(item['price'] for item in items)
            
            mock_orders.append({
                'order_id': f'TOAST-{random.randint(1000, 9999)}',
                'customer_name': customer['name'],
                'customer_phone': customer['phone'],
                'customer_address': customer['address'],
                'items': items,
                'total_amount': round(total, 2),
                'status': random.choice(['pending', 'preparing']),
                'order_type': random.choice(['delivery', 'pickup']),
                'timestamp': (datetime.utcnow() - timedelta(minutes=random.randint(5, 60))).isoformat()
            })
        
        return mock_orders
