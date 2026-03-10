/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'amc-primary': '#3b82f6',
        'amc-secondary': '#8b5cf6',
        'amc-success': '#10b981',
        'amc-warning': '#f59e0b',
        'amc-error': '#ef4444',
      },
    },
  },
  plugins: [],
}
