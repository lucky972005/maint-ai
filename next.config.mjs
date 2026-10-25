import withPWA from "@ducanh2912/next-pwa";

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  eslint: {
    ignoreDuringBuilds: true,
  },
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "images.unsplash.com" },
    ],
  },
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "X-Frame-Options",
            value: "SAMEORIGIN",
          },
          {
            key: "X-XSS-Protection",
            value: "1; mode=block",
          },
          {
            key: "Referrer-Policy",
            value: "strict-origin-when-cross-origin",
          },
          {
            key: "Permissions-Policy",
            value: "camera=*, microphone=*",
          },
        ],
      },
    ];
  },
};

export default withPWA({
  dest: "public",
  disable: process.env.NODE_ENV === "development",
  register: true,
  workboxOptions: {
    skipWaiting: true,
    runtimeCaching: [
      {
        urlPattern: /^https:\/\/images\.unsplash\.com\/.*/i,
        handler: "StaleWhileRevalidate",
        options: { cacheName: "machine-images", expiration: { maxEntries: 50, maxAgeSeconds: 86400 * 30 } },
      },
      {
        urlPattern: /\/api\/.*/i,
        handler: "NetworkFirst",
        options: { cacheName: "api-cache", networkTimeoutSeconds: 10, expiration: { maxEntries: 32, maxAgeSeconds: 86400 } },
      },
    ],
  },
})(nextConfig);
