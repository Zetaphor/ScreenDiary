<template>
  <div class="grid grid-cols-3 gap-4 p-4">
    <div v-for="item in summary.ocr_records" :key="item.id" class="aspect-w-1 aspect-h-1 relative cursor-pointer" @click="navigateToImage(item.id)">
      <img class="object-cover rounded shadow-md" :src="`https://placekitten.com/600/600`" alt="">
      <div class="absolute inset-0 bg-black bg-opacity-70 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
        <div class="text-white text-center">
          <p>{{ $formatDateTime(item.datetime).date }}</p>
          <p>{{ $formatDateTime(item.datetime).time }}</p>
          <p>{{ item.ocr_title }}</p>
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