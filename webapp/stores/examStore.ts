import { defineStore } from 'pinia'

import { useNuxtApp } from '#app' // Required for Nuxt composables

export interface Exam {
  id: number
  comment?: string
  created_at: string
}

export interface ReadingGroup {
  sensor_id: string
  readings: number[]
  timestamps: number[]
}

export const useExamStore = defineStore('exam', {
  state: () => ({
    exams: [] as Exam[],
    selectedExam: null as Exam | null,
    readings: [] as ReadingGroup[],
    loading: false as boolean,
    error: null as string | null,
  }),

  actions: {
    async fetchExams(skip = 0, limit = 20) {
      const { $api } = useNuxtApp();
      this.loading = true
      this.error = null
      try {
        const res = await $api.get<Exam[]>(`/exams?skip=${skip}&limit=${limit}`)
        console.log("Fetched exams:", res);
        this.exams = res
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Failed to load exams'
      } finally {
        this.loading = false
      }
    },

    async fetchExam(id: number) {
      this.loading = true
      const { $api } = useNuxtApp();
      try {
        const res = await $api.get<Exam>(`/exams/${id}`)
        this.selectedExam = res
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Exam not found'
      } finally {
        this.loading = false
      }
    },

    async createExam(comment?: string) {
      const { $api } = useNuxtApp();
      this.loading = true
      try {
        const res = await $api.post<Exam>('/exams', { comment })
        this.exams.push(res)
        this.selectedExam = res
        return res
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Failed to create exam'
      } finally {
        this.loading = false
      }
    },

    async fetchReadings(examId: number) {
      const { $api } = useNuxtApp();
      this.loading = true
      this.error = null
      try {
        const res = await $api.get<ReadingGroup[]>(`reading/exams/${examId}/bulk`)
        this.readings = res
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Failed to load readings'
      } finally {
        this.loading = false
      }
      console.log("Fetched readings:", this.readings);
    },

    async uploadReadings(examId: number, data: ReadingGroup[]) {
      const { $api } = useNuxtApp();
      this.loading = true
      try {
        const res = await $api.post<ReadingGroup[]>(`reading/exams/${examId}/bulk`, data)
        this.readings = res
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Failed to upload readings'
      } finally {
        this.loading = false
      }
    },

    async deleteExam(examId: number) {
      const { $api } = useNuxtApp();
      this.loading = true
      try {
        await $api.delete(`/exams/${examId}`)
        this.exams = this.exams.filter(exam => exam.id !== examId)
        if (this.selectedExam?.id === examId) {
          this.selectedExam = null
          this.readings = []
        }
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Failed to delete exam'
      } finally {
        this.loading = false
      }
    }
  },
})
