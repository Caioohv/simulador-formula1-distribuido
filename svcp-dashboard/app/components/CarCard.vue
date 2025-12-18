<script setup>
const props = defineProps({
  carro: {
    type: Object,
    required: true
  },
  showDetails: {
    type: Boolean,
    default: false
  }
})

const tempoDesdeAtualizacao = ref('')

const calcularTempoDecorrido = () => {
  if (!props.carro.timestamp) return ''

  const agora = new Date()
  const dataEvento = new Date(props.carro.timestamp)
  const diff = Math.floor((agora - dataEvento) / 1000)

  if (diff < 60) return `${diff}s atrás`
  if (diff < 3600) return `${Math.floor(diff / 60)}m atrás`
  return `${Math.floor(diff / 3600)}h atrás`
}

const getTireStatus = (pressao) => {
  if (pressao >= 40) return 'ok'
  if (pressao >= 30) return 'warning'
  if (pressao >= 20) return 'danger'
  if (pressao >= 10) return 'critical'
  return 'emergency'
}

const menorPressaoStatus = computed(() => getTireStatus(props.carro.menorPressao))

onMounted(() => {
  tempoDesdeAtualizacao.value = calcularTempoDecorrido()

  setInterval(() => {
    tempoDesdeAtualizacao.value = calcularTempoDecorrido()
  }, 2000)
})
</script>

<template>
  <div class="car-card">
    <div class="car-header">
      <div class="car-info">
        <h3 class="car-name">{{ carro.nome }}</h3>
        <span class="car-team">{{ carro.equipe }}</span>
        <span class="car-id">#{{ carro.carroId }}</span>
      </div>
      <div class="car-stats">
        <div class="car-avg">
          <span class="avg-label">Pressão Média</span>
          <span class="avg-value" :class="{
            'avg-ok': carro.mediaPressao >= 40,
            'avg-warning': carro.mediaPressao >= 30 && carro.mediaPressao < 40,
            'avg-danger': carro.mediaPressao < 30
          }">
            {{ carro.mediaPressao.toFixed(1) }} PSI
          </span>
        </div>
        <div class="car-min">
          <span class="min-label">Menor Pressão</span>
          <span class="min-value" :class="`tire-${menorPressaoStatus}`">
            {{ carro.menorPressao.toFixed(1) }} PSI
          </span>
        </div>
      </div>
    </div>

    <div v-if="showDetails" class="car-details">
      <div class="detail-row">
        <span class="detail-label">Último ponto:</span>
        <span class="detail-value">{{ carro.pontoNome }} (#{{ carro.pontoId }})</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Velocidade:</span>
        <span class="detail-value">{{ (carro.velocidade * 3.6).toFixed(2) }} km/h</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Atualizado:</span>
        <span class="detail-value">{{ tempoDesdeAtualizacao }}</span>
      </div>
    </div>

    <div class="tires-grid">
      <div class="tire-row">
        <TireStatus :pressao="carro.pressaoPneus.pneu1 || 0" posicao="FE" />
        <TireStatus :pressao="carro.pressaoPneus.pneu2 || 0" posicao="FD" />
      </div>
      <div class="tire-row">
        <TireStatus :pressao="carro.pressaoPneus.pneu3 || 0" posicao="TE" />
        <TireStatus :pressao="carro.pressaoPneus.pneu4 || 0" posicao="TD" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.car-card {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.car-card:hover {
  border-color: #555;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.car-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #333;
}

.car-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.car-name {
  font-size: 1.25rem;
  font-weight: bold;
  color: #fff;
  margin: 0;
}

.car-team {
  font-size: 0.9rem;
  color: #999;
}

.car-id {
  font-size: 0.8rem;
  color: #666;
}

.car-stats {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.car-avg,
.car-min {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.avg-label,
.min-label {
  font-size: 0.75rem;
  color: #999;
  text-transform: uppercase;
}

.avg-value,
.min-value {
  font-size: 1.5rem;
  font-weight: bold;
}

.avg-ok {
  color: #00ff00;
}

.avg-warning {
  color: #ffff00;
}

.avg-danger {
  color: #ff0000;
}

.tire-ok {
  color: #00ff00;
}

.tire-warning {
  color: #ffff00;
}

.tire-danger {
  color: #ff6600;
}

.tire-critical {
  color: #ff0000;
}

.tire-emergency {
  color: #ff0000;
  animation: blink 1s infinite;
}

@keyframes blink {

  0%,
  50%,
  100% {
    opacity: 1;
  }

  25%,
  75% {
    opacity: 0.3;
  }
}

.car-details {
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 0.25rem 0;
  font-size: 0.9rem;
}

.detail-label {
  color: #999;
}

.detail-value {
  color: #fff;
  font-weight: 500;
}

.tires-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

.tire-row {
  display: flex;
  gap: 3rem;
  justify-content: center;
}
</style>
