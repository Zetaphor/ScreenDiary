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
      class="accordion-content px-1 mb-4 bg-gray-100"
    >
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';

const props = defineProps({
  initialOpen: {
    type: Boolean,
    default: false
  }
});

const isOpen = ref(props.initialOpen);
</script>
