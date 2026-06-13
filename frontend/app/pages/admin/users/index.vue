<script setup>
definePageMeta({
  layout: 'sidebar', // Menggunakan layouts/user-panel.vue
  composables: 'useAuth'    // Menggunakan middleware/auth.ts
})

const config = useRuntimeConfig()
const { currentUser, isAdmin } = useAuth()

// Ambil data pengguna dari backend
const { data: users, pending, error, refresh } = await useFetch(`${config.public.apiBase}/auth/users`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${currentUser.value?.token}`
  }
})

// Fungsi menghapus user
// const deleteUser = (id) => {
//   if (confirm('Apakah Anda yakin ingin menghapus user ini?')) {
//     // Panggil API untuk menghapus user
//     $fetch(`${config.public.apiBase}/users/${id}`, {
//       method: 'DELETE',
//       headers: {
//         Authorization: `Bearer ${currentUser.value?.token}`
//       }
//     }).then(() => {
//       alert('User berhasil dihapus')
//       refresh() // Refresh data setelah penghapusan
//     }).catch(() => {
//       alert('Gagal menghapus user')
//     })
//   }
// }
</script>
<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Manajemen Pengguna</h1>
        <p class="text-sm text-slate-500">Kelola akun admin dan apoteker yang terdaftar di sistem.</p>
      </div>
      <button class="px-4 py-2.5 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition text-sm">
        + Tambah Pengguna
      </button>
    </div>

    <div v-if="pending" class="text-center py-12 text-slate-500">
      <p class="animate-pulse">Sedang memuat data dari server...</p>
    </div>

    <div v-else-if="error" class="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-100 text-sm">
      Gagal memuat data: {{ error.message || 'Terjadi kesalahan pada server.' }}
    </div>

    <div v-else class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <table class="w-full text-left border-collapse">
        <thead class="bg-slate-50 border-b border-slate-200">
          <tr>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Nama</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Email</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Role</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-center">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 text-sm text-slate-700">
          <tr v-for="user in users" :key="user.id" class="hover:bg-slate-50/80 transition">
            <td class="p-4 font-semibold text-slate-900">{{ user.nama_lengkap }}</td>
            <td class="p-4 text-slate-500">{{ user.email }}</td>
            <td class="p-4">
              <span :class="user.role === 'admin' ? 'bg-purple-50 text-purple-700 border-purple-100' : 'bg-blue-50 text-blue-700 border-blue-100'" 
                    class="px-2.5 py-1 text-xs font-semibold rounded-full border capitalize">
                {{ user.role }}
              </span>
            </td>
            <td class="p-4 text-center space-x-2">
              <button class="text-indigo-600 hover:text-indigo-900 font-medium">Edit</button>
              <button @click="deleteUser(user.id)" class="text-rose-600 hover:text-rose-900 font-medium">Hapus</button>
            </td>
          </tr>
          
          <tr v-if="users?.length === 0">
            <td colspan="4" class="p-8 text-center text-slate-400">Tidak ada data pengguna found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
