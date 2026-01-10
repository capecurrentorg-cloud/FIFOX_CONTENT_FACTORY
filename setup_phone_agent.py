#!/usr/bin/env python3
"""
FIFOX Phone Agent Integration
Connects Mara (AI phone agent) with restaurant menu and operations
"""

import json
import os
from datetime import datetime

def load_menu():
    """Load restaurant menu"""
    with open('sample_restaurant_menu.json', 'r') as f:
        return json.load(f)

def generate_phone_agent_prompt(menu):
    """Generate the AI prompt for the phone agent"""
    
    # Build menu text
    menu_text = f"Restaurant: {menu['restaurant_name']}\n"
    menu_text += f"Tagline: {menu['tagline']}\n\n"
    
    for category, items in menu['categories'].items():
        menu_text += f"\n{category.upper()}:\n"
        for item in items:
            menu_text += f"- {item['name']}: {item['description']} - ${item['price']}\n"
    
    prompt = f"""You are Mara, a warm and friendly AI phone assistant for {menu['restaurant_name']}.

PERSONALITY:
- Warm, patient, and detail-oriented
- Never rush customers
- Repeat orders back word-for-word
- Apologetic when clarifying
- Make customers feel heard and valued

GREETING:
"Hi! Thanks for calling {menu['restaurant_name']}. This is Mara. How can I help you today?"

MENU:
{menu_text}

HOURS:
{json.dumps(menu['hours'], indent=2)}

CONTACT:
Phone: {menu['contact']['phone']}
Address: {menu['contact']['address']}

YOUR CAPABILITIES:
1. Take phone orders
2. Make reservations
3. Answer menu questions
4. Provide hours and location information
5. Handle dietary restrictions and allergies
6. Suggest menu items based on preferences

INSTRUCTIONS:
- Always confirm order details before finalizing
- Ask about allergies and dietary restrictions
- Suggest popular items when customers are unsure
- Be patient with indecisive customers
- End calls warmly: "Thank you for calling {menu['restaurant_name']}! We'll see you soon!"

Remember: You're Mara, and you make every customer feel like a VIP!
"""
    
    return prompt

def save_agent_prompt(prompt, filename='mara_agent_prompt.txt'):
    """Save the generated prompt"""
    with open(filename, 'w') as f:
        f.write(prompt)
    print(f"✓ Saved agent prompt to: {filename}")

def main():
    """Main setup function"""
    print("🦊 FIFOX Phone Agent Setup")
    print("=" * 60)
    
    # Load menu
    print("\n📋 Loading menu...")
    menu = load_menu()
    print(f"✓ Loaded menu for: {menu['restaurant_name']}")
    
    # Generate prompt
    print("\n🤖 Generating Mara's AI prompt...")
    prompt = generate_phone_agent_prompt(menu)
    
    # Save prompt
    save_agent_prompt(prompt)
    
    print("\n" + "=" * 60)
    print("✓ Phone agent setup complete!")
    print("\n📝 Next Steps:")
    print("1. Choose a platform:")
    print("   - Vapi.ai (easiest): https://vapi.ai")
    print("   - Bland.ai: https://bland.ai")
    print("   - Custom (Twilio + OpenAI)")
    print("\n2. Upload mara_agent_prompt.txt to your chosen platform")
    print("3. Configure voice settings (female, warm, medium speed)")
    print("4. Connect your phone number")
    print("5. Test with a few calls!")
    print("\n💡 See PHONE_AGENT_SETUP.md for detailed instructions")

if __name__ == "__main__":
    main()
