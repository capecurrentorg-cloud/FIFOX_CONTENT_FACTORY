// FIFOX Order Verification System - Frontend Integration
// Connects command center UI to the 3-way verification backend

class OrderVerificationClient {
    constructor() {
        this.ws = null;
        this.orders = new Map();
        this.activeListeners = new Set();
        this.verificationResults = [];
    }
    
    /**
     * Initialize WebSocket connection to verification backend
     */
    connect(wsUrl = 'ws://localhost:8765') {
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            console.log('🔗 Connected to order verification system');
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleVerificationUpdate(data);
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        
        this.ws.onclose = () => {
            console.log('Disconnected from verification system');
            // Attempt reconnect after 5 seconds
            setTimeout(() => this.connect(wsUrl), 5000);
        };
    }
    
    /**
     * Handle updates from verification backend
     */
    handleVerificationUpdate(data) {
        switch (data.type) {
            case 'agent_report':
                this.handleAgentReport(data);
                break;
            case 'verification_result':
                this.handleVerificationResult(data);
                break;
            case 'kitchen_order':
                this.handleKitchenOrder(data);
                break;
            case 'timer_update':
                this.handleTimerUpdate(data);
                break;
        }
    }
    
    /**
     * Handle agent report (MARA, LLaMA, or Ollama)
     */
    handleAgentReport(data) {
        const { call_id, agent_name, order } = data;
        
        if (!this.orders.has(call_id)) {
            this.orders.set(call_id, {
                call_id,
                agents: {},
                status: 'listening'
            });
        }
        
        this.orders.get(call_id).agents[agent_name] = order;
        this.activeListeners.add(agent_name);
        
        console.log(`📥 ${agent_name.toUpperCase()} reported for call ${call_id}`);
        
        // Update UI
        this.updateListeningIndicator(call_id, agent_name);
    }
    
    /**
     * Handle verification result from VERA
     */
    handleVerificationResult(data) {
        const { call_id, approved, consensus_level, confidence, final_order, matching_agents, action } = data;
        
        this.verificationResults.push(data);
        
        if (this.orders.has(call_id)) {
            this.orders.get(call_id).verification = data;
            this.orders.get(call_id).status = approved ? 'approved' : 'rejected';
        }
        
        console.log(`🦊 VERA ${approved ? 'APPROVED' : 'REJECTED'} call ${call_id} (${confidence}% confidence)`);
        
        // Update UI with verification result
        this.displayVerificationResult(data);
        
        // Clear listeners for this call
        if (approved) {
            this.activeListeners.clear();
        }
    }
    
    /**
     * Handle kitchen order (sent to Toast)
     */
    handleKitchenOrder(data) {
        const { call_id, order_number, order, status, start_time } = data;
        
        console.log(`🍳 Order #${order_number} sent to kitchen`);
        
        // Add to command center orders list
        this.addOrderToCommandCenter({
            order_number,
            call_id,
            order,
            status,
            timestamp: start_time
        });
        
        // Start timer
        this.startOrderTimer(order_number, start_time);
    }
    
    /**
     * Handle timer updates
     */
    handleTimerUpdate(data) {
        const { order_number, elapsed_time, status } = data;
        this.updateTimerDisplay(order_number, elapsed_time, status);
    }
    
    /**
     * Update listening indicator in UI
     */
    updateListeningIndicator(call_id, agent_name) {
        const indicator = document.getElementById('listening-indicator');
        if (!indicator) return;
        
        const order = this.orders.get(call_id);
        const agentCount = Object.keys(order.agents).length;
        
        indicator.innerHTML = `
            <div class="listening-status">
                <h4>🎧 Listening to Call ${call_id.slice(-4)}</h4>
                <div class="agent-indicators">
                    <div class="agent-indicator ${order.agents.mara ? 'active' : ''}">
                        <div class="agent-avatar fox-mara">🦊</div>
                        <span>MARA</span>
                    </div>
                    <div class="agent-indicator ${order.agents.llama ? 'active' : ''}">
                        <div class="agent-avatar fox-llama">🦙</div>
                        <span>LLaMA</span>
                    </div>
                    <div class="agent-indicator ${order.agents.ollama ? 'active' : ''}">
                        <div class="agent-avatar fox-ollama">🦙</div>
                        <span>Ollama</span>
                    </div>
                </div>
                <p>${agentCount}/3 agents reported</p>
            </div>
        `;
    }
    
    /**
     * Display verification result
     */
    displayVerificationResult(result) {
        const { call_id, approved, consensus_level, confidence, matching_agents, discrepancies } = result;
        
        const modal = document.getElementById('verification-modal');
        if (!modal) return;
        
        const consensusColors = {
            'perfect': '#2ecc71',
            'majority': '#f39c12',
            'none': '#e74c3c'
        };
        
        modal.innerHTML = `
            <div class="modal-content verification-result">
                <div class="modal-header">
                    <h2>🦊 VERA's Verification Result</h2>
                    <button onclick="closeVerificationModal()" class="close-button">✕</button>
                </div>
                
                <div class="verification-status" style="background: ${consensusColors[consensus_level]}">
                    <h3>${approved ? '✅ APPROVED' : '❌ REJECTED'}</h3>
                    <p>${consensus_level.toUpperCase()} Consensus (${matching_agents.length}/3)</p>
                    <div class="confidence-score">${confidence}%</div>
                </div>
                
                <div class="matching-agents">
                    <h4>Matching Agents:</h4>
                    <div class="agent-list">
                        ${matching_agents.map(agent => `
                            <div class="agent-badge fox-${agent}">
                                ${generateFoxAvatar(agent, 'small')}
                                <span>${agent.toUpperCase()}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                ${discrepancies && discrepancies.length > 0 ? `
                    <div class="discrepancies">
                        <h4>⚠️ Discrepancies:</h4>
                        <ul>
                            ${discrepancies.map(d => `<li>${d}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${approved ? `
                    <div class="next-action">
                        <p>✓ Order sent to kitchen via Toast API</p>
                        <p>⏱️ Timer started</p>
                    </div>
                ` : `
                    <div class="next-action rejected">
                        <p>🔄 MARA will request clarification from customer</p>
                    </div>
                `}
            </div>
        `;
        
        modal.style.display = 'flex';
        
        // Auto-close after 5 seconds if approved
        if (approved) {
            setTimeout(() => {
                modal.style.display = 'none';
            }, 5000);
        }
    }
    
    /**
     * Add order to command center display
     */
    addOrderToCommandCenter(orderData) {
        const ordersList = document.getElementById('ordersList');
        if (!ordersList) return;
        
        const { order_number, order, status, timestamp } = orderData;
        const customer = order.customer_name || 'Unknown';
        const phone = order.customer_phone || '';
        
        const orderCard = document.createElement('div');
        orderCard.className = 'order-card';
        orderCard.id = `order-${order_number}`;
        
        const timeAgo = this.getTimeAgo(timestamp);
        
        orderCard.innerHTML = `
            <div class="order-header">
                <span class="order-number">#${order_number}</span>
                <span class="order-time">${timeAgo}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <div id="mara-avatar-${order_number}"></div>
                <div style="flex: 1;">
                    <div class="customer-name">Verified by VERA</div>
                    <div style="font-size: 12px; color: #2ecc71;">✓ 3-way consensus</div>
                </div>
            </div>
            <div class="customer-name">${customer} - ${phone}</div>
            <div class="order-items">
                ${order.items.map(item => {
                    const mods = item.modifiers && item.modifiers.length > 0 
                        ? ` (${item.modifiers.join(', ')})` 
                        : '';
                    return `• ${item.quantity}x ${item.name}${mods}`;
                }).join('<br>')}
            </div>
            <div style="display: flex; align-items: center; gap: 10px; margin-top: 10px;">
                <div id="lara-avatar-${order_number}"></div>
                <span class="order-status status-preparing">LARA: Preparing</span>
            </div>
        `;
        
        ordersList.insertBefore(orderCard, ordersList.firstChild);
        
        // Populate fox avatars
        setTimeout(() => {
            const maraContainer = document.getElementById(`mara-avatar-${order_number}`);
            const laraContainer = document.getElementById(`lara-avatar-${order_number}`);
            if (maraContainer && typeof generateFoxAvatar === 'function') {
                maraContainer.innerHTML = generateFoxAvatar('mara', 'small');
            }
            if (laraContainer && typeof generateFoxAvatar === 'function') {
                laraContainer.innerHTML = generateFoxAvatar('lara', 'small');
            }
        }, 100);
    }
    
    /**
     * Start order timer
     */
    startOrderTimer(order_number, start_time) {
        const timersList = document.getElementById('timersList');
        if (!timersList) return;
        
        const timerItem = document.createElement('div');
        timerItem.className = 'timer-item';
        timerItem.id = `timer-${order_number}`;
        
        timerItem.innerHTML = `
            <div class="timer-header">
                <span class="timer-order">Order #${order_number}</span>
                <span>🍽️ Cooking</span>
            </div>
            <div class="timer-time" id="timer-display-${order_number}">00:00</div>
        `;
        
        timersList.insertBefore(timerItem, timersList.firstChild);
        
        // Start timer countdown
        this.updateTimer(order_number, start_time);
    }
    
    /**
     * Update timer display
     */
    updateTimer(order_number, start_time) {
        const timerDisplay = document.getElementById(`timer-display-${order_number}`);
        if (!timerDisplay) return;
        
        const interval = setInterval(() => {
            const elapsed = Date.now() - new Date(start_time).getTime();
            const minutes = Math.floor(elapsed / 60000);
            const seconds = Math.floor((elapsed % 60000) / 1000);
            
            const display = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            timerDisplay.textContent = display;
            
            // Warning if over 15 minutes
            if (minutes >= 15) {
                const timerItem = document.getElementById(`timer-${order_number}`);
                if (timerItem) {
                    timerItem.classList.add('timer-warning');
                }
            }
        }, 1000);
        
        // Store interval for cleanup
        if (!this.timerIntervals) {
            this.timerIntervals = new Map();
        }
        this.timerIntervals.set(order_number, interval);
    }
    
    /**
     * Get human-readable time ago
     */
    getTimeAgo(timestamp) {
        const now = Date.now();
        const time = new Date(timestamp).getTime();
        const diff = now - time;
        
        const minutes = Math.floor(diff / 60000);
        if (minutes < 1) return 'just now';
        if (minutes === 1) return '1 min ago';
        if (minutes < 60) return `${minutes} min ago`;
        
        const hours = Math.floor(minutes / 60);
        if (hours === 1) return '1 hour ago';
        return `${hours} hours ago`;
    }
    
    /**
     * Get verification statistics
     */
    getStats() {
        const stats = {
            total_orders: this.verificationResults.length,
            perfect_match: 0,
            majority_match: 0,
            no_consensus: 0,
            accuracy_rate: 0
        };
        
        this.verificationResults.forEach(result => {
            if (result.consensus_level === 'perfect') {
                stats.perfect_match++;
            } else if (result.consensus_level === 'majority') {
                stats.majority_match++;
            } else {
                stats.no_consensus++;
            }
        });
        
        stats.accuracy_rate = stats.total_orders > 0 
            ? ((stats.perfect_match + stats.majority_match) / stats.total_orders * 100).toFixed(1)
            : 0;
        
        return stats;
    }
}

// Global instance
const verificationClient = new OrderVerificationClient();

// Helper function to close verification modal
function closeVerificationModal() {
    const modal = document.getElementById('verification-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Initialize on page load
if (typeof window !== 'undefined') {
    window.addEventListener('DOMContentLoaded', () => {
        // Add verification indicator to command center if it exists
        const dashboard = document.querySelector('.dashboard');
        if (dashboard) {
            // Add listening indicator
            const indicator = document.createElement('div');
            indicator.id = 'listening-indicator';
            indicator.className = 'listening-indicator';
            dashboard.appendChild(indicator);
            
            // Add verification modal
            const modal = document.createElement('div');
            modal.id = 'verification-modal';
            modal.className = 'modal';
            document.body.appendChild(modal);
            
            // Try to connect to verification backend
            // In development, this will fail gracefully
            try {
                verificationClient.connect();
            } catch (e) {
                console.log('Verification system not available (development mode)');
            }
        }
    });
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { OrderVerificationClient, verificationClient };
}
