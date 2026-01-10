#!/usr/bin/env python3
"""
FIFOX Content Generator Test Script
Tests the content generation system with sample restaurant data
"""

import json
import random
from datetime import datetime

def load_menu(filename='sample_restaurant_menu.json'):
    """Load the restaurant menu from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return None

def generate_daily_special():
    """Generate a daily special post"""
    specials = [
        "Fresh Catch of the Day - Market Price",
        "Chef's Pasta Special - $22.99",
        "Prime Rib Special - $32.99",
        "Lobster Tail Dinner - $39.99"
    ]
    return random.choice(specials)

def generate_social_post(menu_data):
    """Generate a sample social media post"""
    templates = [
        "🦊 Try our {item}! {description} Only ${price}!",
        "New favorite alert! 🔥 Our {item} is a must-try. {description}",
        "Weekend vibes call for {item}! {description} Reserve your table now!",
        "📍 Stop by and enjoy our {item} - {description} You won't regret it!"
    ]
    
    # Get random item from menu
    category = random.choice(list(menu_data['categories'].keys()))
    item = random.choice(menu_data['categories'][category])
    
    template = random.choice(templates)
    post = template.format(
        item=item['name'],
        description=item['description'],
        price=item['price']
    )
    
    return {
        'timestamp': datetime.now().isoformat(),
        'content': post,
        'category': category,
        'item': item['name']
    }

def generate_content_batch(menu_data, count=5):
    """Generate multiple content pieces"""
    content_batch = []
    
    for i in range(count):
        content_batch.append(generate_social_post(menu_data))
    
    return content_batch

def main():
    """Main test function"""
    print("🦊 FIFOX Content Generator - Test Run")
    print("=" * 50)
    
    # Load menu
    menu = load_menu()
    if not menu:
        return
    
    print(f"\n✓ Loaded menu for: {menu['restaurant_name']}")
    print(f"  Tagline: {menu['tagline']}")
    
    # Generate daily special
    print(f"\n📅 Daily Special:")
    print(f"  {generate_daily_special()}")
    
    # Generate social posts
    print(f"\n📱 Generated Social Media Posts:")
    print("-" * 50)
    
    posts = generate_content_batch(menu, count=5)
    for i, post in enumerate(posts, 1):
        print(f"\nPost #{i}:")
        print(f"  {post['content']}")
        print(f"  [Category: {post['category']} | Item: {post['item']}]")
    
    print("\n" + "=" * 50)
    print("✓ Content generation test complete!")
    print("\n💡 This is placeholder content. Replace with actual menu items.")

if __name__ == "__main__":
    main()
