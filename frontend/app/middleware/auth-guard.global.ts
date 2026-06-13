export default defineNuxtRouteMiddleware((to, from) => {
  const { isLoggedIn, isAdmin } = useAuth()

  // 1. PENGAMANAN GLOBAL: Jika belum login, tendang ke halaman login (kecuali sedang di login/register)
  if (!isLoggedIn.value) {
    if (to.path !== '/login' && to.path !== '/register') {
      return navigateTo('/login')
    }
    return
  }

  // 2. JIKA SUDAH LOGIN: Blokir agar tidak bisa kembali mengakses halaman login/register
  if (isLoggedIn.value && (to.path === '/login' || to.path === '/register')) {
    if (isAdmin.value) {
      return navigateTo('/admin/dashboard')
    } else {
      return navigateTo('/apoteker/dashboard')
    }
  }

  // 3. VALIDASI RUTE ADMIN: Jika user biasa mencoba masuk ke area '/admin'
  if (to.path.startsWith('/admin')) {
    if (!isAdmin.value) {
      return navigateTo('/apoteker/dashboard')
    }
  }

  // 4. VALIDASI RUTE APOTEKER: Jika admin mencoba masuk ke area '/apoteker'
  if (to.path.startsWith('/apoteker')) {
    if (isAdmin.value) {
      return navigateTo('/admin/dashboard')
    }
  }
})