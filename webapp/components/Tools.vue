<template>
  <div class="pl-2">
    <div v-if="sensorStore.isConnected">
        <UButtonGroup size="xl">
            <UButton
            v-if="!sensorStore.isRecording"
            @click="record"
            color="success"
            variant="subtle"
            :label="$t('gravar')"
            />
            <UButton
            v-else
            @click="pause"
            color="success"
            variant="subtle"
            :label="$t('parar')"
            />
            <UButton
                @click="save(sensorStore.historyBuffer,Date.now(),'json')"
                color="success"
                variant="subtle"
                :label="$t('salvar')"
            />
        </UButtonGroup>
    </div>
  </div>
</template>

<script setup lang="ts">
const sensorStore = useSensorStore();

const record = () => sensorStore.StartRecord();
const pause = () => sensorStore.PauseRecord();
const save = (A: any,B: any,C: any) => sensorStore.SaveRecord(A,B,C);

</script>
