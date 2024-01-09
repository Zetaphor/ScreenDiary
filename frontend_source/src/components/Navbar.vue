<template>
  <nav class="bg-gray-800 p-4 text-white flex justify-between items-center">
    <RouterLink to="/">
      <img :src="logo" alt="ScreenDiary Logo" class="h-16 mr-2">
    </RouterLink>
    <div class="flex-grow mx-4">
      <div>
        <input class="w-full p-2 rounded" type="search" placeholder="Search...">
      </div>
    </div>
    <button class="p-2 rounded hover:bg-gray-700 inline-flex items-center">
      <material-icon name="search" filled title="Search" :size="42" />
    </button>
    <button class="p-2 rounded hover:bg-gray-700 inline-flex items-center">
      <material-icon name="refresh" filled title="Reload" :size="42" />
    </button>
    <router-link to="/settings" class="p-2 rounded hover:bg-gray-700 inline-flex items-center">
      <material-icon name="settings" filled title="Settings" :size="42" />
    </router-link>
  </nav>
  <div class="w-full bg-slate-300">
    <p class="p-1 pl-4">{{ summary.ocr_completed }} processed captures. <span v-if="summary.ocr_pending">{{ summary.ocr_pending }} captures awaiting processing.</span></p>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import logo from '@/assets/screendiary_logo.png';
import { useSummaryStore } from '@/stores/summary'

const summary = useSummaryStore()
</script>