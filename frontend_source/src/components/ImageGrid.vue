<template>
  <div class="grid grid-cols-3 gap-4 p-4">
    <div v-for="i in 9" :key="i" class="aspect-w-1 aspect-h-1">
      <img class="object-cover rounded shadow-md" :src="`https://via.placeholder.com/600x600?text=Image ${i}`" alt="">
    </div>
  </div>
</template>
