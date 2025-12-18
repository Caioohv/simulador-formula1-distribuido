<script setup>
const store = useCarrosStore()

const carros = computed(() => {
  return store.selectedTeam ? store.carrosPorEquipe : store.carrosOrdenados
})

const showDetails = computed(() => !!store.selectedTeam)

onMounted(() => {
  store.fetchEventos()

  setInterval(() => {
    store.fetchEventos()
  }, 5000)
})
</script>

<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1 class="dashboard-title">F1 Tire Monitoring Dashboard</h1>
      <div class="header-info">
        <span v-if="store.lastUpdate" class="last-update">
          Última atualização: {{ new Date(store.lastUpdate).toLocaleTimeString() }}
        </span>
        <span class="car-count">{{ carros.length }} carros monitorados</span>
      </div>
    </header>

    <div class="dashboard-content">
      <TeamFilter />

      <div v-if="store.loading" class="loading">
        Carregando dados...
      </div>

      <div v-else-if="carros.length === 0" class="no-data">
        Nenhum dado disponível
      </div>

      <div v-else class="cars-grid">
        <CarCard v-for="carro in carros" :key="carro.carroId" :carro="carro" :show-details="showDetails" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  min-height: 100vh;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #333;
}

.dashboard-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #fff;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.header-info {
  display: flex;
  gap: 2rem;
  font-size: 0.9rem;
  color: #999;
}

.last-update,
.car-count {
  display: flex;
  align-items: center;
}

.dashboard-content {
  width: 100%;
}

.loading,
.no-data {
  text-align: center;
  padding: 4rem 2rem;
  font-size: 1.2rem;
  color: #666;
}

.cars-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }

  .dashboard-title {
    font-size: 1.8rem;
  }

  .cars-grid {
    grid-template-columns: 1fr;
  }

  .header-info {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
