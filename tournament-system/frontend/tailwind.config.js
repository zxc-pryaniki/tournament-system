/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // Це каже Tailwind шукати класи у твоїх React-файлах
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
