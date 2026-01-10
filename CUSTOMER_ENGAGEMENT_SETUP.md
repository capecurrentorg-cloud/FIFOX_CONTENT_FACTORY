# FIFOX Reservation & Customer Engagement System
# RHEA - Reservations & Customer Appreciation Agent

## Overview
Automated reservation management and customer relationship system featuring:
- Reservation booking and management
- Birthday and anniversary tracking
- Automatic reward sending (free appetizers, desserts)
- Social media engagement monitoring
- Customer appreciation campaigns

---

## Agent Profile: RHEA

**Name:** Rhea  
**Role:** Reservations & Customer Appreciation  
**Personality:** Gracious, elegant, remembers every detail, makes guests feel like VIPs

### Core Functions

#### 1. Reservation Management
- Accept reservations via phone, website, social media
- Confirm bookings automatically
- Send reminders (24 hours before)
- Track special occasions
- Manage table assignments

#### 2. Customer Tracking
Track and remember:
- Customer names and preferences
- Birthday dates
- Anniversary dates
- Dietary restrictions
- Past orders and favorites
- Visit frequency

#### 3. Automatic Rewards
**Birthday Program:**
- Send "Happy Birthday" message 1 week before
- Offer: Free dessert on their birthday month
- Personalized message from Rhea

**Anniversary Program:**
- Track first visit anniversary
- Send reminder and appreciation
- Offer: Free appetizer on anniversary month
- Encourage celebration at restaurant

**Loyalty Rewards:**
- Track visit frequency
- 5th visit: Free appetizer
- 10th visit: 10% off meal
- VIP status after 20 visits

#### 4. Social Media Engagement
Monitor and respond to:
- Instagram mentions and tags
- Facebook check-ins and posts
- Google Reviews
- Yelp reviews
- Twitter mentions

**Engagement Actions:**
- Thank customers for posts
- Share customer photos (with permission)
- Respond to reviews (positive and negative)
- Invite engaged customers to loyalty program

---

## Setup Options

### Option 1: Automated (Recommended)
**Platform:** Toast POS + Mailchimp + Zapier
- Toast handles reservations
- Mailchimp sends birthday/anniversary emails
- Zapier connects everything

**Cost:** ~$50-100/month

### Option 2: Custom Integration
**Components:**
- Reservation database (Airtable or Google Sheets)
- Email automation (SendGrid, Mailgun)
- Social monitoring (Brand24, Mention)
- Customer tracking system

**Cost:** ~$30-80/month

### Option 3: All-in-One
**Platform:** OpenTable + Customer Relationship features
- Built-in reservation system
- Basic customer tracking
- Email campaigns

**Cost:** Per-cover fee + monthly subscription

---

## Database Schema

```json
{
  "customer_id": "unique_id",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "(555) 123-4567",
  "birthday": "1985-06-15",
  "anniversary_date": "2020-03-20",
  "first_visit": "2023-01-15",
  "total_visits": 12,
  "dietary_restrictions": ["gluten-free"],
  "favorite_items": ["Ribeye Steak", "Caesar Salad"],
  "vip_status": true,
  "rewards_earned": [
    {
      "type": "birthday_dessert",
      "date": "2024-06-15",
      "redeemed": true
    }
  ],
  "social_media": {
    "instagram": "@johndoe",
    "last_post": "2024-01-05"
  }
}
```

---

## Reward Campaign Templates

### Birthday Email
```
Subject: 🎂 Happy Birthday from [Restaurant Name]!

Hi [Name],

Happy Birthday! 🎉

To celebrate YOUR special day, we'd love to treat you to a 
complimentary dessert when you visit us this month.

Just mention this email when you dine with us!

Can't wait to help you celebrate,
Rhea & The [Restaurant] Team

P.S. Book your birthday dinner: [Reservation Link]
```

### Anniversary Email
```
Subject: 🎊 Celebrating YOU - [X] Years with Us!

Hi [Name],

We can't believe it's been [X] years since your first visit!

Thank you for being part of our family. To show our appreciation,
enjoy a FREE appetizer on your next visit this month.

Looking forward to many more meals together!

Warmly,
Rhea & The [Restaurant] Team

Reserve your table: [Reservation Link]
```

### Social Media Thank You
```
@[username] Thank you so much for sharing your experience! 
We're thrilled you enjoyed the [item]! 🦊

Come back soon and ask for Rhea - we have a special 
treat waiting for you! ❤️
```

---

## Integration Setup

### 1. Customer Database Setup
```bash
# Install dependencies
pip install airtable-python-wrapper sendgrid

# Configure
python setup_customer_database.py
```

### 2. Birthday Automation
```bash
# Setup birthday checker (runs daily)
python setup_birthday_automation.py

# This will:
# - Check for upcoming birthdays
# - Send automated emails
# - Track reward redemptions
```

### 3. Social Media Monitor
```bash
# Setup social listening
python setup_social_monitor.py

# Monitors:
# - Instagram hashtags
# - Facebook mentions
# - Google/Yelp reviews
```

---

## API Keys Required

```bash
# Email Service (choose one)
SENDGRID_API_KEY=your_key_here
MAILGUN_API_KEY=your_key_here

# Database (choose one)
AIRTABLE_API_KEY=your_key_here
GOOGLE_SHEETS_CREDENTIALS=path_to_credentials.json

# Social Media (optional)
INSTAGRAM_ACCESS_TOKEN=your_token_here
FACEBOOK_PAGE_TOKEN=your_token_here
TWITTER_BEARER_TOKEN=your_token_here

# Review Platforms (optional)
YELP_API_KEY=your_key_here
GOOGLE_PLACES_API_KEY=your_key_here
```

---

## Quick Start

1. **Choose a platform** (Toast, OpenTable, or custom)
2. **Import existing customers** (if any)
3. **Set up birthday/anniversary tracking**
4. **Configure email templates**
5. **Test with a few customers**
6. **Monitor and adjust**

---

## Metrics to Track

- Reservation conversion rate
- Birthday email open rate
- Anniversary reward redemption rate
- Social media engagement increase
- Customer lifetime value
- Repeat visit frequency

---

## Best Practices

✅ **Do:**
- Personalize every message
- Make rewards easy to redeem
- Track what works
- Thank customers publicly (with permission)
- Follow up after special occasions

❌ **Don't:**
- Spam customers
- Make rewards complicated
- Ignore negative feedback
- Share customer info without permission
- Send generic mass emails

---

## Support

See `setup_customer_engagement.py` for automated setup.
