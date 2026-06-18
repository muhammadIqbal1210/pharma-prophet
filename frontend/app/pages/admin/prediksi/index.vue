<script setup>
definePageMeta({
  layout: 'sidebar', // Menggunakan layouts/sidebar.vue
  composables: 'useAuth'    // Menggunakan middleware/auth.ts
})

</script>
<template>
    <div class="space-y-6">
        <div class="flex justify-between items-center">
        <div>
            <h1 class="text-2xl font-bold text-slate-900">Manajemen Prediksi</h1>
            <p class="text-sm text-slate-500">Kelola dan pantau data prediksi penjualan obat apotek.</p>
        </div>  
    </div>
    </div>    
</template>