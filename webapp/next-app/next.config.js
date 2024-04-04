/** @type {import('next').NextConfig} */

const nextConfig = {
  output: "standalone",
  images: {
    domains: ['localhost', '127.0.0.1', '0.0.0.0', 'api'],
  },
  i18n: {
    locales: ['ru'], // Add your locales here
    defaultLocale: 'ru', // Specify your default locale
  },
};

module.exports = nextConfig;
