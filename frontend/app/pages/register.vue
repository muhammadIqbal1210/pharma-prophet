<template>
  <div class="flex items-center justify-center min-h-screen p-4">
    <div class="bg-white rounded-3xl shadow-xl p-10 w-full max-w-md animate-fade-in">
      
      <div class="flex flex-col items-center mb-8 border-b border-slate-100 pb-6">
        <div class="flex items-center gap-4 mb-4">
          <img src="/ikon.jpg" alt="Logo Pharma Prophet" class="w-16 h-16 object-contain">
          <div>
            <h1 class="text-2xl font-bold text-slate-950 tracking-tight">Pharma Prophet</h1>
            <p class="text-xs font-medium text-slate-500 tracking-wider">Sistem Prediksi Stok Apotek</p>
          </div>
        </div>
        <p class="text-sm font-semibold text-slate-500">Daftar Akun Baru untuk akses sistem</p>
      </div>

      <div class="flex gap-2 rounded-xl border border-slate-400 mb-8">
        <NuxtLink to="/login" class="flex-1 text-center py-3 text-slate-900 hover:text-slate-900 font-semibold rounded-xl hover:bg-white/50 transition cursor-pointer">
          Masuk
        </NuxtLink>
        <div class="flex-1 text-center py-3 bg-gradient-to-r from-emerald-600 to-green-600 text-white font-semibold rounded-xl shadow-sm border border-slate-100 cursor-pointer">
          Daftar
        </div>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-5">
        <div class="grid grid-cols-2 gap-4">
          <div class="relative min-h-[56px]">
            <input 
              v-model="form.username" 
              type="text" 
              id="username"
              placeholder=" " 
              required 
              class="peer w-full px-4 py-3.5 bg-transparent border-2 border-slate-200 rounded-xl outline-none text-slate-900 font-medium text-base transition-colors duration-300 focus:border-emerald-500"
            />
            <label 
              for="username" 
              class="absolute left-3 bg-white text-slate-400 font-normal text-sm tracking-wider transition-all duration-300 pointer-events-none origin-[0_0]
                    top-1/2 -translate-y-1/2 scale-100
                    peer-focus:top-0 peer-focus:text-xs peer-focus:-translate-y-1/2 peer-focus:text-emerald-600 peer-focus:font-semibold
                    [:not(:placeholder-shown)]:top-0 [:not(:placeholder-shown)]:scale-85 [:not(:placeholder-shown)]:-translate-y-1/2 [:not(:placeholder-shown)]:text-emerald-600 [:not(:placeholder-shown)]:font-bold"
            >
              Username
            </label>
          </div>
          <div class="space-y-1.5">
            <label class="text-xs font-semibold text-slate-600 uppercase tracking-wider">Email</label>
            <input v-model="form.email" type="email" placeholder="contoh@med.com" required 
                   class="w-full px-5 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-200 focus:border-emerald-400 transition placeholder:text-slate-400 text-sm font-medium"/>
          </div>
        </div>

        <div class="space-y-1.5">
          <label class="text-xs font-semibold text-slate-600 uppercase tracking-wider">Nama Lengkap Tim Medis</label>
          <input v-model="form.nama_lengkap" type="text" placeholder="Muhammad Iqbal" required 
                 class="w-full px-5 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-200 focus:border-emerald-400 transition placeholder:text-slate-400 text-sm font-medium"/>
        </div>

        <div class="space-y-1.5 relative">
          <label class="text-xs font-semibold text-slate-600 uppercase tracking-wider">Password Aman</label>
          <input v-model="form.password" type="password" placeholder="••••••••" required 
                 class="w-full px-5 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-200 focus:border-emerald-400 transition placeholder:text-slate-400 text-sm font-medium"/>
        </div>

        <button type="submit" :disabled="loading" 
                class="w-full py-4 bg-gradient-to-r from-emerald-600 to-green-600 text-white font-bold rounded-2xl hover:shadow-lg hover:shadow-emerald-200 active:scale-[0.98] transition-all duration-150 disabled:opacity-60 disabled:cursor-not-allowed">
          {{ loading ? 'Mendaftar...' : 'Daftar Sekarang' }}
        </button>
      </form>

      <p v-if="errorMsg" class="mt-6 text-center text-sm font-semibold text-rose-600 bg-rose-50 p-4 rounded-xl border border-rose-100">{{ errorMsg }}</p>
    </div>
  </div>
</template>

<script setup>
const { register } = useAuth()
const form = ref({ username: '', nama_lengkap: '', email: '', password: '' , role: 'apoteker' }) 
const loading = ref(false)
const errorMsg = ref('')

const handleRegister = async () => {
  loading.value = true
  errorMsg.value = ''
  try {
    await register({
      ...form.value,
      role: 'apoteker' 
    })
  } catch (err) {
    errorMsg.value = err
  } finally {
    loading.value = false
  }
}
</script>