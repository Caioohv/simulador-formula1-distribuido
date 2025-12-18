# F1 Tire Monitoring Dashboard

Dashboard web para monitoramento em tempo real da pressão dos pneus dos carros de Fórmula 1.

## Características

- Monitoramento de 24 carros em tempo real
- Conexão com 3 instâncias MongoDB (dados distribuídos)
- Sistema de cores para status dos pneus:
  - Verde: 50-40 PSI (OK)
  - Amarelo: 40-30 PSI (Atenção)
  - Vermelho: 30-20 PSI (Perigo)
  - Vermelho piscando: 20-10 PSI (Crítico)
  - Vermelho piscando + alerta: <10 PSI (Emergência)
- Ordenação automática por menor pressão média
- Filtro por equipe com detalhes adicionais:
  - Último ponto da pista
  - Tempo desde última atualização
  - Velocidade atual
- Tema escuro monocromatico
- Atualização automática a cada 5 segundos

## Instalação

```bash
cd svcp-dashboard
npm install
```

## Executar em desenvolvimento

```bash
npm run dev
```

O dashboard estará disponível em: http://localhost:3000

## Build para produção

```bash
npm run build
npm run preview
```

## Configuração MongoDB

As 3 instâncias MongoDB devem estar rodando nas portas:
- mongodb-1: localhost:27017
- mongodb-2: localhost:27018
- mongodb-3: localhost:27019

Credenciais padrão:
- Usuário: admin
- Senha: admin123
- Database: formula1_db
