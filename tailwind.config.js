/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', 
    './templates/*.html',
    './templates/**/*.html',
    './static/**/*.css',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('tailwindcss'),
    require('autoprefixer'),
  ],
}
