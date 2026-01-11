"""
Database models for FIFOX Backend
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Order(db.Model):
    """Order model for restaurant orders"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(100))
    customer_phone = db.Column(db.String(20))
    customer_address = db.Column(db.String(200))
    items = db.Column(db.Text)  # JSON string of order items
    total_amount = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')  # pending, preparing, ready, delivery, completed
    order_type = db.Column(db.String(20))  # delivery, pickup, dine-in
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    def to_dict(self):
        """Convert order to dictionary"""
        import json
        return {
            'id': self.id,
            'order_id': self.order_id,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_address': self.customer_address,
            'items': json.loads(self.items) if self.items else [],
            'total_amount': self.total_amount,
            'status': self.status,
            'order_type': self.order_type,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'notes': self.notes
        }


class Timer(db.Model):
    """Kitchen timer model"""
    __tablename__ = 'timers'
    
    id = db.Column(db.Integer, primary_key=True)
    timer_id = db.Column(db.String(50), unique=True, nullable=False)
    order_id = db.Column(db.String(50), nullable=False)
    dish_name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer)  # Duration in seconds
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        """Convert timer to dictionary"""
        elapsed = 0
        remaining = self.duration
        
        if self.started_at and self.is_active:
            elapsed = int((datetime.utcnow() - self.started_at).total_seconds())
            remaining = max(0, self.duration - elapsed)
        
        return {
            'id': self.id,
            'timer_id': self.timer_id,
            'order_id': self.order_id,
            'dish_name': self.dish_name,
            'duration': self.duration,
            'elapsed': elapsed,
            'remaining': remaining,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'is_active': self.is_active
        }


class Content(db.Model):
    """Generated content model"""
    __tablename__ = 'content'
    
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.String(50), unique=True, nullable=False)
    platform = db.Column(db.String(20), nullable=False)  # instagram, tiktok, facebook, youtube, snapchat
    content_type = db.Column(db.String(20))  # post, story, reel, video, etc.
    caption = db.Column(db.Text)
    hashtags = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))
    status = db.Column(db.String(20), default='draft')  # draft, approved, posted
    viral_score = db.Column(db.Integer)
    dara_insight = db.Column(db.Text)  # Competitive analysis insight
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posted_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert content to dictionary"""
        return {
            'id': self.id,
            'content_id': self.content_id,
            'platform': self.platform,
            'content_type': self.content_type,
            'caption': self.caption,
            'hashtags': self.hashtags,
            'image_url': self.image_url,
            'video_url': self.video_url,
            'status': self.status,
            'viral_score': self.viral_score,
            'dara_insight': self.dara_insight,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'posted_at': self.posted_at.isoformat() if self.posted_at else None
        }


class Settings(db.Model):
    """Settings model for application configuration"""
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert setting to dictionary"""
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'description': self.description,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AgentStatus(db.Model):
    """AI Agent status model"""
    __tablename__ = 'agent_status'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_name = db.Column(db.String(50), unique=True, nullable=False)  # MARA, VERA, LARA, etc.
    status = db.Column(db.String(20), default='active')  # active, idle, paused, error
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    calls_handled = db.Column(db.Integer, default=0)
    success_rate = db.Column(db.Float, default=100.0)
    agent_metadata = db.Column(db.Text)  # JSON string for additional agent-specific data
    
    def to_dict(self):
        """Convert agent status to dictionary"""
        import json
        return {
            'id': self.id,
            'agent_name': self.agent_name,
            'status': self.status,
            'last_active': self.last_active.isoformat() if self.last_active else None,
            'calls_handled': self.calls_handled,
            'success_rate': self.success_rate,
            'metadata': json.loads(self.agent_metadata) if self.agent_metadata else {}
        }
