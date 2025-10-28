export default defineNuxtRouteMiddleware(async (to, from) => {
  const user = useAuthUserStore();

  if (to.path === "/" && user.loggedIn) {
    return navigateTo("/graphs");
  }

  if (to.path === "/login" && user.loggedIn) {
    return navigateTo("/");
  }

  if (to.path != "/login" && !user.loggedIn) {
    console.log("Usuário não autenticado, redirecionando...");
    return navigateTo("/login");
  }
});
