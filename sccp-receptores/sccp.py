import os
import paho.mqtt.client as mqtt
import json
import sys
import time
import rpyc

RPC_HOSTS = {8001: 'sacp-8001', 8002: 'sacp-8002', 8003: 'sacp-8003'}
RPC_HOST_FALLBACK = 'sacp-8001'
_rpyc_conn = None

def get_rpc_port(ponto_id):
    """Retorna a porta RPC baseado no ID do ponto"""
    ponto_num = int(ponto_id)
    if 1 <= ponto_num <= 5:
        return 8001
    elif 6 <= ponto_num <= 10:
        return 8002
    elif 11 <= ponto_num <= 15:
        return 8003
    else:
        return None

def on_connect(client, userdata, flags, rc):
    ponto_id = userdata['ponto_id']
    topico = f"formula1/sensor-{ponto_id}"
    print(f"[SCCP-{ponto_id}] Conectado ao broker MQTT (código: {rc})")
    print(f"[SCCP-{ponto_id}] Inscrito no tópico: {topico}")
    client.subscribe(topico)

def on_message(client, userdata, msg):
    ponto_id = userdata['ponto_id']
    try:
        evento = json.loads(msg.payload.decode())
        vel_mps = evento.get('velocidade', 0)
        vel_kmh = vel_mps * 3.6

        print(f"[SCCP-{ponto_id}] Recebido evento:")
        print(f"  Carro: {evento['nome']} (ID: {evento['carroId']}) - {evento['equipe']}")
        print(f"  Ponto: {evento['pontoNome']} (ID: {evento['pontoId']})")
        print(f"  Distância: {evento['distancia']:.2f}m | Velocidade: {vel_kmh:.2f}km/h ({vel_mps:.2f}m/s)")
        print(f"  Tempo: {evento['tempo']:.2f}s")
        print(f"  Pressão Pneus: {evento['pressaoPneus']}")
        print(f"  Timestamp: {evento['timestamp']}")
        print("-" * 60)

        send_event_rpc(ponto_id, evento)
    except Exception as e:
        print(f"[SCCP-{ponto_id}] Erro ao processar mensagem: {e}")

def _get_rpyc_root(ponto_id):
    global _rpyc_conn
    rpc_port = get_rpc_port(ponto_id)
    
    if rpc_port is None:
        print(f"[SCCP-{ponto_id}] ID do ponto inválido: {ponto_id}")
        return None
    
    rpc_host = RPC_HOSTS.get(rpc_port, RPC_HOST_FALLBACK)
    
    if _rpyc_conn is None:
        try:
            _rpyc_conn = rpyc.connect(rpc_host, rpc_port)
            print(f"[SCCP-{ponto_id}] Conectado ao servidor RPYC {rpc_host}:{rpc_port}")
        except Exception as e:
            print(f"[SCCP-{ponto_id}] Erro ao conectar ao RPYC {rpc_host}:{rpc_port}: {e}")
            _rpyc_conn = None
    return _rpyc_conn.root if _rpyc_conn else None

def send_event_rpc(ponto_id, evento):
    try:
        root = _get_rpyc_root(ponto_id)
        if root is None:
            print(f"[SCCP-{ponto_id}] Conexão RPYC indisponível; evento não enviado")
            return
        root.save_event(evento)
        print(f"[SCCP-{ponto_id}] Evento enviado ao RPC via rpyc")
    except Exception as e:
        print(f"[SCCP-{ponto_id}] Erro ao enviar evento via rpyc: {e}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 sccp.py <ponto_id>")
        sys.exit(1)
    
    ponto_id = sys.argv[1]
    broker = os.getenv("MQTT_HOST", "mqtt")
    porta = int(os.getenv("MQTT_PORT", "1883"))
    
    client = mqtt.Client(userdata={'ponto_id': ponto_id})
    client.on_connect = on_connect
    client.on_message = on_message
    
    print(f"[SCCP-{ponto_id}] Conectando ao broker {broker}:{porta}...")
    
    while True:
        try:
            client.connect(broker, porta, 60)
            client.loop_forever()
        except Exception as e:
            print(f"[SCCP-{ponto_id}] Erro de conexão: {e}. Tentando novamente em 5s...")
            time.sleep(5)

if __name__ == "__main__":
    main()