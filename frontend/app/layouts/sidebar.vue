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
  { label: 'Dashboard', to: '/apoteker/dashboard', icon: 'lucide:layout-dashboard' },
  { label: 'Produk', to: '/apoteker/products', icon: 'lucide:package-plus' },
  // { label: 'Stok Obat', to: '/apoteker/stock', icon: 'lucide:pill' }, 
  { label: 'Transaksi', to: '/apoteker/transactions', icon: 'lucide:receipt' },
  // { label: 'Prediksi Stok', to: '/apoteker/prediksi', icon: 'lucide:cpu' },
]

const adminMenu = [
  { label: 'Dashboard', to: '/admin/dashboard', icon: 'lucide:layout-dashboard' },
  { label: 'Manajemen User', to: '/admin/users', icon: 'lucide:user-cog' },
  { label: 'Produk', to: '/admin/products', icon: 'lucide:package-plus' },
  { label: 'Stok Obat', to: '/admin/stock', icon: 'lucide:pill' }, 
  { label: 'Pembelian Stok', to: '/admin/purchases', icon: 'lucide:shopping-cart' },
  { label: 'Transaksi', to: '/admin/transactions', icon: 'lucide:receipt' },
  { label: 'Prediksi Stok', to: '/admin/prediksi', icon: 'lucide:cpu' },
  { label: 'Laporan Penjualan', to: '/admin/reports', icon: 'lucide:activity' }, 
]
</script>

<template>
  <div class="flex h-screen w-screen bg-slate-50 text-slate-800 font-sans antialiased overflow-hidden">
    <aside class="w-72 h-full sticky top-0 shrink-0 border-r border-slate-200 bg-white text-slate-700 flex flex-col justify-between overflow-y-auto">
      <div>
        <div class="p-6 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <img src="/ikon.jpg" alt="Logo Pharma Prophet" class="h-11 w-11 rounded-xl object-cover shadow-md ring-2 ring-emerald-400/30" />
            <div class="min-w-0">
              <h2 class="text-lg font-bold text-slate-900 tracking-tight leading-none">Pharma Cast</h2>
              <p class="text-slate-400 font-semibold text-[10px] tracking-tight mt-1 leading-snug">
                Sistem Manajemen Inventory dan Penjualan Apotek
              </p>
            </div>
          </div>
        </div>

        <nav class="p-4 space-y-1">
          <template v-if="!isAdmin">
            <p class="px-2 pb-2 text-[10px] font-semibold uppercase tracking-widest text-slate-400">Menu Utama</p>
            <NuxtLink
              v-for="item in mainMenu"
              :key="item.to"
              :to="item.to"
              class="flex items-center gap-3 rounded-xl px-4 py-2 text-sm font-semibold text-slate-600 transition-all duration-200 hover:bg-slate-50 hover:text-emerald-600 group"
              active-class="bg-emerald-50 !text-emerald-700 border border-emerald-100/50"
            >
              <div class="w-8 h-8 rounded-lg bg-slate-100 group-hover:bg-emerald-100/60 transition-colors flex items-center justify-center shrink-0"
                   :class="route.path === item.to ? '!bg-emerald-100 text-emerald-600' : 'text-slate-400 group-hover:text-emerald-600'">
                <Icon :name="item.icon" class="text-base" />
              </div>
              {{ item.label }}
            </NuxtLink>
          </template>

          <template v-if="isAdmin">
            <p class="px-4 text-[10px] font-semibold uppercase tracking-widest text-slate-400">Sistem Admin</p>
            <div class="space-y-1">
              <NuxtLink
                v-for="item in adminMenu.slice(0, 7)"
                :key="item.to"
                :to="item.to"
                class="flex items-center gap-3 rounded-xl px-4 py-2 text-sm font-semibold text-slate-600 transition-all duration-200 hover:bg-slate-50 hover:text-emerald-600 group"
                active-class="bg-emerald-50 !text-emerald-700 border border-emerald-100/50"
              >
                <div class="w-8 h-8 rounded-lg bg-slate-100 group-hover:bg-emerald-100/60 transition-colors flex items-center justify-center shrink-0"
                     :class="route.path === item.to ? '!bg-emerald-100 text-emerald-600' : 'text-slate-400 group-hover:text-emerald-600'">
                  <Icon :name="item.icon" class="text-base" />
                </div>
                {{ item.label }}
              </NuxtLink>
            </div>

            <div class="pt-4 space-y-1">
              <p class="px-4 pb-2 text-[10px] font-semibold uppercase tracking-widest text-slate-400">Laporan</p>
              <NuxtLink
                :to="adminMenu[7].to"
                class="flex items-center gap-3 rounded-xl px-4 py-2 text-sm font-semibold text-slate-600 transition-all duration-200 hover:bg-slate-50 hover:text-emerald-600 group"
                active-class="bg-emerald-50 !text-emerald-700 border border-emerald-100/50"
              >
                <div class="w-8 h-8 rounded-lg bg-slate-100 group-hover:bg-emerald-100/60 transition-colors flex items-center justify-center shrink-0"
                     :class="route.path === adminMenu[7].to ? '!bg-emerald-100 text-emerald-600' : 'text-slate-400 group-hover:text-emerald-600'">
                  <Icon :name="adminMenu[7].icon" class="text-base" />
                </div>
                {{ adminMenu[7].label }}
              </NuxtLink>
            </div>
          </template>
        </nav>
      </div>

      <div class="p-4 border-t border-slate-100 space-y-3 bg-slate-50/50">
        <div class="flex items-center gap-3 px-2 py-1">
          <div class="w-10 h-10 bg-emerald-600/10 text-emerald-700 rounded-xl shrink-0 flex items-center justify-center text-sm font-bold border border-emerald-200/50">
            {{ (currentUser?.nama_lengkap || '').charAt(0) }}
          </div>
          <div class="min-w-0 leading-tight">
            <h4 class="text-xs font-bold text-slate-900 truncate">
              {{ currentUser?.nama_lengkap || currentUser?.username || 'Pengguna' }}
            </h4>
            <p class="text-[10px] font-semibold text-slate-400 truncate mt-0.5 capitalize">
              {{ currentUser.role }}
            </p>
          </div>
        </div>

        <button
          type="button"
          @click="logout"
          class="flex w-full items-center gap-3 rounded-xl px-4 py-2.5 text-sm font-semibold text-rose-600 hover:bg-rose-50 transition-colors group"
        >
          <div class="w-8 h-8 rounded-lg bg-rose-50 group-hover:bg-rose-100 transition-colors flex items-center justify-center shrink-0 text-rose-500">
            <Icon name="lucide:log-out" class="text-base" />
          </div>
          Keluar
        </button>
      </div>
    </aside>

    <div class="flex min-h-screen flex-1 flex-col overflow-hidden">
      <header class="border-b border-slate-200 bg-white px-8 py-4 flex items-center justify-between gap-4">
        <div class="min-w-0">
          <h1 class="text-base font-bold text-slate-900 tracking-tight">{{ pageTitle }}</h1>
        </div>
        
        <div class="flex items-center gap-3 shrink-0">
          <div class="bg-slate-50 border border-slate-200 rounded-xl px-4 py-1.5 text-xs text-slate-600 flex items-center gap-2 font-bold shadow-sm">
            <div class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
            <span>Sesi: {{ currentUser?.nama_lengkap || currentUser?.username || 'Pengguna' }}</span>
          </div>
        </div>
      </header>

      <main class="flex-1 overflow-y-auto p-8 bg-slate-50/60">
        <slot />
      </main>
    </div>
  </div>
</template>