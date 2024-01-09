<template>
  <nav class="bg-gray-800 p-4 text-white flex justify-between items-center">
    <img :src="logo" alt="ScreenDiary Logo" class="h-16 mr-2"> <!-- Adjust the class as needed for sizing -->
    <div class="flex-grow mx-4">
      <input class="w-full p-2 rounded" type="search" placeholder="Search...">
    </div>
    <button class="p-2 rounded hover:bg-gray-700">
      <material-icon name="settings" filled title="Settings" :size="42"/>
    </button>
  </nav>
</template>

<script setup>
import logo from '@/assets/screendiary_logo.png';
</script>