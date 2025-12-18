<script setup>
const props = defineProps({
  pressao: {
    type: Number,
    required: true
  },
  posicao: {
    type: String,
    required: true
  }
})

const getTireStatus = (pressao) => {
  if (pressao >= 40) return 'ok'
  if (pressao >= 30) return 'warning'
  if (pressao >= 20) return 'danger'
  if (pressao >= 10) return 'critical'
  return 'emergency'
}

const status = computed(() => getTireStatus(props.pressao))
</script>

<template>
  <div class="tire-container" :class="`tire-${status}`">
    <div class="tire-icon">
      <div class="tire-inner">
        <span class="tire-pressure">{{ pressao.toFixed(1) }}</span>
      </div>
    </div>
    <div v-if="status === 'emergency'" class="alert-icon">!</div>
    <span class="tire-label">{{ posicao }}</span>
  </div>
</template>

<style scoped>
.tire-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  position: relative;
}

.tire-icon {
  width: 60px;
  height: 80px;
  border: 3px solid;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.tire-inner {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.3);
}

.tire-pressure {
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
}

.tire-label {
  font-size: 0.75rem;
  color: #999;
  text-transform: uppercase;
}

.tire-ok .tire-icon {
  border-color: #00ff00;
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
}

.tire-warning .tire-icon {
  border-color: #ffff00;
  box-shadow: 0 0 10px rgba(255, 255, 0, 0.3);
}

.tire-danger .tire-icon {
  border-color: #ff0000;
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
}

.tire-critical .tire-icon {
  border-color: #ff0000;
  animation: blink 1s infinite;
}

.tire-emergency .tire-icon {
  border-color: #ff0000;
  animation: blink 0.5s infinite;
}

.alert-icon {
  position: absolute;
  top: -10px;
  right: -10px;
  width: 24px;
  height: 24px;
  background: #ff0000;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #fff;
  animation: pulse 1s infinite;
}

@keyframes blink {

  0%,
  49% {
    opacity: 1;
  }

  50%,
  100% {
    opacity: 0.3;
  }
}

@keyframes pulse {

  0%,
  100% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.2);
  }
}
</style>
