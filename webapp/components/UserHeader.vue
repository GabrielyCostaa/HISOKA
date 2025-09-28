<template>
  <div class="p-4 flex items-center justify-between">
    <div v-if="user.loggedIn" class="flex items-center gap-4">
      <span>{{ $t("hello") }}, {{ user.username }} ( {{ user.email }} )</span>
      <UButton class="sm text-gray-50" @click="logout">{{ $t("logout") }}</UButton>
    </div>
    <div v-else-if="route.path == '/graphs'">
      <UButton class="sm text-gray-50" @click="login">{{ $t("login") }}</UButton>
    </div>
  </div>
</template>

<script setup lang="ts">
const user = useAuthUserStore();
const route = useRoute()

async function logout() {
  await user.logout();
  navigateTo("/");
}
async function login() {
  navigateTo("/login");
}

</script>

<style scoped></style>
