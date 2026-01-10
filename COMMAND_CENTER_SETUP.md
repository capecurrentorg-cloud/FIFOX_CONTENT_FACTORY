# FIFOX Command Center - Order Management & Tracking

## Overview
Real-time restaurant command center displaying:
- Active phone orders from Mara
- Order timers and status
- Delivery map with live tracking
- Kitchen ticket management
- Toast POS integration

---

## System Architecture

```
Phone Call → Mara (AI Agent) → Order Captured
                ↓
         Toast POS API → Create Ticket
                ↓
         Command Center Dashboard
                ↓
    ┌──────────┼──────────┐
    ↓          ↓          ↓
 Kitchen    Timer      Map View
 Display    Counter    (Delivery)
```

---

## Features

### 1. Order Ticket System
When Mara takes a phone order:
- Creates ticket in Toast POS automatically
- Starts countdown timer
- Assigns ticket number
- Routes to kitchen display
- Tracks order status (Pending → Preparing → Ready → Out for Delivery)

### 2. Command Center Display

**Left Panel: Active Orders**
```
┌─────────────────────────────┐
│ ORDER #1247 - 🕐 12:34      │
│ John Doe - (555) 123-4567   │
│ 1x Ribeye Steak ($26.99)    │
│ 1x Caesar Salad ($9.99)     │
│ Status: PREPARING           │
│ ETA: 15 minutes             │
└─────────────────────────────┘
```

**Center Panel: Timer Dashboard**
```
ACTIVE ORDERS (5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#1247  [████████░░] 8min
#1248  [██████░░░░] 12min
#1249  [███░░░░░░░] 18min
```

**Right Panel: Delivery Map**
```
┌─────────────────────────────┐
│     🗺️  GOOGLE MAPS          │
│                             │
│   📍 Order #1247            │
│      123 Main St            │
│      ETA: 15 min            │
│                             │
│   📍 Order #1248            │
│      456 Oak Ave            │
│      ETA: 22 min            │
└─────────────────────────────┘
```

### 3. Toast POS Integration

**API Endpoints:**
```javascript
// Create Order
POST /restaurants/{restaurantGuid}/orders
{
  "check": {
    "customer": {
      "firstName": "John",
      "lastName": "Doe",
      "phone": "5551234567"
    },
    "selections": [
      {
        "itemId": "ribeye-steak",
        "quantity": 1,
        "price": 26.99
      }
    ],
    "deliveryInfo": {
      "address": "123 Main St",
      "deliveryTime": "2024-01-10T18:30:00Z"
    }
  }
}

// Get Order Status
GET /restaurants/{restaurantGuid}/orders/{orderId}

// Update Order Status
PUT /restaurants/{restaurantGuid}/orders/{orderId}
{
  "status": "PREPARING" | "READY" | "OUT_FOR_DELIVERY" | "DELIVERED"
}
```

### 4. Google Maps Integration

**Display Features:**
- Real-time delivery driver location
- Customer delivery addresses
- Route optimization
- ETA calculations
- Traffic updates

**API Setup:**
```javascript
// Google Maps API
const map = new google.maps.Map(document.getElementById('map'), {
  center: { lat: 40.7128, lng: -74.0060 },
  zoom: 12
});

// Add order markers
orders.forEach(order => {
  new google.maps.Marker({
    position: order.deliveryAddress.coords,
    map: map,
    title: `Order #${order.id}`,
    icon: '🍕'
  });
});
```

---

## Setup Instructions

### 1. Toast POS Setup

**Requirements:**
- Toast account with API access
- Restaurant GUID
- API credentials

**Steps:**
```bash
# 1. Get Toast API credentials
# Login to Toast Dashboard → Settings → API → Generate Token

# 2. Configure environment
TOAST_API_URL=https://api.toasttab.com
TOAST_RESTAURANT_GUID=your_restaurant_guid
TOAST_API_TOKEN=your_api_token

# 3. Test connection
curl -X GET \
  "${TOAST_API_URL}/restaurants/${TOAST_RESTAURANT_GUID}/menus" \
  -H "Authorization: Bearer ${TOAST_API_TOKEN}"
```

### 2. Google Maps Setup

**Requirements:**
- Google Cloud account
- Maps JavaScript API enabled
- API key with Maps & Geocoding

**Steps:**
```bash
# 1. Enable APIs in Google Cloud Console
# - Maps JavaScript API
# - Geocoding API
# - Directions API

# 2. Get API key
GOOGLE_MAPS_API_KEY=your_api_key_here

# 3. Add to command center
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY"></script>
```

### 3. Command Center Installation

```bash
# Install dependencies
npm install socket.io express toast-api-client @googlemaps/js-api-loader

# Configure
cp .env.example .env
# Edit .env with your API keys

# Start command center
npm start

# Access at: http://localhost:3000/command-center
```

---

## Workflow Example

### Phone Order Flow

1. **Customer calls restaurant**
   - Mara (AI) answers
   - Takes order details
   - Confirms delivery address

2. **Order created in Toast**
   ```javascript
   // Mara triggers this automatically
   const order = await toast.createOrder({
     customer: { name, phone },
     items: orderItems,
     delivery: { address, time }
   });
   ```

3. **Ticket appears on Command Center**
   - Order number assigned: #1247
   - Timer starts: 0:00
   - Status: PENDING
   - Map marker added

4. **Kitchen receives ticket**
   - Displays on kitchen screen
   - Prints at prep station
   - Staff marks "START PREPARING"

5. **Timer updates**
   - Command center shows: "PREPARING - 8 min"
   - Color coding: Green (on time), Yellow (5min late), Red (10min+ late)

6. **Food ready**
   - Kitchen marks "READY"
   - Driver assigned
   - Route calculated on map

7. **Out for delivery**
   - Live GPS tracking
   - ETA updates
   - Customer notified

8. **Delivered**
   - Driver confirms
   - Order archived
   - Timer stops
   - Metrics logged

---

## Configuration Files

### config.json
```json
{
  "toast": {
    "apiUrl": "https://api.toasttab.com",
    "restaurantGuid": "YOUR_GUID",
    "apiToken": "YOUR_TOKEN"
  },
  "googleMaps": {
    "apiKey": "YOUR_API_KEY",
    "defaultCenter": {
      "lat": 40.7128,
      "lng": -74.0060
    },
    "defaultZoom": 12
  },
  "orderTimers": {
    "warningThreshold": 15,
    "alertThreshold": 20,
    "autoRefreshInterval": 5000
  },
  "commandCenter": {
    "port": 3000,
    "socketEnabled": true,
    "soundAlerts": true
  }
}
```

---

## API Documentation

### Toast POS Endpoints

**Create Order:**
`POST /restaurants/{guid}/orders`

**Get Orders:**
`GET /restaurants/{guid}/orders?date={date}`

**Update Status:**
`PUT /restaurants/{guid}/orders/{orderId}`

**Get Menu:**
`GET /restaurants/{guid}/menus`

### Command Center WebSocket Events

**Order Created:**
```javascript
socket.on('order:created', (order) => {
  // Add to display
  // Start timer
  // Add map marker
});
```

**Order Updated:**
```javascript
socket.on('order:updated', (order) => {
  // Update status
  // Refresh timer
  // Update map
});
```

**Order Completed:**
```javascript
socket.on('order:completed', (order) => {
  // Archive order
  // Stop timer
  // Remove marker
});
```

---

## Dashboard Screenshots Placeholder

```
[Command Center Layout]
┌────────────────────────────────────────────────────────────┐
│ FIFOX COMMAND CENTER                          🦊  12:45 PM │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  ACTIVE ORDERS (5)    │    TIMERS    │    DELIVERY MAP    │
│  ─────────────────────┼──────────────┼────────────────────│
│  #1247 John Doe       │  #1247  8min │      📍 #1247      │
│  Ribeye + Salad       │  #1248 12min │      📍 #1248      │
│  🕐 PREPARING         │  #1249 18min │  🗺️  [MAP VIEW]   │
│  ──────────────────── │  #1250 22min │                    │
│  #1248 Jane Smith     │  #1251  5min │      📍 #1249      │
│  Salmon + Wine        │              │                    │
│  🔥 READY             │  AVG: 13min  │      📍 #1250      │
│                       │              │                    │
└────────────────────────────────────────────────────────────┘
```

---

## Cost Breakdown

**Monthly Costs:**
- Toast POS: $165/month (includes API access)
- Google Maps API: ~$20/month (estimated for 1000 orders)
- Server hosting: $20-50/month
- **Total: ~$205-235/month**

---

## Support & Troubleshooting

**Common Issues:**

1. **Orders not appearing in Toast**
   - Check API token validity
   - Verify restaurant GUID
   - Check menu item IDs match

2. **Map not loading**
   - Verify Google Maps API key
   - Check API is enabled in Google Cloud
   - Verify billing is active

3. **Timers not updating**
   - Check WebSocket connection
   - Verify auto-refresh interval
   - Check browser console for errors

---

## Next Steps

1. Set up Toast POS account
2. Get API credentials
3. Enable Google Maps API
4. Install command center software
5. Test with sample orders
6. Train staff on system
7. Go live!

See `setup_command_center.js` for automated setup script.
