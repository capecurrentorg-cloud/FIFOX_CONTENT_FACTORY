// FIFOX Dashboard - JavaScript for Panel Switching and Interactions

// ========================================
// NAVIGATION AND PANEL SWITCHING
// ========================================

// Panel switching function
function switchPanel(panelId) {
    // Hide all panels
    document.querySelectorAll('.panel').forEach(panel => {
        panel.classList.remove('active');
    });
    
    // Show selected panel
    const targetPanel = document.getElementById(panelId + '-panel');
    if (targetPanel) {
        targetPanel.classList.add('active');
    }
    
    // Update navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    const activeNav = document.querySelector(`[data-panel="${panelId}"]`);
    if (activeNav) {
        activeNav.classList.add('active');
    }
    
    // Update breadcrumb
    const breadcrumbMap = {
        'overview': 'Home / Overview',
        'command-center': 'Command Center / Orders & Timers',
        'phone-agent': 'Phone Agent / 3-Agent Verification',
        'content-factory': 'Content Factory / 3-Click System',
        'social-hub': 'Social Media / Hub & Analytics',
        'settings': 'Settings / Configuration'
    };
    document.getElementById('breadcrumb').textContent = breadcrumbMap[panelId] || 'Dashboard';
}

// Navigation click handlers
document.addEventListener('DOMContentLoaded', function() {
    // Set up navigation
    document.querySelectorAll('.nav-item[data-panel]').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const panelId = this.getAttribute('data-panel');
            switchPanel(panelId);
        });
    });
    
    // Sidebar toggle for mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
    
    // Initialize dashboard
    initDashboard();
});

// ========================================
// TIME DISPLAY
// ========================================

function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit' 
    });
    
    // Update all time displays
    document.querySelectorAll('.time-display').forEach(display => {
        display.textContent = timeString;
    });
}

// Update time every second
setInterval(updateTime, 1000);
updateTime();

// ========================================
// FOX COMMUNICATIONS FEED
// ========================================

const foxCommunications = [
    {
        time: '10:23 AM',
        from: 'LARA → Content Team',
        message: 'Today\'s Special: Grilled Salmon - create posts highlighting fresh catch!'
    },
    {
        time: '10:25 AM',
        from: 'DARA → IRA & GARA (Instagram)',
        message: 'Competitive Intel: Luigi\'s cheese-pull video got 50k views. Recommend similar angle for our mozzarella sticks.'
    },
    {
        time: '10:27 AM',
        from: 'IRA → VERA',
        message: 'Instagram post ready for review - Salmon special with ocean vibes caption'
    },
    {
        time: '10:28 AM',
        from: 'VERA → IRA',
        message: '✓ APPROVED - Viral Score: 89% - Ready to post'
    },
    {
        time: '10:30 AM',
        from: 'MARA → VERA',
        message: 'Order #1247 confirmed - 3/3 agent match'
    },
    {
        time: '10:30 AM',
        from: 'VERA → Kitchen',
        message: '✓ Order #1247 sent to Toast POS - Timer started'
    }
];

function populateCommunications() {
    const commFeed = document.getElementById('commFeed');
    if (!commFeed) return;
    
    commFeed.innerHTML = '';
    
    foxCommunications.forEach(comm => {
        const commDiv = document.createElement('div');
        commDiv.className = 'comm-message';
        commDiv.innerHTML = `
            <div class="comm-time">[${comm.time}]</div>
            <div class="comm-from">${comm.from}</div>
            <div class="comm-text">${comm.message}</div>
        `;
        commFeed.appendChild(commDiv);
    });
}

// ========================================
// COMMAND CENTER - ORDERS
// ========================================

const sampleOrders = [
    {
        id: '#1234',
        time: '5 min ago',
        customer: 'Sarah Johnson - (555) 123-4567',
        items: ['Signature Burger', 'Caesar Salad', 'Strawberry Lemonade'],
        status: 'preparing'
    },
    {
        id: '#1233',
        time: '12 min ago',
        customer: 'Mike Chen - (555) 987-6543',
        items: ['Ribeye Steak', 'Garlic Mashed Potatoes', 'Red Wine'],
        status: 'ready'
    },
    {
        id: '#1232',
        time: '18 min ago',
        customer: 'Emma Davis - (555) 456-7890',
        items: ['Grilled Salmon', 'Asparagus', 'Sparkling Water'],
        status: 'delivery'
    }
];

function populateOrders() {
    const orderList = document.getElementById('orderList');
    if (!orderList) return;
    
    orderList.innerHTML = '';
    
    sampleOrders.forEach(order => {
        const orderDiv = document.createElement('div');
        orderDiv.className = 'order-card';
        
        const itemsHTML = order.items.map(item => `• ${item}`).join('<br>');
        const statusClass = `status-${order.status}`;
        const statusText = order.status.charAt(0).toUpperCase() + order.status.slice(1);
        
        orderDiv.innerHTML = `
            <div class="order-header">
                <span class="order-number">${order.id}</span>
                <span class="order-time">${order.time}</span>
            </div>
            <div class="customer-name">${order.customer}</div>
            <div class="order-items">${itemsHTML}</div>
            <span class="order-status ${statusClass}">${statusText}</span>
        `;
        
        orderList.appendChild(orderDiv);
    });
}

// ========================================
// COMMAND CENTER - TIMERS
// ========================================

const sampleTimers = [
    { id: 'timer1', order: 'Order #1234', item: '🍔 Burger', minutes: 8, seconds: 45 },
    { id: 'timer2', order: 'Order #1233', item: '🥩 Steak', minutes: 12, seconds: 30 },
    { id: 'timer3', order: 'Order #1230', item: '🍕 Pizza', minutes: 2, seconds: 15, warning: true }
];

let timerIntervals = {};

function populateTimers() {
    const timerList = document.getElementById('timerList');
    if (!timerList) return;
    
    timerList.innerHTML = '';
    
    sampleTimers.forEach(timer => {
        const timerDiv = document.createElement('div');
        timerDiv.className = 'timer-item' + (timer.warning ? ' timer-warning' : '');
        timerDiv.innerHTML = `
            <div class="timer-header">
                <span class="timer-order">${timer.order}</span>
                <span>${timer.item}</span>
            </div>
            <div class="timer-time" id="${timer.id}">
                ${String(timer.minutes).padStart(2, '0')}:${String(timer.seconds).padStart(2, '0')}
            </div>
        `;
        timerList.appendChild(timerDiv);
        
        // Start countdown
        startTimer(timer.id, timer.minutes, timer.seconds);
    });
}

function startTimer(id, startMinutes, startSeconds) {
    let totalSeconds = startMinutes * 60 + startSeconds;
    
    timerIntervals[id] = setInterval(() => {
        if (totalSeconds <= 0) {
            clearInterval(timerIntervals[id]);
            return;
        }
        
        totalSeconds--;
        const mins = Math.floor(totalSeconds / 60);
        const secs = totalSeconds % 60;
        
        const element = document.getElementById(id);
        if (element) {
            element.textContent = String(mins).padStart(2, '0') + ':' + String(secs).padStart(2, '0');
            
            // Add warning class if under 3 minutes
            if (totalSeconds < 180) {
                element.closest('.timer-item').classList.add('timer-warning');
            }
        }
    }, 1000);
}

// ========================================
// MENU CAROUSEL
// ========================================

const menuItems = [
    {
        name: 'Signature Burger',
        description: '8oz grass-fed beef burger with aged cheddar & bacon',
        image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600'
    },
    {
        name: 'Grilled Salmon',
        description: 'Wild-caught Atlantic salmon with lemon butter',
        image: 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=600'
    },
    {
        name: 'Caesar Salad',
        description: 'Fresh romaine with parmesan & croutons',
        image: 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=600'
    },
    {
        name: 'Ribeye Steak',
        description: '12oz prime ribeye with garlic butter',
        image: 'https://images.unsplash.com/photo-1558030006-450675393462?w=600'
    },
    {
        name: 'Chicken Pasta',
        description: 'Grilled chicken with creamy alfredo',
        image: 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=600'
    }
];

let currentMenuIndex = 0;
let carouselInterval = null;

function showMenuItem(index) {
    const item = menuItems[index];
    const imgElement = document.querySelector('.carousel-image img');
    const nameElement = document.getElementById('carouselItemName');
    const descElement = document.getElementById('carouselItemDesc');
    
    if (imgElement) imgElement.src = item.image;
    if (nameElement) nameElement.textContent = item.name;
    if (descElement) descElement.textContent = item.description;
}

function randomMenuItem() {
    currentMenuIndex = Math.floor(Math.random() * menuItems.length);
    showMenuItem(currentMenuIndex);
    showToast('🎲 Random menu item selected!');
}

function startCarousel() {
    showMenuItem(currentMenuIndex);
    
    carouselInterval = setInterval(() => {
        currentMenuIndex = (currentMenuIndex + 1) % menuItems.length;
        showMenuItem(currentMenuIndex);
    }, 5000);
}

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imgElement = document.querySelector('.carousel-image img');
            if (imgElement) {
                imgElement.src = e.target.result;
            }
            showToast('📸 Image uploaded successfully!');
        };
        reader.readAsDataURL(file);
    }
}

// ========================================
// CONTENT GENERATION - 3-CLICK SYSTEM
// ========================================

const contentExamples = {
    instagram: {
        post: {
            caption: "Remember your first burger with Dad? That feeling never gets old. 🍔❤️\n\n#ComfortFood #FamilyMoments #BurgerLove #FoodMemories #NostalgiaEats",
            insight: "Competitor Luigi's got 12k likes on similar close-up shot yesterday. Trending: comfort food nostalgia themes.",
            score: 87,
            image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600'
        },
        story: {
            caption: "Behind the scenes in our kitchen right now 👨‍🍳🔥\n\nSwipe up to order!",
            insight: "Stories with kitchen content get 34% more engagement. Best posted 11am-2pm.",
            score: 82,
            image: 'https://images.unsplash.com/photo-1556910096-6f5e72db6803?w=600'
        },
        reel: {
            caption: "POV: You just walked into heaven 😍🍕\n\n#Reels #FoodPorn #PizzaLover #Satisfying",
            insight: "Reels using trending audio 'Good 4 U' seeing 2.3x normal reach. Recommend close-up food shots.",
            score: 91,
            image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600'
        },
        carousel: {
            caption: "Our Top 5 Most Ordered Dishes (Slide to see why) 👉\n\n1️⃣ Signature Burger\n2️⃣ Grilled Salmon\n3️⃣ Ribeye Steak\n4️⃣ Caesar Salad\n5️⃣ Chocolate Lava Cake",
            insight: "Carousel posts get 3x more saves than single images. Perfect for driving repeat visits.",
            score: 85,
            image: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600'
        }
    },
    tiktok: {
        video: {
            caption: "When the cheese pull hits different 🧀😮‍💨 #FoodTok #CheesePull #SatisfyingVideo #FoodASMR",
            insight: "TikTok algorithm favoring food ASMR content. Cheese pull videos averaging 50k+ views.",
            score: 93,
            image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600'
        },
        trending: {
            caption: "Making our famous burger to this sound cause why not 💅🍔 #Trending #BurgerTok",
            insight: "Current trending sound has 2.3M uses. Early adopters seeing 5x normal engagement.",
            score: 88,
            image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600'
        }
    },
    facebook: {
        post: {
            caption: "🍔 FAMILY SPECIAL THIS WEEK 🍔\n\nBring the whole family! Kids eat free on Tuesdays.\n\nReservations: (555) 123-4567\n\n📍 123 Main Street, Your City",
            insight: "Facebook users respond best to family-oriented promotions. Posts with location get 2x more clicks.",
            score: 79,
            image: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600'
        },
        event: {
            caption: "🎉 LIVE MUSIC NIGHT - This Friday!\n\nJoin us for great food, drinks, and entertainment.\n\n🎸 Band starts at 7 PM\n📅 Save the date!",
            insight: "Event posts get shared 4x more than regular posts. Create event listing for automatic reminders.",
            score: 84,
            image: 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=600'
        }
    },
    youtube: {
        short: {
            caption: "The secret to our perfect medium-rare steak 🥩🔥\n\n#Shorts #Cooking #SteakTok #ChefTips",
            insight: "YouTube Shorts under 30 seconds performing best. Recipe tips getting high retention.",
            score: 86,
            image: 'https://images.unsplash.com/photo-1558030006-450675393462?w=600'
        },
        video: {
            caption: "FULL RECIPE: How We Make Our Signature Burger From Scratch\n\nIngredients in description! 🍔👨‍🍳",
            insight: "Long-form recipe videos averaging 8min watch time. Include timestamps in description.",
            score: 81,
            image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600'
        }
    },
    snapchat: {
        story: {
            caption: "Order now through the link! Fresh out the oven 🔥",
            insight: "Snapchat users prefer authentic, unpolished content. Stories with 'right now' urgency perform best.",
            score: 77,
            image: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600'
        },
        spotlight: {
            caption: "Watch us make 100 burgers in 10 minutes ⚡🍔",
            insight: "Spotlight trending: fast-paced, impressive cooking feats. Time-lapse format recommended.",
            score: 83,
            image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600'
        }
    }
};

// ========================================
// CUSTOM CONTENT REQUEST
// ========================================

function startVoiceRequest() {
    // Simulate voice recording
    showToast('🎤 Voice recording... (Feature coming soon)');
    
    // In production, this would use Web Speech API
    // const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    // recognition.start();
}

function generateCustomContent() {
    const input = document.getElementById('customContentInput');
    const request = input.value.trim();
    
    if (!request) {
        showToast('⚠️ Please enter a content request');
        return;
    }
    
    showToast('✨ Generating custom content based on your request...');
    
    // Simulate AI processing delay
    setTimeout(() => {
        // Analyze request to determine platform
        let platform = 'instagram'; // default
        if (request.toLowerCase().includes('tiktok')) platform = 'tiktok';
        else if (request.toLowerCase().includes('facebook')) platform = 'facebook';
        else if (request.toLowerCase().includes('youtube')) platform = 'youtube';
        else if (request.toLowerCase().includes('snapchat')) platform = 'snapchat';
        
        // Generate content with custom request context
        generatePlatformContent(platform, 'post');
        
        // Clear input
        input.value = '';
    }, 1500);
}

// ========================================
// CONTENT GENERATION
// ========================================

let currentPlatform = null;
let currentContentType = null;

// New function for platform-specific content generation
function generatePlatformContent(platform, type) {
    currentPlatform = platform;
    currentContentType = type;
    
    const content = contentExamples[platform][type];
    
    // Error handling: Check if content exists
    if (!content) {
        console.error(`Invalid platform/type: ${platform}/${type}`);
        showToast('❌ Content not available');
        return;
    }
    
    const platformEmojis = {
        instagram: '📷',
        tiktok: '🎵',
        snapchat: '👻',
        facebook: '📘',
        youtube: '▶️'
    };
    
    // Update modal content with type information
    const typeLabel = type.charAt(0).toUpperCase() + type.slice(1);
    document.getElementById('modalTitle').textContent = 
        `${platformEmojis[platform]} ${platform.toUpperCase()} - ${typeLabel}`;
    
    document.querySelector('.preview-image img').src = content.image;
    document.querySelector('.preview-caption p').textContent = content.caption;
    document.getElementById('modalInsight').textContent = content.insight;
    document.getElementById('modalScore').textContent = content.score + '%';
    
    // Show modal
    openContentModal();
    
    showToast(`✨ ${platform.toUpperCase()} ${typeLabel} generated! CLICK 1 complete.`);
}

function generateContent(platform) {
    currentPlatform = platform;
    currentContentType = 'post'; // default type
    const content = contentExamples[platform];
    
    // Error handling: Check if platform exists
    if (!content) {
        console.error(`Invalid platform: ${platform}`);
        showToast('❌ Platform not supported');
        return;
    }
    
    // Use the first available content type or 'post' default
    const contentData = content.post || content[Object.keys(content)[0]];
    
    const platformEmojis = {
        instagram: '📷',
        tiktok: '🎵',
        snapchat: '👻',
        facebook: '📘',
        youtube: '▶️'
    };
    
    // Update modal content
    document.getElementById('modalTitle').textContent = 
        `${platformEmojis[platform]} ${platform.toUpperCase()} - Content Preview`;
    
    document.querySelector('.preview-image img').src = contentData.image;
    document.querySelector('.preview-caption p').textContent = contentData.caption;
    document.getElementById('modalInsight').textContent = contentData.insight;
    document.getElementById('modalScore').textContent = contentData.score + '%';
    
    // Show modal
    openContentModal();
    
    // Mark platform as having content ready
    const btn = document.querySelector(`.platform-btn[data-platform="${platform}"]`);
    if (btn) {
        btn.classList.add('has-content');
        const badge = btn.querySelector('.new-content-badge');
        if (badge) {
            badge.style.display = 'block';
            badge.textContent = 'READY';
        }
    }
    
    showToast('✨ Content generated! Click 1 of 3 complete.');
}

// ========================================
// MODAL CONTROLS
// ========================================

function openContentModal() {
    const modal = document.getElementById('contentModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeContentModal() {
    const modal = document.getElementById('contentModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

function approveAndPost() {
    // CLICK 2 - Copy caption and open platform
    const caption = document.querySelector('.preview-caption p').textContent;
    
    // Copy to clipboard with fallback for browsers that don't support Clipboard API
    if (navigator.clipboard && navigator.clipboard.writeText) {
        // Modern clipboard API (requires HTTPS in production)
        navigator.clipboard.writeText(caption).then(() => {
            showToast('✅ Caption copied to clipboard!');
            openPlatformAndUpdateStats();
        }).catch(err => {
            console.error('Clipboard API failed:', err);
            fallbackCopyToClipboard(caption);
        });
    } else {
        // Fallback for older browsers or non-HTTPS contexts
        fallbackCopyToClipboard(caption);
    }
}

// Fallback copy method for browsers without Clipboard API
function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-9999px';
    document.body.appendChild(textArea);
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showToast('✅ Caption copied to clipboard!');
            openPlatformAndUpdateStats();
        } else {
            showToast('⚠️ Please copy the caption manually.');
        }
    } catch (err) {
        console.error('Fallback copy failed:', err);
        showToast('⚠️ Please copy the caption manually.');
    } finally {
        document.body.removeChild(textArea);
    }
}

// Helper function to open platform and update stats
function openPlatformAndUpdateStats() {
    // Open social media platform
    const platformUrls = {
        instagram: 'https://www.instagram.com',
        tiktok: 'https://www.tiktok.com/upload',
        facebook: 'https://www.facebook.com',
        youtube: 'https://studio.youtube.com',
        snapchat: 'https://www.snapchat.com'
    };
    
    if (currentPlatform && platformUrls[currentPlatform]) {
        setTimeout(() => {
            window.open(platformUrls[currentPlatform], '_blank');
            showToast(`🚀 Opening ${currentPlatform.toUpperCase()}... Paste and post!`);
        }, 1000);
    }
    
    closeContentModal();
    
    // Update stats
    const contentPosted = document.getElementById('contentPosted');
    if (contentPosted) {
        const current = parseInt(contentPosted.textContent);
        contentPosted.textContent = current + 1;
    }
}

function regenerateContent() {
    // CLICK 3 - Generate new version
    showToast('↻ Regenerating with new angle...');
    closeContentModal();
    
    // Simulate regeneration delay
    setTimeout(() => {
        if (currentPlatform && currentContentType) {
            generatePlatformContent(currentPlatform, currentContentType);
            showToast('✨ New content variation generated!');
        } else if (currentPlatform) {
            generateContent(currentPlatform);
            showToast('✨ New content variation generated!');
        }
    }, 1000);
}

// ========================================
// TOAST NOTIFICATIONS
// ========================================

function showToast(message) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    
    if (toast && toastMessage) {
        toastMessage.textContent = message;
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}

// ========================================
// DASHBOARD INITIALIZATION
// ========================================

function initDashboard() {
    // Populate initial data
    populateCommunications();
    populateOrders();
    populateTimers();
    startCarousel();
    
    // Add live timer for phone agent panel
    const liveTimer = document.querySelector('.live-timer');
    if (liveTimer) {
        let seconds = 0;
        setInterval(() => {
            seconds++;
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            liveTimer.textContent = String(mins).padStart(2, '0') + ':' + String(secs).padStart(2, '0');
        }, 1000);
    }
    
    // Simulate stats updates
    const STAT_UPDATE_PROBABILITY = 0.7; // 30% chance of update per interval
    const STAT_UPDATE_INTERVAL = 30000; // Update check every 30 seconds
    
    setInterval(() => {
        const callsHandled = document.getElementById('callsHandled');
        if (callsHandled) {
            const current = parseInt(callsHandled.textContent);
            if (Math.random() > STAT_UPDATE_PROBABILITY) {
                callsHandled.textContent = current + 1;
            }
        }
    }, STAT_UPDATE_INTERVAL);
    
    console.log('🦊 FIFOX Dashboard initialized successfully!');
}

// ========================================
// KEYBOARD SHORTCUTS
// ========================================

document.addEventListener('keydown', function(e) {
    // Escape to close modal
    if (e.key === 'Escape') {
        closeContentModal();
    }
    
    // Alt + 1-7 for quick navigation
    if (e.altKey) {
        const panels = ['overview', 'command-center', 'phone-agent', 'content-factory', 'social-hub'];
        const num = parseInt(e.key);
        if (num >= 1 && num <= panels.length) {
            switchPanel(panels[num - 1]);
        }
    }
});

// ========================================
// WINDOW CONTROLS
// ========================================

// Close sidebar on outside click (mobile)
document.addEventListener('click', function(e) {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    
    if (window.innerWidth <= 768) {
        if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    }
});

// Handle window resize
let resizeTimeout;
window.addEventListener('resize', function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        // Reset sidebar state on desktop
        if (window.innerWidth > 768) {
            document.getElementById('sidebar').classList.remove('active');
        }
    }, 250);
});

// ========================================
// EXPORT FUNCTIONS FOR HTML ONCLICK
// ========================================

window.switchPanel = switchPanel;
window.generateContent = generateContent;
window.generatePlatformContent = generatePlatformContent;
window.startVoiceRequest = startVoiceRequest;
window.generateCustomContent = generateCustomContent;
window.closeContentModal = closeContentModal;
window.approveAndPost = approveAndPost;
window.regenerateContent = regenerateContent;
window.randomMenuItem = randomMenuItem;
window.handleImageUpload = handleImageUpload;
window.showToast = showToast;
