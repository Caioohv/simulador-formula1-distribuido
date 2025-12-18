<script setup>
const store = useCarrosStore()

const equipes = computed(() => store.equipesUnicas)
const selectedTeam = computed(() => store.selectedTeam)

const selectTeam = (team) => {
  if (selectedTeam.value === team) {
    store.clearTeamFilter()
  } else {
    store.setSelectedTeam(team)
  }
}
</script>

<template>
  <div class="team-filter">
    <h3 class="filter-title">Filtrar por Equipe</h3>
    <div class="team-buttons">
      <button class="team-button" :class="{ active: !selectedTeam }" @click="store.clearTeamFilter()">
        Todas
      </button>
      <button v-for="equipe in equipes" :key="equipe" class="team-button" :class="{ active: selectedTeam === equipe }"
        @click="selectTeam(equipe)">
        {{ equipe }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.team-filter {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.filter-title {
  font-size: 1rem;
  color: #999;
  margin: 0 0 1rem 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.team-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.team-button {
  padding: 0.5rem 1rem;
  background: #2a2a2a;
  border: 1px solid #444;
  border-radius: 4px;
  color: #999;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.team-button:hover {
  background: #333;
  border-color: #666;
  color: #fff;
}

.team-button.active {
  background: #444;
  border-color: #888;
  color: #fff;
  font-weight: bold;
}
</style>
