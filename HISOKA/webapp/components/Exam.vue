<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useExamStore } from '~/stores/examStore'

const examStore = useExamStore()
const userStore = useAuthUserStore()
const sensorStore = useSensorStore()
const selectedExamId = ref<number | null>(null)

// Fetch exams on mount
onMounted(() => {
  examStore.fetchExams()
})


// Prepare dropdown menu items based on exams
const dropdownItems = computed<DropdownMenuItem[]>(() => {
  return examStore.exams.map(exam => ({
    label: exam.created_at,
    description: `Exam ID: ${exam.comment}`,
    // optional: icon: 'i-lucide-book-open',
    onClick: () => selectExam(exam.id)
  }))
})

// Handle exam selection
async function selectExam(examId: number) {
  if (selectedExamId.value !== examId) {
    selectedExamId.value = examId
    await examStore.fetchReadings(examId)
  } else {
    selectedExamId.value = null
    examStore.readings = []
  }
}
</script>

<template>
  <div v-if="selectedExamId?.valueOf()">
    <UButton
      @click="sensorStore.SaveRecord(sensorStore.historyBuffer, Date.now(), 'json')"
      color="success"
      variant="subtle"
      :label="$t('export')"
    />
    <UButton
      @click="examStore.deleteExam(selectedExamId.valueOf()); selectedExamId = null"
      color="error"
      variant="subtle"
      :label="$t('delete')"
    />
  </div>
  <div v-if="userStore.email">
    <UDropdownMenu
    size="xl"
    :items="dropdownItems"
    :content="{ align: 'start' }"
    :ui="{ content: 'w-64' }"
    >
    <UButton
    size="xl"
    label="Select an Exam ID"
    icon="i-lucide-menu"
    color="neutral"
    variant="outline"
    />
  </UDropdownMenu>
</div>
</template>
