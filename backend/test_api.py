"""
Test script for FIFOX Backend API
Run this after starting the backend with: python backend/app.py
"""
import requests
import json
import time

BACKEND_URL = 'http://localhost:5000'

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f'{BACKEND_URL}/health', timeout=5)
        print(f"✅ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_orders():
    """Test orders API"""
    try:
        # Get all orders
        response = requests.get(f'{BACKEND_URL}/api/orders', timeout=5)
        orders = response.json()
        print(f"✅ Get orders: Found {len(orders)} orders")
        
        # Create a test order
        test_order = {
            'customer_name': 'Test Customer',
            'customer_phone': '(555) 999-8888',
            'items': [
                {'name': 'Test Burger', 'quantity': 1},
                {'name': 'Test Fries', 'quantity': 1}
            ],
            'total_amount': 19.99,
            'order_type': 'pickup'
        }
        
        response = requests.post(f'{BACKEND_URL}/api/orders', 
                               json=test_order, timeout=5)
        if response.status_code == 201:
            order = response.json()
            print(f"✅ Created order: {order['order_id']}")
            
            # Get stats
            response = requests.get(f'{BACKEND_URL}/api/orders/stats', timeout=5)
            stats = response.json()
            print(f"✅ Order stats: {stats}")
            
            return True
    except Exception as e:
        print(f"❌ Orders test failed: {e}")
        return False

def test_content_generation():
    """Test content generation API"""
    try:
        content_request = {
            'platform': 'instagram',
            'content_type': 'post',
            'topic': 'burger special'
        }
        
        response = requests.post(f'{BACKEND_URL}/api/content/generate',
                               json=content_request, timeout=10)
        if response.status_code == 201:
            content = response.json()
            print(f"✅ Generated content: {content['content_id']}")
            print(f"   Caption: {content['caption'][:50]}...")
            print(f"   Viral Score: {content['viral_score']}%")
            return True
    except Exception as e:
        print(f"❌ Content generation test failed: {e}")
        return False

def test_agents():
    """Test agents API"""
    try:
        response = requests.get(f'{BACKEND_URL}/api/agents/status', timeout=5)
        agents = response.json()
        print(f"✅ Agent statuses: Found {len(agents)} agents")
        for agent in agents[:3]:  # Show first 3
            print(f"   - {agent['agent_name']}: {agent['status']}")
        return True
    except Exception as e:
        print(f"❌ Agents test failed: {e}")
        return False

def test_timers():
    """Test timers API"""
    try:
        # Get active timers
        response = requests.get(f'{BACKEND_URL}/api/timers', timeout=5)
        timers = response.json()
        print(f"✅ Active timers: {len(timers)}")
        
        # Create a test timer
        timer_request = {
            'order_id': 'TEST-001',
            'dish_name': 'Test Burger',
            'duration': 600  # 10 minutes
        }
        
        response = requests.post(f'{BACKEND_URL}/api/timers',
                               json=timer_request, timeout=5)
        if response.status_code == 201:
            timer = response.json()
            print(f"✅ Created timer: {timer['timer_id']}")
            return True
    except Exception as e:
        print(f"❌ Timers test failed: {e}")
        return False

def test_settings():
    """Test settings API"""
    try:
        response = requests.get(f'{BACKEND_URL}/api/settings', timeout=5)
        settings = response.json()
        print(f"✅ Settings: {len(settings)} settings loaded")
        return True
    except Exception as e:
        print(f"❌ Settings test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 FIFOX Backend API Tests\n")
    print(f"Testing backend at: {BACKEND_URL}\n")
    
    tests = [
        ('Health Check', test_health),
        ('Orders API', test_orders),
        ('Content Generation API', test_content_generation),
        ('Agents API', test_agents),
        ('Timers API', test_timers),
        ('Settings API', test_settings)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📝 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            failed += 1
        time.sleep(0.5)  # Brief pause between tests
    
    print(f"\n{'='*50}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"{'='*50}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Backend is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check backend logs.")

if __name__ == '__main__':
    main()
