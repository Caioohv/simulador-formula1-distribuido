import { MongoClient } from 'mongodb'

const MONGODB_INSTANCES = [
  { host: 'mongodb-1', port: 27017, name: 'mongodb-1' },
  { host: 'mongodb-2', port: 27017, name: 'mongodb-2' },
  { host: 'mongodb-3', port: 27017, name: 'mongodb-3' }
]

const MONGODB_USER = 'admin'
const MONGODB_PASSWORD = 'admin123'
const MONGODB_DB = 'formula1_db'

export default defineEventHandler(async (event) => {
  const allEventos = []

  for (const instance of MONGODB_INSTANCES) {
    try {
      const uri = `mongodb://${MONGODB_USER}:${MONGODB_PASSWORD}@${instance.host}:${instance.port}/`
      const client = new MongoClient(uri)
      
      await client.connect()
      const db = client.db(MONGODB_DB)
      const collection = db.collection('eventos')
      
      const eventos = await collection.find({}).toArray()
      
      allEventos.push(...eventos.map(e => ({
        ...e,
        _id: e._id.toString(),
        _source: instance.name
      })))
      
      await client.close()
    } catch (error) {
      console.error(`Erro ao conectar ao ${instance.name}:`, error.message)
    }
  }

  return allEventos
})
