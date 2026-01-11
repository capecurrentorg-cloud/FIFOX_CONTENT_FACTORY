// FIFOX Team Data and Logic

const FIFOX_TEAM = {
    mara: {
        name: "MARA",
        role: "Phone Agent",
        age: 28,
        background: "Latina",
        personality: "Warm, patient, detail-obsessed. Never rushes. Calm under pressure.",
        earColor: "#e67e22",
        themeColor: "#e67e22",
        description: "Handles all incoming phone orders with perfect accuracy. ORDER LOCK PROTOCOL ensures 99.9% order accuracy.",
        tasks: ["Taking phone orders", "Order verification", "Customer service"],
        status: "active"
    },
    rhea: {
        name: "RHEA",
        role: "Reservations",
        age: 31,
        background: "Greek-American",
        personality: "Gracious, remembers names, makes every guest feel like VIP. Elegant but approachable.",
        earColor: "#e91e63",
        themeColor: "#e91e63",
        description: "Books reservations, sends confirmations, follow-up thank yous, remembers anniversaries.",
        tasks: ["Reservation management", "Customer appreciation", "Birthday tracking"],
        status: "active"
    },
    vera: {
        name: "VERA",
        role: "Verification",
        age: 26,
        background: "Vietnamese-American",
        personality: "Sharp, analytical, catches every mistake. Protective of brand.",
        earColor: "#2ecc71",
        themeColor: "#2ecc71",
        description: "Quality gatekeeper for ALL content before posting. Responds to comments (approval-gated).",
        tasks: ["Content verification", "Quality control", "Brand protection"],
        status: "active"
    },
    dara: {
        name: "DARA",
        role: "Content Overseer",
        age: 34,
        background: "Nigerian-American",
        personality: "Strategic thinker, always watching competitors, suggests improvements. Natural leader.",
        earColor: "#3498db",
        themeColor: "#3498db",
        description: "Competitive intelligence, strategic insights, coordinates content team.",
        tasks: ["Competitor analysis", "Strategic planning", "Team coordination"],
        status: "active"
    },
    lara: {
        name: "LARA",
        role: "Kitchen Manager",
        age: 38,
        background: "Italian-American",
        personality: "Organized, efficient, no-nonsense but fair. Knows every ingredient cost.",
        earColor: "#e74c3c",
        themeColor: "#e74c3c",
        description: "Inventory management, delivery invoice scanning, AI menu generator.",
        tasks: ["Inventory tracking", "Invoice scanning", "Menu optimization"],
        status: "active"
    },
    tira: {
        name: "TIRA",
        role: "TikTok Copy",
        age: 22,
        background: "Korean-American",
        personality: "High energy, knows every trend, quick wit, Gen Z fluent. Never cringe.",
        earColor: "#e91e63",
        themeColor: "#000",
        description: "Writes TikTok captions, trends, scripts, concepts.",
        tasks: ["TikTok copywriting", "Trend analysis", "Script writing"],
        status: "idle"
    },
    tora: {
        name: "TORA",
        role: "TikTok Visual",
        age: 24,
        background: "Japanese-Brazilian",
        personality: "Creative storyteller, emotional hooks, makes you feel something.",
        earColor: "#00bcd4",
        themeColor: "#000",
        description: "Creates TikTok video concepts, storyboards, visual direction.",
        tasks: ["Video concepts", "Visual storytelling", "Creative direction"],
        status: "idle"
    },
    sara: {
        name: "SARA",
        role: "Snapchat Copy",
        age: 23,
        background: "Swedish-American",
        personality: "Spontaneous, authentic, shows real restaurant life. Makes followers feel like insiders.",
        earColor: "#ffeb3b",
        themeColor: "#ffeb3b",
        description: "Writes Snapchat stories, behind-scenes captions, quick snaps.",
        tasks: ["Snapchat stories", "Behind-the-scenes", "Authentic content"],
        status: "idle"
    },
    kara: {
        name: "KARA",
        role: "Snapchat Visual",
        age: 25,
        background: "Irish-American",
        personality: "Interactive, loves engaging followers, always asking questions.",
        earColor: "#ffc107",
        themeColor: "#ffc107",
        description: "Creates Snapchat filters, interactive content, polls, visual stories.",
        tasks: ["Interactive content", "Filters", "Engagement"],
        status: "idle"
    },
    ira: {
        name: "IRA",
        role: "Instagram Copy",
        age: 27,
        background: "Persian-American",
        personality: "Aesthetic obsessed, every shot is perfect, understands the algorithm.",
        earColor: "#9c27b0",
        themeColor: "#9c27b0",
        description: "Writes Instagram captions, reels scripts, hashtag strategy, grid perfection.",
        tasks: ["Instagram captions", "Hashtag strategy", "Aesthetic curation"],
        status: "idle"
    },
    gara: {
        name: "GARA",
        role: "Instagram Visual",
        age: 26,
        background: "Puerto Rican",
        personality: "Relatable, warm, 'best friend' energy. Makes followers feel connected.",
        earColor: "#ff6b9d",
        themeColor: "#ff6b9d",
        description: "Creates Instagram images, reels concepts, carousel layouts, stories.",
        tasks: ["Image creation", "Reels concepts", "Visual engagement"],
        status: "idle"
    },
    farah: {
        name: "FARAH",
        role: "Facebook",
        age: 32,
        background: "Egyptian-American",
        personality: "Professional, trustworthy, speaks to families and older customers.",
        earColor: "#1565c0",
        themeColor: "#1565c0",
        description: "Creates Facebook posts for community, events, older demographic.",
        tasks: ["Community posts", "Event creation", "Family content"],
        status: "idle"
    },
    bara: {
        name: "BARA",
        role: "YouTube",
        age: 29,
        background: "Indian-American",
        personality: "Patient storyteller, educational, shows the craft. Makes 10-minute videos feel like 2 minutes.",
        earColor: "#f44336",
        themeColor: "#f44336",
        description: "Creates YouTube long-form content, documentaries, recipes, vlogs.",
        tasks: ["Long-form content", "Educational videos", "Recipe tutorials"],
        status: "idle"
    }
};

// Platform to fox mapping
const PLATFORM_FOXES = {
    tiktok: { copywriter: 'tira', visual: 'tora' },
    snapchat: { copywriter: 'sara', visual: 'kara' },
    instagram: { copywriter: 'ira', visual: 'gara' },
    facebook: { copywriter: 'farah', visual: 'farah' },
    youtube: { copywriter: 'bara', visual: 'bara' }
};

// Generate fox avatar HTML
function generateFoxAvatar(foxKey, size = '') {
    const fox = FIFOX_TEAM[foxKey];
    const sizeClass = size ? `fox-avatar-${size}` : '';
    
    return `
        <div class="fox-avatar fox-${foxKey} ${sizeClass}">
            <div class="fox-face">
                <div class="fox-ears">
                    <div class="fox-ear"></div>
                    <div class="fox-ear"></div>
                </div>
                <div class="fox-features">
                    <div class="fox-eyes">
                        <div class="fox-eye"></div>
                        <div class="fox-eye"></div>
                    </div>
                    <div class="fox-snout">
                        <div class="fox-nose"></div>
                    </div>
                    <div class="fox-smile"></div>
                </div>
            </div>
        </div>
    `;
}

// Generate fox card HTML
function generateFoxCard(foxKey) {
    const fox = FIFOX_TEAM[foxKey];
    return `
        <div class="fox-card" data-fox="${foxKey}" onclick="showFoxDetails('${foxKey}')">
            ${generateFoxAvatar(foxKey)}
            <div class="fox-card-name">${fox.name}</div>
            <div class="fox-card-role">${fox.role}</div>
            <span class="fox-card-status status-${fox.status}">${fox.status.toUpperCase()}</span>
        </div>
    `;
}

// Generate fox creator badge
function generateCreatorBadge(foxKey) {
    const fox = FIFOX_TEAM[foxKey];
    return `
        <div class="fox-creator-badge">
            ${generateFoxAvatar(foxKey, 'small')}
            <span class="fox-creator-name">Created by ${fox.name}</span>
        </div>
    `;
}

// Generate full fox team roster
function generateFoxRoster(containerSelector) {
    const container = document.querySelector(containerSelector);
    if (!container) return;
    
    let html = '<div class="fox-team-grid">';
    for (const foxKey in FIFOX_TEAM) {
        html += generateFoxCard(foxKey);
    }
    html += '</div>';
    container.innerHTML = html;
}

// Show fox details modal
function showFoxDetails(foxKey) {
    const fox = FIFOX_TEAM[foxKey];
    const modal = document.getElementById('foxDetailsModal');
    if (!modal) return;
    
    document.getElementById('foxDetailAvatar').innerHTML = generateFoxAvatar(foxKey, 'large');
    document.getElementById('foxDetailName').textContent = fox.name;
    document.getElementById('foxDetailRole').textContent = fox.role;
    document.getElementById('foxDetailAge').textContent = `Age: ${fox.age}`;
    document.getElementById('foxDetailBackground').textContent = fox.background;
    document.getElementById('foxDetailPersonality').textContent = fox.personality;
    document.getElementById('foxDetailDescription').textContent = fox.description;
    
    let tasksHtml = '<ul style="list-style: none; padding: 0;">';
    fox.tasks.forEach(task => {
        tasksHtml += `<li style="padding: 5px 0;">✓ ${task}</li>`;
    });
    tasksHtml += '</ul>';
    document.getElementById('foxDetailTasks').innerHTML = tasksHtml;
    
    modal.style.display = 'flex';
}

// Close fox details modal
function closeFoxDetails() {
    const modal = document.getElementById('foxDetailsModal');
    if (modal) modal.style.display = 'none';
}

// Get foxes for a platform
function getFoxesForPlatform(platform) {
    return PLATFORM_FOXES[platform.toLowerCase()] || null;
}

// Assign fox to task
function assignFoxToTask(foxKey, task, orderNumber) {
    const fox = FIFOX_TEAM[foxKey];
    if (!fox) return false;
    
    fox.status = 'working';
    fox.currentTask = task;
    fox.currentOrder = orderNumber;
    
    // Update UI if fox card exists
    updateFoxCardStatus(foxKey);
    return true;
}

// Update fox card status in UI
function updateFoxCardStatus(foxKey) {
    const foxCard = document.querySelector(`[data-fox="${foxKey}"]`);
    if (!foxCard) return;
    
    const fox = FIFOX_TEAM[foxKey];
    const statusElement = foxCard.querySelector('.fox-card-status');
    if (statusElement) {
        statusElement.className = `fox-card-status status-${fox.status}`;
        statusElement.textContent = fox.status.toUpperCase();
    }
}

// Complete fox task
function completeFoxTask(foxKey) {
    const fox = FIFOX_TEAM[foxKey];
    if (!fox) return false;
    
    fox.status = 'idle';
    fox.currentTask = null;
    fox.currentOrder = null;
    
    updateFoxCardStatus(foxKey);
    return true;
}

// Get active foxes
function getActiveFoxes() {
    return Object.keys(FIFOX_TEAM).filter(key => FIFOX_TEAM[key].status === 'active');
}

// Get working foxes
function getWorkingFoxes() {
    return Object.keys(FIFOX_TEAM).filter(key => FIFOX_TEAM[key].status === 'working');
}

// Initialize fox system
function initializeFoxSystem() {
    console.log('🦊 FIFOX Team System Initialized');
    console.log(`Total Foxes: ${Object.keys(FIFOX_TEAM).length}`);
    console.log(`Active Foxes: ${getActiveFoxes().length}`);
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        FIFOX_TEAM,
        PLATFORM_FOXES,
        generateFoxAvatar,
        generateFoxCard,
        generateCreatorBadge,
        generateFoxRoster,
        showFoxDetails,
        closeFoxDetails,
        getFoxesForPlatform,
        assignFoxToTask,
        completeFoxTask,
        getActiveFoxes,
        getWorkingFoxes,
        initializeFoxSystem
    };
}
