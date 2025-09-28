<template>
  <div class="pl-2">
    <UButtonGroup size="xl">
      <UButton
        v-if="!sensorStore.isConnected"
        @click="connect"
        color="success"
        variant="subtle"
        :label="$t('connect')"
      />
      <UButton
        v-else
        @click="disconnect"
        color="error"
        variant="subtle"
        :label="$t('disconnect')"
      />
    </UButtonGroup>
  </div>
</template>

<script setup lang="ts">
const sensorStore = useSensorStore();

const connect = () => sensorStore.connectSerial();
const disconnect = () => sensorStore.disconnect();
</script>
