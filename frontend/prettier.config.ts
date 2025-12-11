import { type Config } from 'prettier'

const config: Config = {
  singleQuote: true,
  trailingComma: 'all',
  semi: false,
  plugins: ['prettier-plugin-tailwindcss', 'prettier-plugin-svelte'],
  overrides: [
    {
      files: '*.svelte',
      options: {
        parser: 'svelte',
      },
    },
  ],
  tailwindStylesheet: './src/routes/layout.css',
}

export default config
