<script setup lang="ts">
definePageMeta({
  middleware: ["authenticated"],
});

const cookie = useCookie<User>("userCookie");

type User = {
  access_token: string;
  token_type: string;
  user_id: number;
};
const user = useAuthUserStore();

const runtimeConfig = useRuntimeConfig();
const showModal = ref(true);
const username = ref("");
const password = ref("");
async function login({ username, password }): Promise<void> {
  const formData = new URLSearchParams();
  formData.append("grant_type", "password");
  formData.append("username", username);
  formData.append("password", password);

  $fetch<User>(runtimeConfig.public.apiBase + "/auth/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Accept: "application/json",
    },
    body: formData,
  })
    .then(async (result) => {
      await user.setToken(result);
      await user.hydrateFromCookie();
      navigateTo("/");
    })
    .catch(() => alert("Bad credentials"));
}
</script>

<template>
  <ProductCarrousel class="" :open="showModal"> </ProductCarrousel>
  <NewLogin
    :open="showModal"
    :username="username"
    :password="password"
    @update:username="username = $event"
    @update:password="password = $event"
    @submit="login"
  />
</template>
