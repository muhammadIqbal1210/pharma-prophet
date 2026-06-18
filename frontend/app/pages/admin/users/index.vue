<script setup>
definePageMeta({
  layout: 'sidebar', // Menggunakan layouts/sidebar.vue
  composables: 'useAuth'    // Menggunakan middleware/auth.ts
})

const config = useRuntimeConfig()
const { currentUser } = useAuth()

// Ambil data pengguna dari backend
const { data: users, pending, error, refresh } = await useFetch(`${config.public.apiBase}/auth/users`, {
  method: 'GET',
  headers: {
    Authorization: `Bearer ${currentUser.value?.token}`
  }
})

// Fungsi menghapus user
const deleteUser = (id) => {
  if (confirm('Apakah Anda yakin ingin menghapus user ini?')) {
    $fetch(`${config.public.apiBase}/auth/users/${id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${currentUser.value?.token}`
      }
    }).then(() => {
      alert('User berhasil dihapus')
      refresh() // Refresh data tabel setelah penghapusan sukses
    }).catch(() => {
      alert('Gagal menghapus user')
    })
  }
}

// State untuk kontrol buka/tutup modal
const isModalOpen = ref(false)

// State input form: Dikunci mati secara otomatis menggunakan role 'apoteker'
const form = ref({
  nama_lengkap: '',
  username: '',
  email: '',
  password: '',
  role: 'apoteker' // <-- Otomatis dikunci sebagai apoteker
})

// Fungsi kirim data ke Backend
const handleAddUser = async () => {
  try {
    await $fetch(`${config.public.apiBase}/auth/register`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${currentUser.value?.token}`
      },
      body: form.value
    })
    
    form.value = { nama_lengkap: '', username: '', email: '', password: '', role: 'apoteker' }
    isModalOpen.value = false
    refresh()
    alert('Petugas apoteker baru berhasil ditambahkan!')
  } catch (error) {
    // Jalur alternatif jika error berasal dari validasi Pydantic FastAPI (Error 422)
    const rawDetail = error.response?._data?.detail
    
    let cleanMessage = 'Terjadi kesalahan pada server.'

    if (Array.isArray(rawDetail)) {
      // Jika detail berupa array, ambil pesan 'msg' dari baris error pertama
      cleanMessage = rawDetail[0]?.msg || cleanMessage
    } else if (typeof rawDetail === 'string') {
      // Jika detail langsung berupa string pesan biasa (misal dari HTTPExceptions)
      cleanMessage = rawDetail
    } else {
      // Jika tidak keduanya, pakai fallback error message bawaan fetch
      cleanMessage = error.message
    }

    alert('Gagal menambah data: ' + cleanMessage)
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Manajemen Pengguna</h1>
        <p class="text-sm text-slate-500">Kelola akun staf apoteker yang terdaftar di dalam sistem.</p>
      </div>
      <button @click="isModalOpen = true" class="px-4 py-2.5 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition text-sm flex items-center gap-1.5 shadow-sm">
        <Icon name="lucide:user-plus" class="text-base" />
        Tambah Petugas
      </button>
    </div>

    <div v-if="pending" class="text-center py-12 text-slate-500">
      <p class="animate-pulse font-medium text-sm">Sedang memuat data dari server...</p>
    </div>

    <div v-else-if="error" class="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-100 text-sm">
      Gagal memuat data: {{ error.message || 'Terjadi kesalahan pada server.' }}
    </div>

    <div v-else class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <table class="w-full text-left border-collapse">
        <thead class="bg-slate-50 border-b border-slate-200">
          <tr>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Username</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Nama Lengkap</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Email</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Hak Akses</th>
            <th class="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-center">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 text-sm text-slate-700">
          <tr v-for="user in users" :key="user.id" class="hover:bg-slate-50/80 transition">
            <td class="p-4 font-mono text-slate-600 text-xs">{{ user.username }}</td>
            <td class="p-4 font-semibold text-slate-900">{{ user.nama_lengkap }}</td>
            <td class="p-4 text-slate-500">{{ user.email }}</td>
            <td class="p-4">
              <span :class="user.role === 'admin' ? 'bg-purple-50 text-purple-700 border-purple-100' : 'bg-teal-50 text-teal-700 border-teal-100'" 
                    class="px-2.5 py-1 text-xs font-bold rounded-lg border capitalize tracking-wide">
                {{ user.role }}
              </span>
            </td>
            <td class="p-4 text-center space-x-3">
              <button class="text-indigo-600 hover:text-indigo-900 font-semibold text-xs">Edit</button>
              <button @click="deleteUser(user.id)" class="text-rose-600 hover:text-rose-900 font-semibold text-xs">Hapus</button>
            </td>
          </tr>
          
          <tr v-if="!users?.length">
            <td colspan="5" class="p-8 text-center text-slate-400">Tidak ada data pengguna yang ditemukan.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm animate-fade-in">
      <div class="bg-white w-full max-w-md rounded-2xl shadow-xl p-6 border border-slate-100 space-y-4">
        
        <div class="flex justify-between items-center border-b pb-3">
          <div>
            <h3 class="text-lg font-bold text-slate-900">Registrasi Apoteker Baru</h3>
            <p class="text-xs text-slate-400 mt-0.5">Akun otomatis terdaftar sebagai hak akses Farmasi.</p>
          </div>
          <button @click="isModalOpen = false" class="text-slate-400 hover:text-slate-600 transition">✕</button>
        </div>

        <form @submit.prevent="handleAddUser" class="space-y-4">
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Nama Lengkap</label>
            <input v-model="form.nama_lengkap" type="text" required placeholder="Contoh: Apt. Rudi Hermawan" class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition" />
          </div>
          
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Username</label>
            <input v-model="form.username" type="text" required placeholder="rudi_farmasi" class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm font-mono transition" />
          </div>
          
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Email Resmi</label>
            <input v-model="form.email" type="email" required placeholder="rudi@domain.com" class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition" />
          </div>
          
          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Password Awal</label>
            <input v-model="form.password" type="password" required placeholder="••••••••" class="w-full mt-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none text-sm transition" />
          </div>

          <div class="flex justify-end gap-2 pt-3 border-t mt-2">
            <button type="button" @click="isModalOpen = false" class="px-4 py-2.5 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50 font-semibold text-xs transition">
              Batal
            </button>
            <button type="submit" class="px-5 py-2.5 bg-emerald-600 text-white rounded-xl hover:bg-emerald-700 font-semibold text-xs shadow-md transition">
              Simpan & Daftarkan
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>