#!/usr/bin/env python3
"""
FIFOX Order Verification WebSocket Server
Provides real-time updates to the command center UI
"""

import asyncio
import websockets
import json
import time
from order_verification import (
    OrderVerifier, 
    simulate_mara_order, 
    simulate_llama_order, 
    simulate_ollama_order
)

# Connected clients
clients = set()

# Verifier instance
verifier = OrderVerifier()


async def handle_client(websocket, path):
    """Handle WebSocket client connections"""
    clients.add(websocket)
    print(f"✅ Client connected. Total clients: {len(clients)}")
    
    try:
        async for message in websocket:
            data = json.loads(message)
            await handle_message(websocket, data)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)
        print(f"❌ Client disconnected. Total clients: {len(clients)}")


async def handle_message(websocket, data):
    """Handle incoming messages from clients"""
    msg_type = data.get('type')
    
    if msg_type == 'ping':
        await websocket.send(json.dumps({'type': 'pong'}))
    
    elif msg_type == 'start_demo':
        # Start a demo order simulation
        await simulate_order_flow()
    
    elif msg_type == 'get_stats':
        stats = verifier.get_verification_stats()
        await websocket.send(json.dumps({
            'type': 'stats',
            'data': stats
        }))


async def broadcast(message):
    """Broadcast message to all connected clients"""
    if clients:
        await asyncio.gather(
            *[client.send(json.dumps(message)) for client in clients],
            return_exceptions=True
        )


async def simulate_order_flow():
    """Simulate a complete order verification flow"""
    call_id = f"CALL_{int(time.time())}"
    
    print(f"\n🎬 Starting order simulation for {call_id}")
    
    # Step 1: MARA takes order
    await asyncio.sleep(1)
    mara_report = simulate_mara_order(call_id)
    result = verifier.receive_report(mara_report)
    
    await broadcast({
        'type': 'agent_report',
        'call_id': call_id,
        'agent_name': 'mara',
        'order': mara_report.order.to_dict()
    })
    
    # Step 2: LLaMA listens and reports
    await asyncio.sleep(2)
    llama_report = simulate_llama_order(call_id, match=True)
    result = verifier.receive_report(llama_report)
    
    await broadcast({
        'type': 'agent_report',
        'call_id': call_id,
        'agent_name': 'llama',
        'order': llama_report.order.to_dict()
    })
    
    # Step 3: Ollama listens and reports
    await asyncio.sleep(2)
    ollama_report = simulate_ollama_order(call_id, match=True)
    result = verifier.receive_report(ollama_report)
    
    await broadcast({
        'type': 'agent_report',
        'call_id': call_id,
        'agent_name': 'ollama',
        'order': ollama_report.order.to_dict()
    })
    
    # Step 4: VERA verifies and approves
    if result:
        await broadcast({
            'type': 'verification_result',
            'call_id': result.call_id,
            'approved': result.approved,
            'consensus_level': result.consensus_level,
            'confidence': result.confidence,
            'final_order': result.final_order.to_dict() if result.final_order else None,
            'matching_agents': result.matching_agents,
            'discrepancies': result.discrepancies,
            'action': result.action
        })
        
        # Step 5: If approved, send to kitchen
        if result.approved:
            await asyncio.sleep(1)
            kitchen_data = verifier.kitchen_orders.get(call_id)
            if kitchen_data:
                await broadcast({
                    'type': 'kitchen_order',
                    'call_id': call_id,
                    'order_number': kitchen_data['order_number'],
                    'order': kitchen_data['order'],
                    'status': kitchen_data['status'],
                    'start_time': kitchen_data['start_time']
                })
    
    print(f"✅ Order simulation complete for {call_id}\n")


async def timer_loop():
    """Send timer updates every second"""
    while True:
        await asyncio.sleep(1)
        
        # Update all active kitchen timers
        for call_id, kitchen_order in verifier.kitchen_orders.items():
            if kitchen_order.get('timer_started'):
                start_time = kitchen_order['start_time']
                from datetime import datetime
                elapsed = (datetime.now() - datetime.fromisoformat(start_time)).total_seconds()
                
                await broadcast({
                    'type': 'timer_update',
                    'order_number': kitchen_order['order_number'],
                    'elapsed_time': int(elapsed),
                    'status': 'active'
                })


async def periodic_demo():
    """Periodically run demo orders"""
    await asyncio.sleep(5)  # Wait 5 seconds after server start
    
    while True:
        if clients:
            print("\n🎬 Running automated demo order...")
            await simulate_order_flow()
        
        await asyncio.sleep(30)  # Demo every 30 seconds


async def main():
    """Start the WebSocket server"""
    print("\n" + "="*60)
    print("🦊 FIFOX Order Verification Server")
    print("="*60)
    print("Starting WebSocket server on ws://localhost:8765")
    print("Waiting for command center connections...")
    print("="*60 + "\n")
    
    # Start WebSocket server
    server = await websockets.serve(handle_client, "localhost", 8765)
    
    # Start background tasks
    asyncio.create_task(timer_loop())
    asyncio.create_task(periodic_demo())
    
    # Keep server running
    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Server shutting down...")
