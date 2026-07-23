const apiUrl = import.meta.env.VITE_API_URL?.trim()

if (!apiUrl) {
  throw new Error(
    'Falta VITE_API_URL. Configura la URL del backend en el archivo .env.',
  )
}

export const API_URL = apiUrl.replace(/\/+$/, '')
