<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <h2>Daftar Akun PharmaCast</h2>
      <p class="subtitle">Sistem Prediksi & Manajemen Stok Apotek</p>
      
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Username</label>
          <input v-model="form.username" type="text" placeholder="Masukkan Username" required />
        </div>
        <div class="form-group">
          <label>Nama Lengkap</label>
          <input v-model="form.nama_lengkap" type="text" placeholder="Masukkan nama lengkap" required />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="contoh@email.com" required />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input v-model="form.password" type="password" placeholder="••••••••" required />
        </div>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Mendaftar...' : 'Daftar Sekarang' }}
        </button>
      </form>

      <p v-if="errorMsg" class="error-text">{{ errorMsg }}</p>
      <p v-if="successMsg" class="success-text">{{ successMsg }}</p>
      
      <p class="auth-footer">
        Sudah punya akun? <NuxtLink to="/login">Login di sini</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
const { register } = useAuth()
const form = ref({ username: '', nama_lengkap: '', email: '', password: '' , role: 'apoteker' }) // Kita set role default di sini
const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

const handleRegister = async () => {
  loading.value = true
  errorMsg.value = ''
  successMsg.value = ''
  try {
    await register({
      ...form.value,
      role: 'apoteker'
    })
    successMsg.value = 'Pendaftaran berhasil. Silakan masuk menggunakan akun Anda.'
    navigateTo('/login')
  } catch (err) {
    errorMsg.value = err
  } finally {
    loading.value = false
  }
}
</script>