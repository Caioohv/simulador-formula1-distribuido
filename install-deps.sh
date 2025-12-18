#!/bin/bash

echo "Instalando dependências do Dashboard F1..."
cd svcp-dashboard && npm install

echo ""
echo "Instalando dependências do Simulador..."
cd ../simulador-pista && npm install

echo ""
echo "Instalando dependências Python (SCCP)..."
cd ../sccp-receptores && pip install -r requirements.txt

echo ""
echo "Instalando dependências Python (SACP)..."
cd ../sacp-armazenadores && pip install -r requirements.txt

echo ""
echo "Todas as dependências foram instaladas com sucesso!"
echo ""
echo "Para iniciar o sistema completo, execute:"
echo "docker-compose -f docker-compose.full.yml up --build"
