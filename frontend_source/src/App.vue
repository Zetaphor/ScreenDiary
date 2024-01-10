<script setup>
import { RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
</script>

<template>
  <header class="fixed top-0 w-full z-50">
    <Navbar />
  </header>

  <div class="pt-32">
    <RouterView />
  </div>
</template>

<style scoped></style>
