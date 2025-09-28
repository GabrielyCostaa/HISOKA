<template>
  <UModal
    v-model:open="localOpen"
    title="Login"
    :dismissible="false"
    :ui="{ header: 'justify-center' }"
    :overlay="false"
    class="bg-neutral-50 left-50/100 -translate-x-110/100"
  >
    <template #header>
      <div class="form text-5xl uppercase p-5">
        <p>{{ $t("welcome") }}</p>
      </div>
    </template>
    <template #body>
      <UForm class="form flex flex-col gap-5 p-3">
        <UFormField :label="$t('username')" name="Username" class="text-3xl">
          <UInput
            v-model="localUsername"
            placeholder="Jhon@13"
            class="w-full"
          />
        </UFormField>
        <UFormField :label="$t('password')" name="Username" class="text-3xl">
          <UInput
            v-model="localPassword"
            type="password"
            placeholder="******"
            class="w-full"
            :ui="{ input: 'size-200' }"
          />
        </UFormField>
      </UForm>
    </template>
    <template #footer>
      <div class="flex flex-col w-full form text-xl">
        <UButton
          :label="$t('login')"
          color="neutral"
          class="justify-center text-3xl uppercase"
          @click="submit"
        />
        <div class="w-full text-center pt-3">
          <p>
            {{ $t("singup-text") }}
            <a href="/register"><span class="text-emerald-400">{{ $t("singup") }}!</span></a>
          </p>
          <div class="w-full align-middle pt-2">
            <UIcon name="logos:facebook" class="text-3xl pl-10" />
            <UIcon name="logos:google-icon" class="text-3xl pr-10" />
          </div>
        </div>
      </div>
    </template>
  </UModal>
</template>

<script setup lang="ts">
const props = defineProps<{
  open: boolean;
  username: string;
  password: string;
}>();
const emit = defineEmits([
  "update:open",
  "update:username",
  "update:password",
  "submit",
]);

const localUsername = ref(props.username);
const localPassword = ref(props.password);
const localOpen = ref(props.open);

watch(localUsername, (val) => emit("update:username", val));
watch(localPassword, (val) => emit("update:password", val));

function submit() {
  emit("submit", {
    username: localUsername.value,
    password: localPassword.value,
  });
  emit("update:open", false);
}
</script>

<style scoped>
.form {
  font-family: "League Gothic";
}
</style>
