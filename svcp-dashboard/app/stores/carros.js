import { defineStore } from 'pinia'

export const useCarrosStore = defineStore('carros', {
  state: () => ({
    eventos: [],
    carrosData: new Map(),
    selectedTeam: null,
    loading: false,
    lastUpdate: null
  }),

  getters: {
    carrosOrdenados: (state) => {
      const carros = Array.from(state.carrosData.values())
      return carros.sort((a, b) => a.mediaPressao - b.mediaPressao)
    },

    carrosPorEquipe: (state) => {
      if (!state.selectedTeam) return state.carrosOrdenados
      return state.carrosOrdenados.filter(c => c.equipe === state.selectedTeam)
    },

    equipesUnicas: (state) => {
      const equipes = new Set(Array.from(state.carrosData.values()).map(c => c.equipe))
      return Array.from(equipes).sort()
    }
  },

  actions: {
    async fetchEventos() {
      this.loading = true
      try {
        const data = await $fetch('/api/eventos')
        // Converte objeto em array se necessário
        const eventos = Array.isArray(data) ? data : Object.values(data)
        this.eventos = eventos
        this.processarEventos(eventos)
        this.lastUpdate = new Date()
      } catch (error) {
        console.error('Erro ao buscar eventos:', error)
      } finally {
        this.loading = false
      }
    },

    processarEventos(eventos) {
      const carrosMap = new Map()

      eventos.forEach(evento => {
        const carroId = evento.carroId
        const existente = carrosMap.get(carroId)

        if (!existente || new Date(evento.timestamp) > new Date(existente.timestamp)) {
          const pressoes = evento.pressaoPneus || {}
          const valores = [
            pressoes.pneu1 || 0,
            pressoes.pneu2 || 0,
            pressoes.pneu3 || 0,
            pressoes.pneu4 || 0
          ]
          
          const mediaPressao = valores.reduce((a, b) => a + b, 0) / 4

          carrosMap.set(carroId, {
            carroId,
            nome: evento.nome,
            equipe: evento.equipe,
            pontoId: evento.pontoId,
            pontoNome: evento.pontoNome,
            velocidade: evento.velocidade,
            distancia: evento.distancia,
            pressaoPneus: pressoes,
            mediaPressao,
            timestamp: evento.timestamp,
            _source: evento._source
          })
        }
      })

      this.carrosData = carrosMap
    },

    setSelectedTeam(team) {
      this.selectedTeam = team
    },

    clearTeamFilter() {
      this.selectedTeam = null
    }
  }
})
