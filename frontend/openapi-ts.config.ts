import { defineConfig } from '@hey-api/openapi-ts'

const API_URL_BASE = process.env.API_URL_BASE || 'http://localhost/api'

export default defineConfig({
  input: `${API_URL_BASE}/openapi.json`,
  output: {
    format: 'prettier',
    path: 'src/lib/api',
  },
  plugins: [
    '@hey-api/typescript',
    {
      name: '@hey-api/sdk',
      asClass: false,
    },
  ],
})
