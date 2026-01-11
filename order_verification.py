#!/usr/bin/env python3
"""
FIFOX Order Verification System
3-way listening and approval system:
- MARA answers phones (primary agent)
- LLaMA listens and reports
- Ollama listens and reports
- VERA requires 2/3 consensus before posting to kitchen via Toast API
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Configuration from environment variables
TOAST_API_KEY = os.getenv('TOAST_API_KEY', '')
TOAST_RESTAURANT_GUID = os.getenv('TOAST_RESTAURANT_GUID', '')
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
VAPI_API_KEY = os.getenv('VAPI_API_KEY', '')


class OrderStatus(Enum):
    """Order status throughout the verification process"""
    PENDING = "pending"
    LISTENING = "listening"
    VERIFYING = "verifying"
    APPROVED = "approved"
    REJECTED = "rejected"
    SENT_TO_KITCHEN = "sent_to_kitchen"


@dataclass
class OrderItem:
    """Represents a single item in an order"""
    name: str
    quantity: int
    modifiers: List[str] = None
    special_instructions: str = ""
    
    def __post_init__(self):
        if self.modifiers is None:
            self.modifiers = []
    
    def to_dict(self):
        return asdict(self)
    
    def __eq__(self, other):
        """Compare two order items for equality"""
        if not isinstance(other, OrderItem):
            return False
        return (self.name.lower() == other.name.lower() and
                self.quantity == other.quantity and
                sorted([m.lower() for m in self.modifiers]) == sorted([m.lower() for m in other.modifiers]))


@dataclass
class Order:
    """Complete order from a customer"""
    call_id: str
    customer_phone: str
    customer_name: str
    items: List[OrderItem]
    delivery_address: Optional[str] = None
    special_instructions: str = ""
    order_type: str = "delivery"  # delivery, pickup, dine-in
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'call_id': self.call_id,
            'customer_phone': self.customer_phone,
            'customer_name': self.customer_name,
            'items': [item.to_dict() for item in self.items],
            'delivery_address': self.delivery_address,
            'special_instructions': self.special_instructions,
            'order_type': self.order_type,
            'timestamp': self.timestamp
        }


@dataclass
class AgentReport:
    """Report from one of the listening agents"""
    agent_name: str  # mara, llama, ollama
    call_id: str
    order: Order
    confidence: float  # 0.0 to 1.0
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


@dataclass
class VerificationResult:
    """Result of VERA's verification process"""
    call_id: str
    approved: bool
    consensus_level: str  # "perfect" (3/3), "majority" (2/3), "none" (0/3)
    confidence: int  # 0-100
    final_order: Optional[Order]
    matching_agents: List[str]
    discrepancies: List[str]
    action: str  # SEND_TO_KITCHEN, REQUEST_CLARIFICATION
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class OrderVerifier:
    """
    VERA - The Order Verifier
    Compares orders from 3 agents and approves if 2/3 match
    """
    
    def __init__(self):
        self.pending_orders: Dict[str, Dict[str, AgentReport]] = {}
        self.verified_orders: Dict[str, VerificationResult] = {}
        self.kitchen_orders: Dict[str, dict] = {}
    
    def receive_report(self, report: AgentReport) -> Optional[VerificationResult]:
        """
        Receive an order report from one of the agents
        Returns verification result if all 3 agents have reported
        """
        call_id = report.call_id
        
        # Initialize storage for this call if needed
        if call_id not in self.pending_orders:
            self.pending_orders[call_id] = {}
        
        # Store the report
        self.pending_orders[call_id][report.agent_name] = report
        
        print(f"📥 VERA received report from {report.agent_name.upper()} for call {call_id}")
        print(f"   Agents reported so far: {len(self.pending_orders[call_id])}/3")
        
        # Check if we have all 3 reports
        if len(self.pending_orders[call_id]) == 3:
            print(f"✓ All 3 agents have reported for call {call_id}. Verifying consensus...")
            result = self._verify_consensus(call_id)
            return result
        
        return None
    
    def _verify_consensus(self, call_id: str) -> VerificationResult:
        """
        Check for 2/3 consensus among the three agents
        """
        reports = self.pending_orders[call_id]
        
        # Get orders from each agent
        mara_order = reports['mara'].order if 'mara' in reports else None
        llama_order = reports['llama'].order if 'llama' in reports else None
        ollama_order = reports['ollama'].order if 'ollama' in reports else None
        
        # Compare all pairs
        matches = []
        discrepancies = []
        
        if mara_order and llama_order:
            if self._compare_orders(mara_order, llama_order):
                matches.append('mara-llama')
            else:
                discrepancies.append(f"MARA vs LLaMA: {self._get_differences(mara_order, llama_order)}")
        
        if mara_order and ollama_order:
            if self._compare_orders(mara_order, ollama_order):
                matches.append('mara-ollama')
            else:
                discrepancies.append(f"MARA vs Ollama: {self._get_differences(mara_order, ollama_order)}")
        
        if llama_order and ollama_order:
            if self._compare_orders(llama_order, ollama_order):
                matches.append('llama-ollama')
            else:
                discrepancies.append(f"LLaMA vs Ollama: {self._get_differences(llama_order, ollama_order)}")
        
        # Determine consensus
        match_count = len(matches)
        
        if match_count == 3:
            # Perfect consensus
            consensus_level = "perfect"
            confidence = 100
            approved = True
            action = "SEND_TO_KITCHEN"
            final_order = mara_order  # All match, use MARA's
            matching_agents = ['mara', 'llama', 'ollama']
            
        elif match_count >= 2:
            # Majority consensus (2/3)
            consensus_level = "majority"
            confidence = 67
            approved = True
            action = "SEND_TO_KITCHEN"
            # Use the majority order
            final_order = self._get_majority_order(mara_order, llama_order, ollama_order, matches)
            matching_agents = self._get_matching_agents(matches)
            
        else:
            # No consensus
            consensus_level = "none"
            confidence = 0
            approved = False
            action = "REQUEST_CLARIFICATION"
            final_order = None
            matching_agents = []
        
        result = VerificationResult(
            call_id=call_id,
            approved=approved,
            consensus_level=consensus_level,
            confidence=confidence,
            final_order=final_order,
            matching_agents=matching_agents,
            discrepancies=discrepancies,
            action=action
        )
        
        # Store the result
        self.verified_orders[call_id] = result
        
        # Print result
        self._print_verification_result(result)
        
        # If approved, send to kitchen
        if approved and final_order:
            self.send_to_kitchen(call_id, final_order)
        
        return result
    
    def _compare_orders(self, order1: Order, order2: Order) -> bool:
        """Compare two orders for equality"""
        if len(order1.items) != len(order2.items):
            return False
        
        # Create sorted lists of items for comparison
        items1_sorted = sorted([str(item.to_dict()) for item in order1.items])
        items2_sorted = sorted([str(item.to_dict()) for item in order2.items])
        
        return items1_sorted == items2_sorted
    
    def _get_differences(self, order1: Order, order2: Order) -> str:
        """Get human-readable differences between orders"""
        diffs = []
        
        if len(order1.items) != len(order2.items):
            diffs.append(f"Item count ({len(order1.items)} vs {len(order2.items)})")
        
        # Compare each item
        for i, item1 in enumerate(order1.items):
            if i < len(order2.items):
                item2 = order2.items[i]
                if item1.name != item2.name:
                    diffs.append(f"Item {i+1} name ({item1.name} vs {item2.name})")
                if item1.quantity != item2.quantity:
                    diffs.append(f"Item {i+1} quantity ({item1.quantity} vs {item2.quantity})")
                if item1.modifiers != item2.modifiers:
                    diffs.append(f"Item {i+1} modifiers ({item1.modifiers} vs {item2.modifiers})")
        
        return ", ".join(diffs) if diffs else "Different items"
    
    def _get_majority_order(self, mara_order: Order, llama_order: Order, 
                           ollama_order: Order, matches: List[str]) -> Order:
        """Get the order that has majority support"""
        if 'mara-llama' in matches:
            return mara_order
        elif 'mara-ollama' in matches:
            return mara_order
        else:  # llama-ollama
            return llama_order
    
    def _get_matching_agents(self, matches: List[str]) -> List[str]:
        """Get list of agents that match"""
        agents = set()
        for match in matches:
            agents.update(match.split('-'))
        return list(agents)
    
    def _print_verification_result(self, result: VerificationResult):
        """Print verification result to console"""
        print("\n" + "="*60)
        print("🦊 VERA'S VERIFICATION RESULT")
        print("="*60)
        print(f"Call ID: {result.call_id}")
        print(f"Consensus: {result.consensus_level.upper()} ({len(result.matching_agents)}/3)")
        print(f"Confidence: {result.confidence}%")
        print(f"Approved: {'✅ YES' if result.approved else '❌ NO'}")
        print(f"Action: {result.action}")
        
        if result.matching_agents:
            print(f"Matching Agents: {', '.join([a.upper() for a in result.matching_agents])}")
        
        if result.discrepancies:
            print(f"\n⚠️  Discrepancies:")
            for disc in result.discrepancies:
                print(f"   - {disc}")
        
        if result.final_order:
            print(f"\n📋 Final Order:")
            for i, item in enumerate(result.final_order.items, 1):
                mods = f" ({', '.join(item.modifiers)})" if item.modifiers else ""
                print(f"   {i}. {item.quantity}x {item.name}{mods}")
        
        print("="*60 + "\n")
    
    def send_to_kitchen(self, call_id: str, order: Order) -> bool:
        """
        Send verified order to kitchen via Toast API
        Starts timer and displays in command center
        """
        print(f"🍳 Sending order to kitchen...")
        
        # Prepare order data for Toast API
        toast_order = self._prepare_toast_order(order)
        
        # Store in kitchen orders
        order_number = len(self.kitchen_orders) + 1
        self.kitchen_orders[call_id] = {
            'order_number': order_number,
            'order': order.to_dict(),
            'toast_data': toast_order,
            'status': 'pending',
            'start_time': datetime.now().isoformat(),
            'timer_started': True
        }
        
        # In production, send to Toast API:
        # response = self._send_to_toast_api(toast_order)
        
        print(f"✅ Order #{order_number} sent to kitchen")
        print(f"⏱️  Timer started for call {call_id}")
        
        # Save to command center data file
        self._update_command_center(call_id, order_number)
        
        return True
    
    def _prepare_toast_order(self, order: Order) -> dict:
        """Prepare order data in Toast API format"""
        return {
            'customer': {
                'phone': order.customer_phone,
                'name': order.customer_name,
                'address': order.delivery_address
            },
            'orderType': order.order_type,
            'items': [
                {
                    'name': item.name,
                    'quantity': item.quantity,
                    'modifiers': item.modifiers,
                    'specialInstructions': item.special_instructions
                }
                for item in order.items
            ],
            'specialInstructions': order.special_instructions,
            'timestamp': order.timestamp
        }
    
    def _send_to_toast_api(self, order_data: dict) -> dict:
        """
        Send order to Toast POS API
        Requires TOAST_API_KEY and TOAST_RESTAURANT_GUID
        """
        # This would be the actual API call in production
        # For now, return mock response
        return {
            'success': True,
            'orderId': f"TOAST_{int(time.time())}",
            'status': 'sent'
        }
    
    def _update_command_center(self, call_id: str, order_number: int):
        """Update command center data file with new order"""
        try:
            # Read existing command center data
            data_file = 'command_center_data.json'
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {'orders': [], 'timers': []}
            
            # Add new order
            kitchen_order = self.kitchen_orders[call_id]
            data['orders'].append({
                'order_number': order_number,
                'call_id': call_id,
                'status': 'preparing',
                'timestamp': kitchen_order['start_time'],
                'order_details': kitchen_order['order']
            })
            
            # Add timer
            data['timers'].append({
                'order_number': order_number,
                'start_time': kitchen_order['start_time'],
                'status': 'active'
            })
            
            # Save back to file
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Command center updated with order #{order_number}")
            
        except Exception as e:
            print(f"⚠️  Error updating command center: {e}")


# Helper functions for agent integration

def simulate_mara_order(call_id: str) -> AgentReport:
    """Simulate MARA taking an order"""
    order = Order(
        call_id=call_id,
        customer_phone="+15551234567",
        customer_name="Sarah Johnson",
        items=[
            OrderItem(name="Signature Burger", quantity=1, modifiers=["No onions", "Extra cheese"]),
            OrderItem(name="Caesar Salad", quantity=1),
            OrderItem(name="Strawberry Lemonade", quantity=1)
        ],
        delivery_address="123 Main Street, Apt 4B",
        order_type="delivery"
    )
    
    return AgentReport(
        agent_name="mara",
        call_id=call_id,
        order=order,
        confidence=0.95
    )


def simulate_llama_order(call_id: str, match: bool = True) -> AgentReport:
    """Simulate LLaMA listening and transcribing"""
    if match:
        # Matching order
        order = Order(
            call_id=call_id,
            customer_phone="+15551234567",
            customer_name="Sarah Johnson",
            items=[
                OrderItem(name="Signature Burger", quantity=1, modifiers=["No onions", "Extra cheese"]),
                OrderItem(name="Caesar Salad", quantity=1),
                OrderItem(name="Strawberry Lemonade", quantity=1)
            ],
            delivery_address="123 Main Street, Apt 4B",
            order_type="delivery"
        )
    else:
        # Slightly different order
        order = Order(
            call_id=call_id,
            customer_phone="+15551234567",
            customer_name="Sarah Johnson",
            items=[
                OrderItem(name="Signature Burger", quantity=1, modifiers=["Extra cheese"]),  # Missing "No onions"
                OrderItem(name="Caesar Salad", quantity=1),
                OrderItem(name="Strawberry Lemonade", quantity=1)
            ],
            delivery_address="123 Main Street, Apt 4B",
            order_type="delivery"
        )
    
    return AgentReport(
        agent_name="llama",
        call_id=call_id,
        order=order,
        confidence=0.92
    )


def simulate_ollama_order(call_id: str, match: bool = True) -> AgentReport:
    """Simulate Ollama listening and transcribing"""
    if match:
        # Matching order
        order = Order(
            call_id=call_id,
            customer_phone="+15551234567",
            customer_name="Sarah Johnson",
            items=[
                OrderItem(name="Signature Burger", quantity=1, modifiers=["No onions", "Extra cheese"]),
                OrderItem(name="Caesar Salad", quantity=1),
                OrderItem(name="Strawberry Lemonade", quantity=1)
            ],
            delivery_address="123 Main Street, Apt 4B",
            order_type="delivery"
        )
    else:
        # Different order
        order = Order(
            call_id=call_id,
            customer_phone="+15551234567",
            customer_name="Sarah Johnson",
            items=[
                OrderItem(name="Ribeye Steak", quantity=1, modifiers=["Medium rare"]),  # Completely different
                OrderItem(name="Caesar Salad", quantity=1),
            ],
            delivery_address="123 Main Street, Apt 4B",
            order_type="delivery"
        )
    
    return AgentReport(
        agent_name="ollama",
        call_id=call_id,
        order=order,
        confidence=0.89
    )


# Main demo function
def demo_verification_system():
    """
    Demonstrate the 3-way verification system
    """
    print("\n" + "="*60)
    print("🦊 FIFOX ORDER VERIFICATION SYSTEM DEMO")
    print("="*60 + "\n")
    
    verifier = OrderVerifier()
    call_id = f"CALL_{int(time.time())}"
    
    print(f"📞 Simulating incoming call: {call_id}\n")
    
    # Scenario 1: Perfect consensus (3/3)
    print("SCENARIO 1: Perfect Consensus (3/3 match)")
    print("-" * 60)
    
    mara_report = simulate_mara_order(call_id)
    llama_report = simulate_llama_order(call_id, match=True)
    ollama_report = simulate_ollama_order(call_id, match=True)
    
    verifier.receive_report(mara_report)
    verifier.receive_report(llama_report)
    result = verifier.receive_report(ollama_report)
    
    time.sleep(2)
    
    # Scenario 2: Majority consensus (2/3)
    call_id_2 = f"CALL_{int(time.time())}"
    print("\n\nSCENARIO 2: Majority Consensus (2/3 match)")
    print("-" * 60)
    
    mara_report_2 = simulate_mara_order(call_id_2)
    llama_report_2 = simulate_llama_order(call_id_2, match=True)
    ollama_report_2 = simulate_ollama_order(call_id_2, match=False)
    
    verifier.receive_report(mara_report_2)
    verifier.receive_report(llama_report_2)
    result_2 = verifier.receive_report(ollama_report_2)
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    demo_verification_system()
