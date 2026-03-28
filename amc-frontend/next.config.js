/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'export',
  trailingSlash: true,
  // basePath removed - using custom domain faintech-lab.com on Vercel
  // For GitHub Pages deployment, use: basePath: '/faintech-lab'
  images: {
    unoptimized: true
  }
}

module.exports = nextConfig
