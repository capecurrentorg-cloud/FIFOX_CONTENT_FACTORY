"""
AI Agent status API endpoints
"""
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import json

from models import db, AgentStatus
from services.vapi_service import VapiService

bp = Blueprint('agents', __name__)
vapi_service = VapiService()


@bp.route('/status', methods=['GET'])
def get_all_agent_status():
    """Get status of all agents"""
    agents = AgentStatus.query.all()
    return jsonify([agent.to_dict() for agent in agents])


@bp.route('/<agent_name>/status', methods=['GET'])
def get_agent_status(agent_name):
    """Get status of a specific agent"""
    agent = AgentStatus.query.filter_by(agent_name=agent_name.upper()).first()
    
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    return jsonify(agent.to_dict())


@bp.route('/<agent_name>/status', methods=['PUT'])
def update_agent_status(agent_name):
    """Update agent status"""
    agent = AgentStatus.query.filter_by(agent_name=agent_name.upper()).first()
    
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'status' in data:
            agent.status = data['status']
        if 'calls_handled' in data:
            agent.calls_handled = data['calls_handled']
        if 'success_rate' in data:
            agent.success_rate = data['success_rate']
        if 'metadata' in data:
            agent.metadata = json.dumps(data['metadata'])
        
        agent.last_active = datetime.utcnow()
        db.session.commit()
        
        # Emit WebSocket event
        try:
            current_app.socketio.emit('agent_status_change', agent.to_dict())
        except Exception as e:
            current_app.logger.warning(f"Failed to emit agent_status_change event: {e}")
        
        return jsonify(agent.to_dict())
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating agent status: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/mara/call', methods=['POST'])
def simulate_mara_call():
    """Simulate an incoming call to MARA"""
    data = request.get_json() or {}
    
    try:
        # Simulate call processing
        result = vapi_service.simulate_incoming_call(
            customer_phone=data.get('phone', '555-123-4567'),
            customer_name=data.get('name', 'Test Customer')
        )
        
        # Update MARA's status
        mara = AgentStatus.query.filter_by(agent_name='MARA').first()
        if mara:
            mara.calls_handled += 1
            mara.last_active = datetime.utcnow()
            db.session.commit()
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"Error simulating MARA call: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/verification/stats', methods=['GET'])
def get_verification_stats():
    """Get order verification statistics"""
    try:
        stats = vapi_service.get_verification_stats()
        return jsonify(stats)
        
    except Exception as e:
        current_app.logger.error(f"Error getting verification stats: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/pause', methods=['POST'])
def pause_all_agents():
    """Pause all agents"""
    try:
        agents = AgentStatus.query.all()
        for agent in agents:
            agent.status = 'paused'
        
        db.session.commit()
        
        # Emit WebSocket event
        try:
            current_app.socketio.emit('agents_paused', {'message': 'All agents paused'})
        except Exception as e:
            current_app.logger.warning(f"Failed to emit agents_paused event: {e}")
        
        return jsonify({'message': 'All agents paused successfully'})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error pausing agents: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/resume', methods=['POST'])
def resume_all_agents():
    """Resume all agents"""
    try:
        agents = AgentStatus.query.all()
        for agent in agents:
            if agent.status == 'paused':
                agent.status = 'active'
        
        db.session.commit()
        
        # Emit WebSocket event
        try:
            current_app.socketio.emit('agents_resumed', {'message': 'All agents resumed'})
        except Exception as e:
            current_app.logger.warning(f"Failed to emit agents_resumed event: {e}")
        
        return jsonify({'message': 'All agents resumed successfully'})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error resuming agents: {e}")
        return jsonify({'error': str(e)}), 500
