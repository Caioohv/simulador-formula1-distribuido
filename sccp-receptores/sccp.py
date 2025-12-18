import paho.mqtt.client as mqtt
import json
import sys
import time
import rpyc

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
        # Velocidade vem em m/s — converte para km/h
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

        # Envia o evento para o servidor RPC (implementação mínima)
        send_event_rpc(evento)
    except Exception as e:
        print(f"[SCCP-{ponto_id}] Erro ao processar mensagem: {e}")

RPC_HOST = 'localhost'
RPC_PORT = 8000
_rpyc_conn = None

def _get_rpyc_root():
    """Retorna root do rpyc, conectando na primeira chamada. Retorna None se não conseguiu conectar."""
    global _rpyc_conn
    if _rpyc_conn is None:
        try:
            _rpyc_conn = rpyc.connect(RPC_HOST, RPC_PORT)
            print(f"[SCCP] Conectado ao servidor RPYC {RPC_HOST}:{RPC_PORT}")
        except Exception as e:
            print(f"[SCCP] Erro ao conectar ao RPYC: {e}")
            _rpyc_conn = None
    return _rpyc_conn.root if _rpyc_conn else None

def send_event_rpc(evento):
    """Envia o evento para o servidor RPC via rpyc (método remoto save_event).
    Implementação mínima: tenta conectar uma vez e chama o método remoto; apenas log de erro em falha.
    """
    try:
        root = _get_rpyc_root()
        if root is None:
            print(f"[SCCP-{evento.get('pontoId', '??')}] Conexão RPYC indisponível; evento não enviado")
            return
        root.save_event(evento)
        print(f"[SCCP-{evento.get('pontoId', '??')}] Evento enviado ao RPC via rpyc")
    except Exception as e:
        print(f"[SCCP-{evento.get('pontoId', '??')}] Erro ao enviar evento via rpyc: {e}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python sccp.py <ponto_id>")
        sys.exit(1)
    
    ponto_id = sys.argv[1]
    broker = "localhost"
    porta = 1883
    
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