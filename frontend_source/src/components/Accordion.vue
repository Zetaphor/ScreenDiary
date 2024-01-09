<template>
  <div class="accordion">
    <div
      class="accordion-header cursor-pointer p-4 bg-gray-200"
      @click="isOpen = !isOpen"
    >
      <slot name="header"></slot>
    </div>
    <div
      v-if="isOpen"
      class="accordion-content p-4 bg-gray-100"
    >
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isOpen = ref(false);
</script>
