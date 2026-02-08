/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: true, // Optional: adds trailing slashes to URLs
  images: {
    unoptimized: true, // Important for static exports
  },
  // Enable standalone output for Docker
  output: 'standalone',
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_BETTER_AUTH_URL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
    NEXT_PUBLIC_BETTER_AUTH_SECRET: process.env.NEXT_PUBLIC_BETTER_AUTH_SECRET,
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME,
    NEXT_PUBLIC_BASE_URL: process.env.NEXT_PUBLIC_BASE_URL,
  },
};

module.exports = nextConfig;