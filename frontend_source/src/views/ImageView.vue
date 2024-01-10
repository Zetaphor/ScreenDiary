<template>
  <div class="w-full flex items-center">
    <RouterLink to="/" class="ml-3 px-3 pt-2 bg-slate-600 text-white mr-4 rounded">
      <material-icon name="arrow_back" filled title="Back" :size="32" />
    </RouterLink>
    <div class="text-center flex-grow">
      <h1 class="text-3xl">{{ data.ocr_title }}</h1>
      <h2 class="text-xl text-gray-600">{{ data.remapped_name === null ? data.application_name : data.remapped_name }}</h2>
    </div>
  </div>

  <div class="w-full px-2">
    <Accordion class="mt-3 pr-3" :initial-open="true">
      <template v-slot:header>
        <h2 class="text-xl text-center font-bold">Metadata</h2>
      </template>
      <div class="flex px-2 pt-3">
        <div class="w-1/2">
          <a :href="imageUrl" target="_blank" class="w-full h-full">
            <img :src="imageUrl" alt="" class="object-cover shadow-md border-slate-600 border-2 rounded-md bg-slate-700">
          </a>
        </div>
        <div class="w-1/2 pl-2">
          <div>
            <p class="mt-3"><span class="font-bold">Date:</span> {{ $formatDateTime(data.datetime).date }}</p>
            <p><span class="font-bold">Time:</span> {{ $formatDateTime(data.datetime).time }}</p>
            <p class="mt-2" v-if="data.remapped_name !== null"><span class="font-bold">Original Name:</span> {{
              data.application_name }}</p>
            <p class="mt-2"><span class="font-bold">OCR Processing Time:</span> {{ data.ocr_time < 1.0 ?
              data.ocr_time.toFixed(3) * 1000 : data.ocr_time.toFixed(2) }}{{ data.ocr_time < 1.0 ? 'ms' : 's' }}</p>
                <div v-if="Boolean(data.url_captured)">
                  <p><span class="font-bold">URL:</span> <a :href="data.url" target="_blank">{{ data.url }}</a></p>
                  <p><span class="font-bold">{{ Boolean(data.url_partial) ? 'Partial URL Match' : 'Full URL Match'
                  }}:</span>
                  </p>
                  <p><span class="font-bold">URL Processing Time:</span> {{ data.url_time < 1.0 ? data.url_time.toFixed(3)
                    * 1000 : data.url_time.toFixed(2) }}{{ data.url_time < 1.0 ? 'ms' : 's' }}</p>
                </div>
          </div>
        </div>
      </div>
    </Accordion>
  </div>
  <div class="w-full px-2">
    <Accordion class="mt-3 pr-3">
      <template v-slot:header>
        <h2 class="text-xl text-center font-bold">OCR Content</h2>
      </template>
      <textarea class="w-full min-h-80 bg-gray-100 pb-4" v-model="data.ocr_content"></textarea>
    </Accordion>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Accordion from '@/components/Accordion.vue';
import { useSummaryStore } from '@/stores/summary'

const summary = useSummaryStore()

const route = useRoute();
const data = summary.getRecordById(route.params.id);
const imageUrl = computed(() => `http://localhost:5000/captures/screenshots/${data.datetime}.png`);
</script>

