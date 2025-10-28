import { mande } from "mande";

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig();
  const api = mande(config.public.apiBase, {
    headers: {
      "Content-Type": "application/json",
    },
  });

  // Torna acessível via `nuxtApp.$api` e `useNuxtApp().$api`
  nuxtApp.provide("api", api);
});
