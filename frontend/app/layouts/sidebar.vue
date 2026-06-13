<script setup>
const route = useRoute()
const { currentUser, isAdmin, logout } = useAuth()

// Sinkronisasi judul halaman agar mendeteksi rute admin maupun apoteker
const pageTitle = computed(() => {
  if (route.path.includes('/dashboard')) return 'Dashboard Ringkasan'
  if (route.path.includes('/stock')) return 'Stok Obat Apotek'
  if (route.path.includes('/transactions')) return 'Riwayat Transaksi'
  if (route.path.includes('/products')) return 'Manajemen Produk'
  if (route.path.includes('/users')) return 'Manajemen Pengguna'
  if (route.path.includes('/reports')) return 'Laporan & Analisis'
  if (route.path.includes('/prediksi')) return 'Prediksi PharmaCast'
  return 'Panel Kontrol PharmaCast'
})

const mainMenu = [
  { label: 'Dashboard', to: '/dashboard', icon: 'lucide:layout-dashboard' },
  { label: 'Stok Obat', to: '/stock', icon: 'lucide:pill' }, // Diubah ke ikon pil kesehatan
  { label: 'Transaksi', to: '/transactions', icon: 'lucide:receipt' },
  { label: 'Produk', to: '/products', icon: 'lucide:package-plus' },
]

const adminMenu = [
  { label: 'Dashboard', to: '/admin/dashboard', icon: 'lucide:layout-dashboard' },
  { label: 'Manajemen User', to: '/admin/users', icon: 'lucide:user-cog' },
  { label: 'Laporan', to: '/reports', icon: 'lucide:activity' }, // Diubah ke ikon aktivitas/grafik detak jantung
]
</script>

<template>
  <div class="flex min-h-screen bg-slate-50 text-slate-800 font-sans antialiased">
    <aside class="w-72 shrink-0 border-r border-teal-900 bg-teal-950 text-teal-100 shadow-xl flex flex-col justify-between">
      
      <div>
        <div class="p-6 border-b border-teal-900 bg-teal-950/60">
          <div class="flex items-center gap-3">
            <img src="/ikon.jpg" alt="Logo Pharma Prophet" class="h-11 w-11 rounded-xl object-cover shadow-md ring-2 ring-emerald-400/30" />
            <div class="min-w-0">
              <h2 class="text-lg font-extrabold text-white tracking-tight">PharmaCast</h2>
              <p class="text-emerald-400 font-medium text-[11px] truncate tracking-wider mt-0.5 ">Sistem Manajemen Inventory dan Penjualan Apotek</p>
            </div>
          </div>
        </div>

        <nav class="p-4 space-y-1.5">
          <template v-if="!isAdmin">
            <p class="px-3 pb-2 text-[10px] font-bold uppercase tracking-widest text-teal-500">Layanan Apoteker</p>
            <NuxtLink
              v-for="item in mainMenu"
              :key="item.to"
              :to="item.to"
              class="flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold text-teal-300/70 transition-all duration-200 hover:bg-teal-900/50 hover:text-white group"
              active-class="bg-emerald-600 !text-white shadow-md shadow-emerald-600/20 ring-1 ring-emerald-400/30"
            >
              <Icon :name="item.icon" class="text-lg text-teal-400/60 group-hover:text-emerald-400 transition-colors" />
              {{ item.label }}
            </NuxtLink>
          </template>

          <template v-if="isAdmin">
            <p class="px-3 pb-2 text-[10px] font-bold uppercase tracking-widest text-teal-500">Sistem Administrator</p>
            <NuxtLink
              v-for="item in adminMenu"
              :key="item.to"
              :to="item.to"
              class="flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold text-teal-300/70 transition-all duration-200 hover:bg-teal-900/50 hover:text-white group"
              active-class="bg-emerald-600 !text-white shadow-md shadow-emerald-600/20 ring-1 ring-emerald-400/30"
            >
              <Icon :name="item.icon" class="text-lg text-teal-400/60 group-hover:text-emerald-400 transition-colors" />
              {{ item.label }}
            </NuxtLink>
          </template>
        </nav>
      </div>

      <div class="p-4 border-t border-teal-900 bg-teal-950/40 space-y-3">
        <button
          type="button"
          @click="logout"
          class="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold text-rose-300 transition-colors hover:bg-rose-950/40 hover:text-rose-200 group"
        >
          <Icon name="lucide:log-out" class="text-lg text-rose-400/70 group-hover:text-rose-400" />
          Keluar Sistem
        </button>

        <div class="rounded-xl border border-teal-900 bg-teal-950/80 p-3.5 flex items-center justify-between shadow-inner">
          <div>
            <p class="text-[9px] font-bold uppercase tracking-widest text-teal-500">Akses Petugas</p>
            <p class="mt-0.5 text-xs font-bold text-white tracking-wide truncate max-w-[120px]">{{ isAdmin ? 'Sistem Manajer' : 'Apoteker Jaga' }}</p>
          </div>
          <span :class="isAdmin ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'" class="px-2 py-0.5 text-[10px] font-extrabold rounded-md border uppercase tracking-wider">
            {{ isAdmin ? 'ADMIN' : 'FARMASI' }}
          </span>
        </div>
      </div>
    </aside>

    <div class="flex min-h-screen flex-1 flex-col overflow-hidden">
      <header class="border-b border-slate-200/80 bg-white/90 px-8 py-4 shadow-sm backdrop-blur-md flex items-center justify-between gap-4">
        <div class="min-w-0">
          <h1 class="text-xl font-semibold text-slate-900 tracking-tight mt-0.5 truncate">{{ pageTitle }}</h1>
        </div>
        
        <div class="flex items-center gap-3 shrink-0">
          <div class="bg-emerald-50/60 border border-emerald-100 rounded-xl px-4 py-2 text-sm text-emerald-800 shadow-sm flex items-center gap-2">
            <Icon name="lucide:shield-check" class="text-emerald-600 text-base" />
            <span>Sesi Aktif: <strong class="text-slate-900 font-bold">{{ currentUser?.nama_lengkap || currentUser?.username || 'User' }}</strong></span>
          </div>
        </div>
      </header>

      <main class="flex-1 overflow-y-auto p-8 bg-slate-50/40">
        <slot />
      </main>
    </div>
  </div>
</template>