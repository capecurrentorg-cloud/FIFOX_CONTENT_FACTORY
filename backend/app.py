"""
FIFOX Backend - Main Flask Application
Real-time order management, AI agent integration, and content generation
"""
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import logging
from datetime import datetime

from config import get_config
from models import db, Order, Timer, Content, Settings, AgentStatus

# Initialize Flask app
app = Flask(__name__, static_folder='..', static_url_path='')
app.config.from_object(get_config())

# Initialize extensions
CORS(app, origins=app.config['CORS_ORIGINS'])
socketio = SocketIO(app, cors_allowed_origins=app.config['SOCKETIO_CORS_ALLOWED_ORIGINS'], async_mode='eventlet')
db.init_app(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO if app.config['DEBUG'] else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def initialize_database():
    """Initialize database with tables and default data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        logger.info("Database tables created")
        
        # Initialize agent statuses if not exist
        agents = ['MARA', 'VERA', 'LARA', 'DARA', 'RHEA', 'TIRA', 'TORA', 'SARA', 'KARA', 'IRA', 'GARA', 'FARAH', 'BARA']
        for agent_name in agents:
            agent = AgentStatus.query.filter_by(agent_name=agent_name).first()
            if not agent:
                agent = AgentStatus(
                    agent_name=agent_name,
                    status='active',
                    last_active=datetime.utcnow()
                )
                db.session.add(agent)
        
        # Initialize default settings if not exist
        default_settings = [
            {'key': 'restaurant_name', 'value': 'FIFOX Restaurant', 'description': 'Restaurant name'},
            {'key': 'restaurant_phone', 'value': '(555) 123-4567', 'description': 'Restaurant phone number'},
            {'key': 'restaurant_address', 'value': '123 Main Street, Your City', 'description': 'Restaurant address'},
            {'key': 'auto_accept_orders', 'value': 'false', 'description': 'Automatically accept orders'},
            {'key': 'timer_notification_threshold', 'value': '180', 'description': 'Timer warning threshold in seconds'},
        ]
        
        for setting_data in default_settings:
            setting = Settings.query.filter_by(key=setting_data['key']).first()
            if not setting:
                setting = Settings(**setting_data)
                db.session.add(setting)
        
        db.session.commit()
        logger.info("Database initialized with default data")


# Import and register blueprints
from routes import orders, content, agents, timers, settings as settings_routes

app.register_blueprint(orders.bp, url_prefix='/api/orders')
app.register_blueprint(content.bp, url_prefix='/api/content')
app.register_blueprint(agents.bp, url_prefix='/api/agents')
app.register_blueprint(timers.bp, url_prefix='/api/timers')
app.register_blueprint(settings_routes.bp, url_prefix='/api/settings')

# Import and initialize WebSocket events
from websocket.events import init_events
init_events(socketio)

# Make socketio available to other modules
app.socketio = socketio


@app.route('/')
def index():
    """Serve the command center dashboard"""
    return send_from_directory(app.static_folder, 'command_center.html')


@app.route('/dashboard')
def dashboard():
    """Serve the command center dashboard (alias)"""
    return send_from_directory(app.static_folder, 'command_center.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Initialize database
    initialize_database()
    
    # Start the server
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting FIFOX Backend on port {port}")
    logger.info(f"Dashboard available at http://localhost:{port}/")
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )
