"""
Kitchen timer API endpoints
"""
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import uuid

from models import db, Timer
from services.timer_service import TimerService

bp = Blueprint('timers', __name__)
timer_service = TimerService()


@bp.route('', methods=['GET'])
def get_timers():
    """Get all active timers"""
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    
    query = Timer.query
    
    if active_only:
        query = query.filter_by(is_active=True)
    
    timers = query.order_by(Timer.started_at.desc()).all()
    
    return jsonify([timer.to_dict() for timer in timers])


@bp.route('/<timer_id>', methods=['GET'])
def get_timer(timer_id):
    """Get a specific timer"""
    timer = Timer.query.filter_by(timer_id=timer_id).first()
    
    if not timer:
        return jsonify({'error': 'Timer not found'}), 404
    
    return jsonify(timer.to_dict())


@bp.route('', methods=['POST'])
def create_timer():
    """Start a new kitchen timer"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    order_id = data.get('order_id')
    dish_name = data.get('dish_name')
    duration = data.get('duration')  # Duration in seconds
    
    if not all([order_id, dish_name, duration]):
        return jsonify({'error': 'order_id, dish_name, and duration are required'}), 400
    
    try:
        # Generate timer ID
        timer_id = f"TMR-{uuid.uuid4().hex[:8].upper()}"
        
        # Create new timer
        timer = Timer(
            timer_id=timer_id,
            order_id=order_id,
            dish_name=dish_name,
            duration=duration,
            started_at=datetime.utcnow(),
            is_active=True
        )
        
        db.session.add(timer)
        db.session.commit()
        
        # Start timer service tracking
        timer_service.start_timer(timer_id, duration, current_app.socketio)
        
        # Emit WebSocket event
        try:
            current_app.socketio.emit('timer_started', timer.to_dict())
        except Exception as e:
            current_app.logger.warning(f"Failed to emit timer_started event: {e}")
        
        return jsonify(timer.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating timer: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<timer_id>', methods=['PUT'])
def update_timer(timer_id):
    """Update a timer"""
    timer = Timer.query.filter_by(timer_id=timer_id).first()
    
    if not timer:
        return jsonify({'error': 'Timer not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'is_active' in data:
            timer.is_active = data['is_active']
            if not data['is_active']:
                timer.completed_at = datetime.utcnow()
                timer_service.stop_timer(timer_id)
        
        db.session.commit()
        
        # Emit WebSocket event
        try:
            current_app.socketio.emit('timer_update', timer.to_dict())
        except Exception as e:
            current_app.logger.warning(f"Failed to emit timer_update event: {e}")
        
        return jsonify(timer.to_dict())
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating timer: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<timer_id>', methods=['DELETE'])
def delete_timer(timer_id):
    """Complete/remove a timer"""
    timer = Timer.query.filter_by(timer_id=timer_id).first()
    
    if not timer:
        return jsonify({'error': 'Timer not found'}), 404
    
    try:
        # Stop timer service tracking
        timer_service.stop_timer(timer_id)
        
        # Mark as completed instead of deleting
        timer.is_active = False
        timer.completed_at = datetime.utcnow()
        db.session.commit()
        
        # Emit WebSocket event
        try:
            current_app.socketio.emit('timer_completed', timer.to_dict())
        except Exception as e:
            current_app.logger.warning(f"Failed to emit timer_completed event: {e}")
        
        return jsonify({'message': 'Timer completed successfully'})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error completing timer: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/bulk', methods=['POST'])
def create_bulk_timers():
    """Create multiple timers for an order"""
    data = request.get_json()
    
    if not data or 'timers' not in data:
        return jsonify({'error': 'No timers data provided'}), 400
    
    created_timers = []
    
    try:
        for timer_data in data['timers']:
            timer_id = f"TMR-{uuid.uuid4().hex[:8].upper()}"
            
            timer = Timer(
                timer_id=timer_id,
                order_id=timer_data['order_id'],
                dish_name=timer_data['dish_name'],
                duration=timer_data['duration'],
                started_at=datetime.utcnow(),
                is_active=True
            )
            
            db.session.add(timer)
            created_timers.append(timer)
            
            # Start timer service tracking
            timer_service.start_timer(timer_id, timer_data['duration'], current_app.socketio)
        
        db.session.commit()
        
        return jsonify([timer.to_dict() for timer in created_timers]), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating bulk timers: {e}")
        return jsonify({'error': str(e)}), 500
