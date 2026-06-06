<!-- layouts/user-panel.vue -->
<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar Kiri -->
    <aside class="w-64 bg-slate-800 text-white p-5 flex flex-col gap-4">
      <div class="font-bold text-xl mb-6">User Panel</div>
      <NuxtLink to="/user" class="hover:text-blue-400">Dashboard</NuxtLink>
      <NuxtLink to="/user/profile" class="hover:text-blue-400">Profil Saya</NuxtLink>
      <NuxtLink to="/user/settings" class="hover:text-blue-400">Pengaturan</NuxtLink>
      <NuxtLink to="/" class="mt-auto hover:text-red-400">🚪 Keluar</NuxtLink>
    </aside>

    <!-- Area Konten Utama -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header Atas -->
      <header class="h-16 bg-white shadow flex items-center justify-between px-6">
        <h1 class="text-lg font-semibold text-gray-700">Nama Menu</h1>
        <p> Hi User, Optimalkan stok sekarang </p>
        <img src="/ikon.jpg" alt="Logo" class="h-8" />
      </header>

      <!-- Konten Halaman Dinamis -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-6">
        <slot />
      </main>
    </div>
  </div>
</template>
