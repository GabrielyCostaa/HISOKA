// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: {
    enabled: true,
    timeline: {
      enabled: true,
    },
  },

  runtimeConfig: {
    apiSecret: "", // can be overridden by NUXT_API_SECRET environment variable
    public: {
      apiBase: "", // can be overridden by NUXT_PUBLIC_API_BASE environment variable
    },
  },

  experimental: {
    cookieStore: true,
  },

  modules: [
    "@nuxt/content",
    "@nuxt/eslint",
    "@nuxt/fonts",
    "@nuxt/icon",
    "@nuxt/image",
    "@nuxt/scripts",
    "@nuxt/test-utils",
    "@nuxt/ui",
    "@vueuse/nuxt",
    "@nuxtjs/i18n",
    "nuxt-auth-utils",
    "@pinia/nuxt",
    "nuxt-svgo",
  ],
  svgo: {
    autoImportPath: "~/assets/svg/",
    defaultImport: "component",
  },
  css: ["~/assets/css/main.css"],
  fonts: {
    families: [
      // do not resolve this font with any provider from `@nuxt/fonts`
      { name: "League Gothic", provider: "google" },
      // only resolve this font with the `google` provider
      // { name: 'My Font Family', provider: 'google' },
      // specify specific font data - this will bypass any providers
      //{ name: 'Other Font', src: 'https://example.com/font.woff2', weight: 'bold' },
    ],
  },
  ui: {
    theme: {
      colors: [
        "primary",
        "secondary",
        "neutral",
        "first",
        "second",
        "third",
        "fourth",
        "fifth",
        "info",
        "success",
        "warning",
        "error",
      ],
    },
  },
  plugins: [
    { src: "~/plugins/apexcharts.client.ts", mode: "client" },
    { src: "~/plugins/api.ts" },
    { src: "~/plugins/auth.client.ts", mode: "client" },
  ],
  i18n: {
    defaultLocale: "br",
    locales: [
      { code: "br", name: "Brasil", file: "br.json" },
      { code: "en", name: "English", file: "en.json" },
    ],
  },
});
