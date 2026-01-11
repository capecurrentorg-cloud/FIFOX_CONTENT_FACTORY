#!/bin/bash
# FIFOX Backend Start Script

echo "🦊 Starting FIFOX Backend..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION found"

# Check if we're in the backend directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the backend/ directory."
    exit 1
fi

# Check if requirements are installed
echo ""
echo "📦 Checking dependencies..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Dependencies not installed. Installing now..."
    pip3 install -r requirements.txt
else
    echo "✅ Dependencies are installed"
fi

# Check if .env file exists
if [ ! -f "../.env" ]; then
    echo ""
    echo "⚠️  .env file not found. Copying .env.example..."
    cp ../.env.example ../.env
    echo "✅ Created .env file. Please edit it with your API keys if needed."
fi

echo ""
echo "🚀 Starting Flask backend..."
echo "   Dashboard: http://localhost:5000"
echo "   API: http://localhost:5000/api"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python3 app.py
