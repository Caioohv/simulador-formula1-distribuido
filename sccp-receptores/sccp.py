import paho.mqtt.client as mqtt
import json
import sys
import time

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
        print(f"[SCCP-{ponto_id}] Recebido evento:")
        print(f"  Carro: {evento['nome']} (ID: {evento['carroId']}) - {evento['equipe']}")
        print(f"  Ponto: {evento['pontoNome']} (ID: {evento['pontoId']})")
        print(f"  Distância: {evento['distancia']}km | Velocidade: {evento['velocidade']:.2f}km/h")
        print(f"  Tempo: {evento['tempo']:.2f}s")
        print(f"  Pressão Pneus: {evento['pressaoPneus']}")
        print(f"  Timestamp: {evento['timestamp']}")
        print("-" * 60)
    except Exception as e:
        print(f"[SCCP-{ponto_id}] Erro ao processar mensagem: {e}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python sccp.py <ponto_id>")
        sys.exit(1)
    
    ponto_id = sys.argv[1]
    broker = "mqtt"
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