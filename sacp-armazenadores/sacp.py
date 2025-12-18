import rpyc
from rpyc.utils.server import ThreadPoolServer
import pymongo
import sys
import os
from datetime import datetime

# Configuração MongoDB
MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
MONGODB_PORT = int(os.getenv('MONGODB_PORT', 27017))
MONGODB_USER = os.getenv('MONGODB_USER', 'admin')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'admin123')
MONGODB_DB = os.getenv('MONGODB_DB', 'formula1_db')

# Conexão MongoDB
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
    
    def exposed_get_eventos(self, filtro=None):
        try:
            if filtro is None:
                filtro = {}
            
            eventos = list(eventos_collection.find(filtro, {'_id': 0}).limit(100))
            print(f"[SACP] {len(eventos)} eventos recuperados")
            return eventos
        except Exception as e:
            print(f"[SACP] Erro ao recuperar eventos: {e}")
            return []
    
    def exposed_get_eventos_por_carro(self, carro_id):
        try:
            eventos = list(eventos_collection.find(
                {'carroId': carro_id},
                {'_id': 0}
            ).sort('timestamp', -1))
            print(f"[SACP] {len(eventos)} eventos do carro {carro_id} recuperados")
            return eventos
        except Exception as e:
            print(f"[SACP] Erro ao recuperar eventos do carro: {e}")
            return []
    
    def exposed_get_eventos_por_ponto(self, ponto_id):
        try:
            eventos = list(eventos_collection.find(
                {'pontoId': ponto_id},
                {'_id': 0}
            ).sort('timestamp', -1).limit(50))
            print(f"[SACP] {len(eventos)} eventos do ponto {ponto_id} recuperados")
            return eventos
        except Exception as e:
            print(f"[SACP] Erro ao recuperar eventos do ponto: {e}")
            return []
    
    def exposed_clear_eventos(self):
        try:
            result = eventos_collection.delete_many({})
            print(f"[SACP] {result.deleted_count} eventos deletados")
            return {
                'success': True,
                'deleted': result.deleted_count
            }
        except Exception as e:
            print(f"[SACP] Erro ao limpar eventos: {e}")
            return {
                'success': False,
                'message': str(e)
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
