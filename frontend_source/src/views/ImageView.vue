<template>
  <div class="flex">
    <div class="w-1/2">
      <img :src="imageUrl" alt="" class="object-cover rounded shadow-md">
    </div>
    <div class="w-1/2">
      <Accordion>
        <template v-slot:header>
          <h2>Section 1</h2>
        </template>
        <p>This is content for section 1.</p>
      </Accordion>

      <Accordion>
        <template v-slot:header>
          <h2>Section 2</h2>
        </template>
        <p>This is content for section 2.</p>
      </Accordion>
    </div>
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
const imageUrl = computed(() => `https://via.placeholder.com/600x600?text=Image ${data.id}`);
</script>

