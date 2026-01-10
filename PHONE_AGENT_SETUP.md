# FIFOX AI Phone Agent Setup
# Mara - Phone Order and Reservation System

## Overview
Connect your restaurant phone system with AI agents to handle:
- Phone orders
- Reservations
- Menu questions
- Hours and location info

## Integration Options

### Option 1: Vapi.ai (Recommended - Easiest)
- Website: https://vapi.ai
- Voice AI that answers calls
- Easy menu integration
- $0.05-0.12 per minute

**Setup:**
1. Sign up at vapi.ai
2. Upload your menu (sample_restaurant_menu.json)
3. Configure voice & personality
4. Forward your restaurant phone number

### Option 2: Bland.ai
- Website: https://bland.ai
- Phone call automation
- LLM-powered conversations
- Similar pricing to Vapi

### Option 3: Custom with Twilio + OpenAI
- More control, more complex
- Requires: Twilio account, OpenAI API
- Phone number handling
- Custom voice integration

### Option 4: RetellAI
- Website: https://retellai.com
- Voice AI for phone calls
- Good for restaurants

## What You Need

1. **Phone Number Provider:**
   - Twilio (recommended)
   - Vonage
   - Bandwidth

2. **AI/LLM Service:**
   - OpenAI GPT-4 (best quality)
   - Anthropic Claude
   - LLaMA (self-hosted, free but complex)
   - Groq (fast, affordable)

3. **Menu Data:**
   - Already have: sample_restaurant_menu.json ✓
   - Use this to train the AI

## Quick Start (Vapi.ai)

```bash
# 1. Get API key from vapi.ai
VAPI_API_KEY=your_key_here

# 2. Upload menu
curl -X POST https://api.vapi.ai/menu \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d @sample_restaurant_menu.json

# 3. Configure assistant
# Set personality: "Friendly, patient, helpful restaurant assistant"
# Set menu knowledge: Upload sample_restaurant_menu.json
# Set voice: Female, warm tone (similar to "Mara" personality)

# 4. Get phone number or forward existing number
```

## Agent Personality (Mara)

**Name:** Mara
**Voice:** Warm, friendly female voice
**Personality Traits:**
- Patient and detail-oriented
- Never rushes customers
- Repeats orders back word-for-word
- Apologetic when clarifying
- Makes customers feel heard

**Example Greeting:**
"Hi! Thanks for calling [Restaurant Name]. This is Mara. How can I help you today?"

## Files Created
- `/phone_agent/` - Phone integration scripts
- `/phone_agent/mara_config.json` - Agent configuration
- `/phone_agent/setup_instructions.md` - Detailed setup

Would you like me to:
1. Set up Vapi.ai integration (recommended)?
2. Create custom Twilio + OpenAI integration?
3. Set up LLaMA locally (free but complex)?
