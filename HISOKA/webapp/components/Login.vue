<script setup lang="ts">
const { locales, setLocale } = useI18n();
const runtimeConfig = useRuntimeConfig();

const emit = defineEmits(["close", "success"]);
const toast = useToast();
const userCookie = useCookie("userCookie"); // cookie seguro
const loggedIn = computed(() => !!userCookie.value);
const open = ref(!userCookie.value ? true : false);

const state = reactive({
  email: "string",
  password: "string",
});

const validate = (state: { email: any; password: any }) => {
  const errors = [];
  if (!state.email)
    errors.push({ path: "email", message: "Email é obrigatório" });
  if (!state.password)
    errors.push({ path: "password", message: "Senha é obrigatória" });
  return errors;
};

const onSubmit = async () => {
  try {
    const formData = new URLSearchParams();
    formData.append("grant_type", "password");
    formData.append("username", state.email);
    formData.append("password", state.password);

    const response = await fetch(runtimeConfig.public.apiBase + "/auth/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Accept: "application/json",
      },
      body: formData,
    });

    open.value = !response.ok;

    if (!response.ok) {
      const errorData = await response.json();
      toast.add({
        title: "Erro de login",
        description: errorData.message || "Verifique suas credenciais",
        color: "error",
        id: "modal-dismiss",
      });
      return;
    }

    const result = await response.json();

    userCookie.value = result;
    refreshCookie("userCookie");

    toast.add({ title: "Login bem-sucedido", color: "success" });

    emit("success", result);
    emit("close", false);
  } catch (err) {
    console.error(err);
    toast.add({
      title: "Erro inesperado",
      description: "Tente novamente mais tarde",
      color: "error",
      id: "modal-dismiss",
    });
  }
};
</script>

<template>
  <UModal v-model:open="open" :dismissible="false">
    <template #content>
      <UForm
        :validate="validate"
        :state="state"
        class="flex flex-col gap-5 p-10"
        @submit="onSubmit"
      >
        <UFormField label="Email" name="email">
          <UInput
            v-model="state.email"
            placeholder="Digite seu e-mail"
            class="w-full"
          />
        </UFormField>

        <UFormField label="Senha" name="password">
          <UInput
            v-model="state.password"
            type="password"
            placeholder="Digite sua senha"
            class="w-full"
          />
        </UFormField>

        <UCheckbox label="lembrar-se" />
        <UButton
          color="primary"
          type="submit"
          label="Entrando"
          class="w-full justify-center"
        />
        <h1>{{ $t("welcome") }}</h1>
      </UForm>
    </template>
  </UModal>
</template>
