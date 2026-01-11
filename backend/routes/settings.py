"""
Settings management API endpoints
"""
from flask import Blueprint, request, jsonify, current_app

from models import db, Settings

bp = Blueprint('settings', __name__)


@bp.route('', methods=['GET'])
def get_settings():
    """Get all settings"""
    settings = Settings.query.all()
    return jsonify({setting.key: setting.value for setting in settings})


@bp.route('/<key>', methods=['GET'])
def get_setting(key):
    """Get a specific setting"""
    setting = Settings.query.filter_by(key=key).first()
    
    if not setting:
        return jsonify({'error': 'Setting not found'}), 404
    
    return jsonify(setting.to_dict())


@bp.route('', methods=['PUT'])
def update_settings():
    """Update multiple settings"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    updated = []
    
    try:
        for key, value in data.items():
            setting = Settings.query.filter_by(key=key).first()
            
            if setting:
                setting.value = str(value)
                updated.append(key)
            else:
                # Create new setting if it doesn't exist
                setting = Settings(key=key, value=str(value))
                db.session.add(setting)
                updated.append(key)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Settings updated successfully',
            'updated': updated
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating settings: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<key>', methods=['PUT'])
def update_setting(key):
    """Update a specific setting"""
    data = request.get_json()
    
    if not data or 'value' not in data:
        return jsonify({'error': 'Value is required'}), 400
    
    try:
        setting = Settings.query.filter_by(key=key).first()
        
        if not setting:
            # Create new setting
            setting = Settings(
                key=key,
                value=str(data['value']),
                description=data.get('description', '')
            )
            db.session.add(setting)
        else:
            setting.value = str(data['value'])
            if 'description' in data:
                setting.description = data['description']
        
        db.session.commit()
        
        return jsonify(setting.to_dict())
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating setting: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<key>', methods=['DELETE'])
def delete_setting(key):
    """Delete a setting"""
    setting = Settings.query.filter_by(key=key).first()
    
    if not setting:
        return jsonify({'error': 'Setting not found'}), 404
    
    try:
        db.session.delete(setting)
        db.session.commit()
        return jsonify({'message': 'Setting deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting setting: {e}")
        return jsonify({'error': str(e)}), 500
