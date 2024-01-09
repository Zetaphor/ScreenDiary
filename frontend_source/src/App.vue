<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
</script>

<template>
  <header>
    <!-- <div class="wrapper bg-slate-500">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div> -->
    <Navbar />
  </header>

  <RouterView />
</template>

<style scoped>

</style>
