<script setup>
import { useSummaryStore } from '@/stores/summary'
import { onMounted } from 'vue'
import ImageGrid from '@/components/ImageGrid.vue'

const summary = useSummaryStore()

onMounted(() => {
  summary.fetchSummary()
})
</script>

<template>
  <div>
    <ImageGrid />
  </div>
</template>