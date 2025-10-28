<script setup lang="ts">
definePageMeta({
  middleware: ["authenticated"],
});

const userStore = useAuthUserStore();

console.log("username:", userStore.username);

async function logout() {
  await navigateTo("/login");
}
</script>

<template>
  <div>
    <h1>{{ $t("welcome") }} {{ userStore.username }}</h1>
    <button @click="logout">Logout</button>
  </div>
</template>
