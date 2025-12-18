# Sistema Distribuído de Monitoramento F1

Sistema distribuído para monitoramento em tempo real de veículos de Fórmula 1, incluindo telemetria de pneus.

## Arquitetura

```
Simulador (24 carros) → MQTT Broker
                           ↓
            15 Receptores SCCP (pontos 1-15)
                           ↓
        3 Servidores RPC SACP (8001, 8002, 8003)
                           ↓
          3 Instâncias MongoDB (27017, 27018, 27019)
                           ↓
                  Dashboard Web (Nuxt.js)
```

## Componentes

### 1. Simulador de Pista (`simulador-pista/`)
- 24 carros publicando telemetria via MQTT
- Tópicos: `formula1/sensor-{1..15}`
- Dados: velocidade, pressão dos pneus, posição, etc.

### 2. Receptores SCCP (`sccp-receptores/`)
- 15 receptores (1 por ponto da pista)
- Recebem eventos MQTT e enviam para servidores RPC
- Pontos 1-5 → RPC 8001
- Pontos 6-10 → RPC 8002
- Pontos 11-15 → RPC 8003

### 3. Armazenadores SACP (`sacp-armazenadores/`)
- 3 servidores RPC em Python
- Salvam eventos em instâncias separadas do MongoDB
- Portas: 8001, 8002, 8003

### 4. Dashboard Web (`svcp-dashboard/`)
- Interface Nuxt.js
- Consulta as 3 instâncias MongoDB
- Visualização em tempo real da pressão dos pneus
- Filtros por equipe
- Sistema de cores por nível de pressão

## Executar o Sistema Completo

```bash
docker-compose -f docker-compose.full.yml up --build
```

Serviços disponíveis:
- MQTT Broker: `localhost:1883`
- MongoDB 1: `localhost:27017`
- MongoDB 2: `localhost:27018`
- MongoDB 3: `localhost:27019`
- RPC Server 1: `localhost:8001`
- RPC Server 2: `localhost:8002`
- RPC Server 3: `localhost:8003`
- Dashboard: `http://localhost:3000`

## Desenvolvimento Individual

### Simulador
```bash
cd simulador-pista
npm install
node index.mjs
```

### Receptores SCCP
```bash
cd sccp-receptores
pip install -r requirements.txt
python sccp.py <ponto_id>
```

### Servidores RPC SACP
```bash
cd sacp-armazenadores
pip install -r requirements.txt
python sacp.py <porta>
```

### Dashboard
```bash
cd svcp-dashboard
npm install
npm run dev
```

## Status dos Pneus

- **Verde** (50-40 PSI): OK
- **Amarelo** (40-30 PSI): Atenção
- **Vermelho** (30-20 PSI): Perigo
- **Vermelho piscando** (20-10 PSI): Crítico
- **Vermelho piscando + alerta** (<10 PSI): Emergência

## Tecnologias

- **MQTT**: Mosquitto
- **RPC**: RPyC (Python)
- **Banco de Dados**: MongoDB (3 instâncias)
- **Backend API**: Nuxt.js Server Routes
- **Frontend**: Nuxt.js + Vue 3 + Pinia
- **Containerização**: Docker + Docker Compose
