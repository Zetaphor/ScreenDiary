<template>
  <nav class="bg-gray-800 p-4 text-white flex justify-between items-center">
    <RouterLink to="/">
      <img :src="logo" alt="ScreenDiary Logo" class="h-16 mr-2">
    </RouterLink>
    <div class="flex-grow mx-4">
      <input class="w-full p-2 rounded" type="search" placeholder="Search...">
    </div>
    <router-link to="/settings" class="p-2 rounded hover:bg-gray-700 inline-flex items-center">
      <material-icon name="settings" filled title="Settings" :size="42" />
    </router-link>

  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import logo from '@/assets/screendiary_logo.png';
</script>