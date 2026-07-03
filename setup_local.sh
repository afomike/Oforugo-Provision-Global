#!/bin/bash
# Local setup script for Oforugo Provision Global
set -e

echo "=== Oforugo Provision Global — Local Setup ==="

# 1. Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 is not installed. Install it from https://python.org"
    exit 1
fi
echo "✓ Python $(python3 --version)"

# 2. Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# 3. Activate and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# 4. Copy .env if not present
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "⚠️  .env file created from .env.example"
    echo "    Edit oforugo/.env and set your DATABASE_URL before running."
    echo ""
else
    echo "✓ .env file already exists"
fi

echo ""
echo "=== Setup complete ==="
echo ""
echo "Next steps:"
echo "  1. Edit .env with your PostgreSQL connection string"
echo "  2. Run the app:"
echo "     source venv/bin/activate"
echo "     python run.py"
echo ""
echo "The app will be available at: http://localhost:5000"
echo "Admin login: admin@oforugo.com / admin123"
