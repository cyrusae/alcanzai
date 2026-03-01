#!/bin/bash
# Quick start script for alcanzai development setup
# Run this once to get everything ready

set -e  # Exit on any error

echo "🚀 alcanzai Development Setup"
echo "=============================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if uv is installed
if ! command -v uv &> /dev/null; then
  echo "📦 Installing uv (Python package manager)..."
  curl https://astral.sh/uv/install.sh | sh
  echo ""
fi

# Install dependencies
echo -e "${BLUE}📚 Installing dependencies...${NC}"
uv sync --all-extras
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Set up pre-commit hooks
echo -e "${BLUE}📝 Setting up git pre-commit hooks...${NC}"
pre-commit install
echo -e "${GREEN}✓ Pre-commit hooks configured${NC}"
echo ""

# Create necessary directories
echo -e "${BLUE}📁 Creating vault directories...${NC}"
mkdir -p vault/_meta vault/Papers vault/Articles vault/PDFs
echo -e "${GREEN}✓ Vault directories created${NC}"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
  echo -e "${YELLOW}⚠️  Creating .env file...${NC}"
  cat > .env << 'EOF'
# API Configuration
ANTHROPIC_API_KEY=sk-ant-YOUR_API_KEY_HERE

# GROBID Configuration (Docker)
GROBID_URL=http://localhost:8070

# Vault Configuration
VAULT_PATH=./vault
EOF
  echo -e "${YELLOW}⚠️  Please edit .env and add your ANTHROPIC_API_KEY${NC}"
  echo ""
fi

# Start GROBID
echo -e "${BLUE}🐳 Starting GROBID service...${NC}"
if command -v docker-compose &> /dev/null; then
  docker-compose up -d grobid 2>/dev/null || true
  echo -e "${YELLOW}⏳ Waiting for GROBID to start (30 seconds)...${NC}"
  sleep 3  # Quick start check
  max_attempts=30
  attempt=0
  while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:8070/api/isalive > /dev/null 2>&1; then
      echo -e "${GREEN}✓ GROBID is running${NC}"
      break
    fi
    attempt=$((attempt + 1))
    sleep 1
  done
  if [ $attempt -eq $max_attempts ]; then
    echo -e "${YELLOW}⚠️  GROBID is still starting. Wait a bit longer or check: docker-compose logs grobid${NC}"
  fi
else
  echo -e "${YELLOW}⚠️  Docker Compose not found. Install it or run: docker-compose up -d grobid${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${BLUE}🔧 Virtual environment created at: .venv${NC}"
echo "Activate it with: source .venv/bin/activate"
echo ""

# Summary
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Setup complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your ANTHROPIC_API_KEY"
echo "  2. Activate venv: source .venv/bin/activate"
echo "  3. Validate setup: alcanzai validate"
echo "  4. Run tests: pytest tests/ -m 'not integration'"
echo "  5. Try importing: alcanzai ingest 1706.03762"
echo ""
echo "For detailed info, see: DEVELOPER.md"
echo ""
