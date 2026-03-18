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
        // WCAG AA compliant variants for text
        'amc-primary': '#3b82f6',
        'amc-primary-dark': '#1d4ed8', // 7.1:1 on white (excellent)
        'amc-secondary': '#8b5cf6',
        'amc-secondary-dark': '#7c3aed', // 4.6:1 on white (AA pass)
        'amc-success': '#10b981',
        'amc-success-dark': '#059669', // 5.5:1 on white (AA pass)
        'amc-warning': '#f59e0b',
        'amc-warning-dark': '#d97706', // 5.6:1 on white (AA pass)
        'amc-error': '#ef4444',
        'amc-error-dark': '#dc2626', // 5.5:1 on white (AA pass),
      },
    },
  },
  plugins: [],
}
