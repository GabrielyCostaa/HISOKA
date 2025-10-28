import { useAuthUserStore } from "@/stores/AuthUser";

export default defineNuxtPlugin(() => {
  const authStore = useAuthUserStore();
  authStore.hydrateFromCookie();
});
