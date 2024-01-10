<template>
  <div class="grid grid-cols-3 gap-4 p-4">
    <div v-for="item in summary.ocr_records" :key="item.id" class="relative border-slate-600 border-2 rounded-md bg-slate-700 overflow-hidden h-full cursor-pointer min-h-[250px]" @click="navigateToImage(item.id)">
      <div class="flex flex-grow items-center justify-center h-full">
        <img class="object-contain shadow-md max-h-full" :src="`http://localhost:5000/captures/screenshots/${item.datetime}.png`">
      </div>

      <div class="absolute bottom-0 w-full bg-gray-900 text-white text-center py-1 rounded-b-md">
        <p>{{ item.ocr_title }}</p>
        <p class="text-gray-400 text-sm">{{ item.application_name }}</p>
      </div>

      <div class="absolute inset-0 bg-black bg-opacity-70 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
        <div class="text-white text-center">
          <p>{{ item.application_name }}</p>
          <p>{{ item.ocr_title }}</p>
          <p>{{ $formatDateTime(item.datetime).date }}</p>
          <p>{{ $formatDateTime(item.datetime).time }}</p>
          <template v-if="Boolean(item.url_captured)">
            <p>{{ item.url }}</p>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useSummaryStore } from '@/stores/summary'

const summary = useSummaryStore()
const router = useRouter();

function navigateToImage(itemId) {
  router.push({ name: 'ImageView', params: { id: itemId } });
}
</script>
