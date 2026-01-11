"""
Order management API endpoints
"""
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import json
import uuid

from models import db, Order

bp = Blueprint('orders', __name__)


@bp.route('', methods=['GET'])
def get_orders():
    """Get all orders with optional filtering"""
    status = request.args.get('status')
    limit = request.args.get('limit', type=int)
    
    query = Order.query
    
    if status:
        query = query.filter_by(status=status)
    
    # Order by timestamp descending (newest first)
    query = query.order_by(Order.timestamp.desc())
    
    if limit:
        query = query.limit(limit)
    
    orders = query.all()
    return jsonify([order.to_dict() for order in orders])


@bp.route('/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order by order_id"""
    order = Order.query.filter_by(order_id=order_id).first()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify(order.to_dict())


@bp.route('', methods=['POST'])
def create_order():
    """Create a new order"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Generate order ID if not provided
    order_id = data.get('order_id', f"ORD-{uuid.uuid4().hex[:8].upper()}")
    
    # Check if order already exists
    existing = Order.query.filter_by(order_id=order_id).first()
    if existing:
        return jsonify({'error': 'Order already exists'}), 400
    
    try:
        # Create new order
        order = Order(
            order_id=order_id,
            customer_name=data.get('customer_name'),
            customer_phone=data.get('customer_phone'),
            customer_address=data.get('customer_address'),
            items=json.dumps(data.get('items', [])),
            total_amount=data.get('total_amount', 0.0),
            status=data.get('status', 'pending'),
            order_type=data.get('order_type', 'pickup'),
            notes=data.get('notes'),
            timestamp=datetime.utcnow()
        )
        
        db.session.add(order)
        db.session.commit()
        
        # Emit WebSocket event for new order
        try:
            from flask import current_app
            current_app.socketio.emit('new_order', order.to_dict())
        except Exception as e:
            current_app.logger.warning(f"Failed to emit new_order event: {e}")
        
        return jsonify(order.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating order: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<order_id>', methods=['PUT'])
def update_order(order_id):
    """Update an existing order"""
    order = Order.query.filter_by(order_id=order_id).first()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    data = request.get_json()
    
    try:
        # Update order fields
        if 'customer_name' in data:
            order.customer_name = data['customer_name']
        if 'customer_phone' in data:
            order.customer_phone = data['customer_phone']
        if 'customer_address' in data:
            order.customer_address = data['customer_address']
        if 'items' in data:
            order.items = json.dumps(data['items'])
        if 'total_amount' in data:
            order.total_amount = data['total_amount']
        if 'status' in data:
            order.status = data['status']
            if data['status'] == 'completed':
                order.completed_at = datetime.utcnow()
        if 'notes' in data:
            order.notes = data['notes']
        
        db.session.commit()
        
        # Emit WebSocket event for order update
        try:
            current_app.socketio.emit('order_update', order.to_dict())
        except Exception as e:
            current_app.logger.warning(f"Failed to emit order_update event: {e}")
        
        return jsonify(order.to_dict())
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating order: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete an order"""
    order = Order.query.filter_by(order_id=order_id).first()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    try:
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting order: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get order statistics"""
    from sqlalchemy import func
    
    # Total orders today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_count = Order.query.filter(Order.timestamp >= today_start).count()
    
    # Active orders (not completed)
    active_count = Order.query.filter(Order.status != 'completed').count()
    
    # Orders by status
    status_counts = db.session.query(
        Order.status,
        func.count(Order.id)
    ).group_by(Order.status).all()
    
    # Total revenue today
    today_revenue = db.session.query(
        func.sum(Order.total_amount)
    ).filter(Order.timestamp >= today_start).scalar() or 0.0
    
    return jsonify({
        'today_count': today_count,
        'active_count': active_count,
        'today_revenue': round(today_revenue, 2),
        'status_counts': {status: count for status, count in status_counts}
    })
