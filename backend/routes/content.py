"""
Content generation API endpoints
"""
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import uuid

from models import db, Content
from services.content_generator import ContentGenerator

bp = Blueprint('content', __name__)
content_generator = ContentGenerator()


@bp.route('/generate', methods=['POST'])
def generate_content():
    """Generate content for a specific platform"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    platform = data.get('platform')
    content_type = data.get('content_type', 'post')
    topic = data.get('topic', '')
    
    if not platform:
        return jsonify({'error': 'Platform is required'}), 400
    
    try:
        # Generate content using the content generator service
        generated = content_generator.generate_content(platform, content_type, topic)
        
        # Save to database
        content_id = f"CNT-{uuid.uuid4().hex[:8].upper()}"
        content = Content(
            content_id=content_id,
            platform=platform,
            content_type=content_type,
            caption=generated['caption'],
            hashtags=generated.get('hashtags', ''),
            image_url=generated.get('image_url', ''),
            video_url=generated.get('video_url', ''),
            status='draft',
            viral_score=generated.get('viral_score', 0),
            dara_insight=generated.get('dara_insight', ''),
            created_at=datetime.utcnow()
        )
        
        db.session.add(content)
        db.session.commit()
        
        # Emit WebSocket event
        try:
            current_app.socketio.emit('content_generated', content.to_dict())
        except Exception as e:
            current_app.logger.warning(f"Failed to emit content_generated event: {e}")
        
        return jsonify(content.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error generating content: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/custom', methods=['POST'])
def generate_custom_content():
    """Generate custom content from voice/text input"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    platform = data.get('platform')
    user_input = data.get('input', '')
    
    if not platform or not user_input:
        return jsonify({'error': 'Platform and input are required'}), 400
    
    try:
        # Generate custom content
        generated = content_generator.generate_custom_content(platform, user_input)
        
        # Save to database
        content_id = f"CNT-{uuid.uuid4().hex[:8].upper()}"
        content = Content(
            content_id=content_id,
            platform=platform,
            content_type='custom',
            caption=generated['caption'],
            hashtags=generated.get('hashtags', ''),
            image_url=generated.get('image_url', ''),
            status='draft',
            viral_score=generated.get('viral_score', 0),
            dara_insight=generated.get('dara_insight', ''),
            created_at=datetime.utcnow()
        )
        
        db.session.add(content)
        db.session.commit()
        
        return jsonify(content.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error generating custom content: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/recent', methods=['GET'])
def get_recent_content():
    """Get recently generated content"""
    limit = request.args.get('limit', 10, type=int)
    platform = request.args.get('platform')
    status = request.args.get('status')
    
    query = Content.query
    
    if platform:
        query = query.filter_by(platform=platform)
    if status:
        query = query.filter_by(status=status)
    
    content_list = query.order_by(Content.created_at.desc()).limit(limit).all()
    
    return jsonify([content.to_dict() for content in content_list])


@bp.route('/<content_id>/approve', methods=['POST'])
def approve_content(content_id):
    """Approve and prepare content for posting"""
    content = Content.query.filter_by(content_id=content_id).first()
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    try:
        content.status = 'approved'
        db.session.commit()
        
        return jsonify({
            'message': 'Content approved',
            'content': content.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error approving content: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<content_id>/post', methods=['POST'])
def mark_as_posted(content_id):
    """Mark content as posted"""
    content = Content.query.filter_by(content_id=content_id).first()
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    try:
        content.status = 'posted'
        content.posted_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Content marked as posted',
            'content': content.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error marking content as posted: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<content_id>', methods=['DELETE'])
def delete_content(content_id):
    """Delete content"""
    content = Content.query.filter_by(content_id=content_id).first()
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    try:
        db.session.delete(content)
        db.session.commit()
        return jsonify({'message': 'Content deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting content: {e}")
        return jsonify({'error': str(e)}), 500
