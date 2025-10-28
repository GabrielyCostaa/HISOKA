<script setup lang="ts">
import { ref, reactive } from 'vue'
import { createReusableTemplate, useMediaQuery } from '@vueuse/core'

const sensorStore = useSensorStore()
const examStore = useExamStore()
const userStore = useAuthUserStore()

// Reusable form template for both drawer and modal
const [DefineFormTemplate, ReuseFormTemplate] = createReusableTemplate()
const isDesktop = useMediaQuery('(min-width: 768px)')

// Drawer / Modal state
const open = ref(false)

const formState = reactive({
  comment: ''
})

const title = 'New Exam'
const description = "Enter a comment for this exam before recording."

// Logic
const record = () => {
  if (sensorStore.isRecording) return;
  // sensorStore.clearHistoryBuffer();
  sensorStore.StartRecord();
  if (userStore.email && examStore.selectedExam == null) {
    // open the drawer/modal instead of using prompt
    open.value = true
  }
}

const pause = () => sensorStore.PauseRecord()

const save = (A: any, B: any, C: any) => {
  pause();
  if (userStore.email && examStore.selectedExam != null) {
    for (const sensor_id in A) {
      const readings = A[sensor_id][1]
      const timestamps = A[sensor_id][0]
      examStore.uploadReadings(examStore.selectedExam.id, [
        { sensor_id, readings, timestamps }
      ])
      console.log("A", A);
      console.log("history", sensorStore.getHistoryBuffer());
      console.log("A is history?", A === sensorStore.getHistoryBuffer());
      
      // sensorStore.clearHistoryBufferById(sensor_id);
      // sensorStore.clearSensorDataById(sensor_id);
    }
  } else {
    sensorStore.SaveRecord(A, B, C)
  }
  
  examStore.selectedExam = null;
  sensorStore.clearHistoryBuffer();
  sensorStore.clearSensorData();
}

// Handle submission of comment
const handleSubmit = async () => {
  if (formState.comment.trim() !== '') {
    await examStore.createExam(formState.comment)
    formState.comment = ''
    open.value = false
  } else {
    alert('Please enter a comment before starting.')
  }
}
</script>

<template>
  <div class="pl-2">
    <div>
      <UButtonGroup size="xl">
        <div v-if="sensorStore.isConnected">
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
          @click="save(sensorStore.getHistoryBuffer(), Date.now(), 'json')"
          color="success"
          variant="subtle"
          :label="$t('salvar')"
          />
        </div>
        <Exam v-else/>
      </UButtonGroup>
    </div>


    <!-- Reusable form -->
    <DefineFormTemplate>
      <UForm :state="formState" class="space-y-4" @submit.prevent="handleSubmit">
        <UFormField label="Comment" name="comment" required>
          <UInput
            v-model="formState.comment"
            placeholder="Enter a comment for this exam"
            required
          />
        </UFormField>

        <UButton label="Start Recording" type="submit" color="success" />
      </UForm>
    </DefineFormTemplate>

    <!-- Desktop: Modal -->
    <UModal
      v-if="isDesktop"
      v-model:open="open"
      :title="title"
      :description="description"
    >
      <template #body>
        <ReuseFormTemplate />
      </template>
    </UModal>

    <!-- Mobile: Drawer -->
    <UDrawer
      v-else
      v-model:open="open"
      :title="title"
      :description="description"
    >
      <template #body>
        <ReuseFormTemplate />
      </template>
    </UDrawer>
  </div>
</template>
