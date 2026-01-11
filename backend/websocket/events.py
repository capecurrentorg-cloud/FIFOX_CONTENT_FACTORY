"""
WebSocket event handlers for real-time updates
"""
from flask import request, current_app
from flask_socketio import emit
import logging

logger = logging.getLogger(__name__)

# This will be set by app.py
_socketio = None


def init_events(socketio):
    """Initialize WebSocket events with socketio instance"""
    global _socketio
    _socketio = socketio
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        logger.info(f"Client connected: {request.sid}")
        emit('connection_response', {
            'status': 'connected',
            'message': 'Successfully connected to FIFOX Backend',
            'sid': request.sid
        })
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        logger.info(f"Client disconnected: {request.sid}")
    
    @socketio.on('ping')
    def handle_ping():
        """Handle ping for connection testing"""
        emit('pong', {'timestamp': 'pong'})
    
    @socketio.on('subscribe')
    def handle_subscribe(data):
        """Handle subscription to specific channels"""
        channel = data.get('channel')
        logger.info(f"Client {request.sid} subscribed to {channel}")
        emit('subscribed', {'channel': channel})
    
    @socketio.on('request_orders')
    def handle_request_orders():
        """Handle request for current orders"""
        from models import Order
        try:
            orders = Order.query.filter(Order.status != 'completed').order_by(Order.timestamp.desc()).all()
            emit('orders_update', [order.to_dict() for order in orders])
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            emit('error', {'message': 'Failed to fetch orders'})
    
    @socketio.on('request_timers')
    def handle_request_timers():
        """Handle request for active timers"""
        from models import Timer
        try:
            timers = Timer.query.filter_by(is_active=True).all()
            emit('timers_update', [timer.to_dict() for timer in timers])
        except Exception as e:
            logger.error(f"Error fetching timers: {e}")
            emit('error', {'message': 'Failed to fetch timers'})
    
    @socketio.on('request_agents')
    def handle_request_agents():
        """Handle request for agent statuses"""
        from models import AgentStatus
        try:
            agents = AgentStatus.query.all()
            emit('agents_update', [agent.to_dict() for agent in agents])
        except Exception as e:
            logger.error(f"Error fetching agents: {e}")
            emit('error', {'message': 'Failed to fetch agents'})
