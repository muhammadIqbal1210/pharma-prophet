<template>
  <nav class="flex items-center justify-center space-x-2 mt-4">
    <button
      @click="goToPage(currentPage - 1)"
      :disabled="currentPage === 1"
      class="px-3 py-1 rounded-md border border-gray-300 hover:bg-gray-100 disabled:opacity-50"
    >
      Prev
    </button>
    <template v-for="page in pages" :key="page">
      <button
        @click="goToPage(page)"
        :class="[
          'px-3 py-1 rounded-md border',
          page === currentPage ? 'bg-emerald-500 text-white border-emerald-600' : 'border-gray-300 hover:bg-gray-100'
        ]"
      >{{ page }}</button>
    </template>
    <button
      @click="goToPage(currentPage + 1)"
      :disabled="currentPage === totalPages"
      class="px-3 py-1 rounded-md border border-gray-300 hover:bg-gray-100 disabled:opacity-50"
    >
      Next
    </button>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps({
  totalItems: { type: Number, required: true },
  pageSize: { type: Number, default: 10 },
  currentPage: { type: Number, default: 1 },
});

const emit = defineEmits(['page-changed']);

const totalPages = computed(() => Math.ceil(props.totalItems / props.pageSize) || 1);

const pages = computed(() => {
  const range = [];
  const maxLinks = 5; // show limited page numbers
  let start = Math.max(1, props.currentPage - Math.floor(maxLinks / 2));
  let end = Math.min(totalPages.value, start + maxLinks - 1);
  if (end - start + 1 < maxLinks) {
    start = Math.max(1, end - maxLinks + 1);
  }
  for (let i = start; i <= end; i++) {
    range.push(i);
  }
  return range;
});

function goToPage(page: number) {
  if (page < 1) page = 1;
  if (page > totalPages.value) page = totalPages.value;
  emit('page-changed', page);
}
</script>

<style scoped>
/* Optional custom styling can be added here */
</style>
