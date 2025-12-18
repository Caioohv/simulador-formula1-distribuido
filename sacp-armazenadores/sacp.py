import rpyc
from rpyc.utils.server import ThreadPoolServer
import pymongo
import sys
import os
from datetime import datetime

MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
MONGODB_PORT = int(os.getenv('MONGODB_PORT', 27017))
MONGODB_USER = os.getenv('MONGODB_USER', 'admin')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'admin123')
MONGODB_DB = os.getenv('MONGODB_DB', 'formula1_db')

client = pymongo.MongoClient(
    f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/'
)
db = client[MONGODB_DB]
eventos_collection = db['eventos']

print(f"[SACP] Conectado ao MongoDB {MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB}")


class EventService(rpyc.SlaveService):
    
    def on_connect(self, conn):
        print("[SACP] Cliente RPC conectado")
    
    def on_disconnect(self, conn):
        print("[SACP] Cliente RPC desconectado")
    
    def exposed_save_event(self, evento):
        try:
            evento['_inserted_at'] = datetime.utcnow().isoformat()
          
            result = eventos_collection.insert_one(evento)
            
            print(f"[SACP] Evento salvo - Carro: {evento.get('nome', '??')} | "
                  f"Ponto: {evento.get('pontoId', '??')} | ID: {result.inserted_id}")
            
            return {
                'success': True,
                'message': 'Evento salvo com sucesso',
                'id': str(result.inserted_id)
            }
        except Exception as e:
            print(f"[SACP] Erro ao salvar evento: {e}")
            return {
                'success': False,
                'message': f'Erro ao salvar evento: {str(e)}'
            }

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 sacp.py <porta>")
        sys.exit(1)
    
    porta = int(sys.argv[1])
    
    print(f"[SACP] Iniciando servidor RPC na porta {porta}...")
    
    server = ThreadPoolServer(
        EventService,
        port=porta,
        protocol_config={'allow_public_attrs': True}
    )
    
    print(f"[SACP] Servidor RPC escutando na porta {porta}")
    server.start()


if __name__ == "__main__":
    main()
