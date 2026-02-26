#!/bin/bash
set -e

echo "Setting up alcanzai development environment..."

pip install --upgrade pip setuptools wheel
pip install uv

uv sync --all-extras

echo "Installing git pre-commit hooks..."
pre-commit install

mkdir -p vault/_meta vault/Papers vault/Articles vault/PDFs

if [ ! -f .env ]; then
  cat > .env << ENVEOF
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
GROBID_URL=http://grobid:8070
VAULT_PATH=./vault
ENVEOF
  echo "Please edit .env and add your ANTHROPIC_API_KEY"
fi

echo "Starting GROBID service..."
docker-compose up -d grobid 2>/dev/null || true

echo "Waiting for GROBID..."
sleep 3
for i in {1..30}; do
  if curl -s http://localhost:8070/api/isalive > /dev/null; then
    echo "GROBID is ready!"
    break
  fi
  sleep 1
done

echo ""
echo "Development environment is ready!"
echo "Next: Edit .env and add your ANTHROPIC_API_KEY"
echo ""
