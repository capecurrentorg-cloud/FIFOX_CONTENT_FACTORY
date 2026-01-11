"""
Vapi.ai Phone Agent Integration Service
Mock implementation for MARA phone agent with order verification workflow
"""
import random
from datetime import datetime


class VapiService:
    """Service for integrating with Vapi.ai phone agent (MARA)"""
    
    def __init__(self, api_key=None, api_url=None):
        self.api_key = api_key
        self.api_url = api_url
        self.mock_mode = not api_key
    
    def simulate_incoming_call(self, customer_phone, customer_name='Customer'):
        """
        Simulate an incoming call to MARA
        
        Real implementation would integrate with Vapi.ai API
        """
        
        if self.mock_mode:
            return self._mock_call_simulation(customer_phone, customer_name)
        
        # TODO: Implement real Vapi.ai API call
        # import requests
        # headers = {'Authorization': f'Bearer {self.api_key}'}
        # data = {
        #     'phone_number': customer_phone,
        #     'assistant_id': 'mara_assistant_id'
        # }
        # response = requests.post(f'{self.api_url}/call', headers=headers, json=data)
        # return response.json()
        
        return {}
    
    def process_transcription(self, transcription_data):
        """
        Process call transcription from Vapi.ai
        
        This would be called by a webhook when call is completed
        """
        
        if self.mock_mode:
            return {
                'processed': True,
                'order_extracted': True,
                'confidence': random.uniform(0.85, 0.99)
            }
        
        # TODO: Implement real transcription processing
        # Extract order details from transcription
        # Use NLP to parse order items, modifiers, etc.
        
        return {}
    
    def verify_order_with_agents(self, order_data):
        """
        Simulate order verification with multiple agents (MARA, LLaMA, Ollama)
        VERA requires 2/3 consensus before approval
        """
        
        # MARA's version (primary agent)
        mara_version = order_data.copy()
        mara_confidence = random.uniform(0.90, 0.99)
        
        # LLaMA's version (silent listener)
        llama_version = order_data.copy()
        # Occasionally introduce small differences for realism
        if random.random() < 0.1:  # 10% chance of slight difference
            llama_version['notes'] = 'Minor discrepancy detected'
        llama_confidence = random.uniform(0.85, 0.95)
        
        # Ollama's version (silent listener)
        ollama_version = order_data.copy()
        if random.random() < 0.1:  # 10% chance of slight difference
            ollama_version['notes'] = 'Reviewing order details'
        ollama_confidence = random.uniform(0.85, 0.95)
        
        # VERA's consensus logic (2/3 match required)
        versions = [mara_version, llama_version, ollama_version]
        confidence_scores = [mara_confidence, llama_confidence, ollama_confidence]
        
        # Simplified matching (in real implementation, would compare order details)
        matches = sum(1 for v in versions if v == mara_version or 'discrepancy' not in v.get('notes', ''))
        
        verified = matches >= 2
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        
        return {
            'verified': verified,
            'mara_version': mara_version,
            'llama_version': llama_version,
            'ollama_version': ollama_version,
            'mara_confidence': mara_confidence,
            'llama_confidence': llama_confidence,
            'ollama_confidence': ollama_confidence,
            'consensus': f"{matches}/3 agents agree",
            'average_confidence': round(avg_confidence, 2),
            'approved_by_vera': verified,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_verification_stats(self):
        """Get verification statistics"""
        
        if self.mock_mode:
            return {
                'total_calls': random.randint(50, 150),
                'successful_verifications': random.randint(48, 148),
                'failed_verifications': random.randint(0, 2),
                'average_confidence': round(random.uniform(0.92, 0.99), 2),
                'mara_accuracy': 99.9,
                'vera_approval_rate': 98.5,
                'consensus_rate': 97.8
            }
        
        # TODO: Fetch real stats from database
        return {}
    
    def _mock_call_simulation(self, customer_phone, customer_name):
        """Generate mock call simulation"""
        
        menu_items = [
            'Signature Burger',
            'Grilled Salmon',
            'Caesar Salad',
            'Ribeye Steak',
            'Margherita Pizza'
        ]
        
        order_items = random.sample(menu_items, random.randint(1, 3))
        
        transcript = f"""
MARA: Thank you for calling FIFOX Restaurant. This is Mara, how can I help you today?

{customer_name.upper()}: Hi, I'd like to place an order for delivery.

MARA: Perfect! Can I get your phone number?

{customer_name.upper()}: Sure, it's {customer_phone}.

MARA: Great! What would you like to order?

{customer_name.upper()}: I'll take {', '.join(order_items)}.

MARA: Excellent choices! Let me read that back to confirm:
- {chr(10).join(f'• {item}' for item in order_items)}

For delivery to your address. Is that correct?

{customer_name.upper()}: Yes, that's perfect!

MARA: ✅ Wonderful! Your order is confirmed and locked. We'll have that to you in about 35-40 minutes. Thank you!
"""
        
        order_data = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'items': [{'name': item, 'quantity': 1} for item in order_items],
            'order_type': 'delivery',
            'status': 'confirmed'
        }
        
        # Verify with multiple agents
        verification = self.verify_order_with_agents(order_data)
        
        return {
            'call_id': f'CALL-{random.randint(1000, 9999)}',
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'call_duration': random.randint(90, 240),  # seconds
            'transcript': transcript,
            'order_data': order_data,
            'verification': verification,
            'status': 'completed',
            'timestamp': datetime.utcnow().isoformat()
        }
