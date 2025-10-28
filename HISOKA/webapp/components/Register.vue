<template>
  <div class="w-screen h-screen grid grid-cols-2 form">
    <div class="text-center justify-center pr-50 pl-50">
      <div class="h-6/8 bg-neutral-50 rounded-b-[10rem] drop-shadow-2xl">
        <div class="p-15">
          <div class="form bg-neutral rounded-xl">
            <p class="p-2 text-9xl">H.I.S.O.K.A</p>
          </div>
        </div>
        <HisokaBoard
          class="w-7/6 -translate-x-3 -translate-y-20"
        ></HisokaBoard>
      </div>
    </div>
    <div class="p-20 flex flex-col">
      <div class="text-center text-6xl p-10">
        <p>{{ $t("singin-title") }}</p>
      </div>
      <UForm
        :schema="schema"
        :state="state"
        @submit="onSubmit"
        @error="onError"
        class="space-y-5"
      >
        <div class="text-3xl">
          <p>{{ $t("fullname") }}</p>
          <UFormField name="fullname">
            <UInput
              v-model="state.fullname"
              placeholder="Jhon brown"
              class="w-full"
              size="xl"
            />
          </UFormField>
        </div>
        <div class="text-3xl">
          <p>{{ $t("username") }}</p>
          <UFormField name="username">
            <UInput
              v-model="state.username"
              placeholder="Jhon@13"
              class="w-full"
              size="xl"
            />
          </UFormField>
        </div>
        <div class="text-3xl">
          <p>{{ $t("email") }}</p>
          <UFormField name="email">
            <UInput
              v-model="state.email"
              placeholder="Jhon@gmai.com"
              class="w-full"
              size="xl"
            />
          </UFormField>
        </div>
        <div class="text-3xl">
          <p>{{ $t("password") }}</p>
          <UFormField name="password">
            <UInput
              v-model="state.password"
              type="password"
              placeholder="******"
              class="w-full"
              size="xl"
            />
          </UFormField>
        </div>
        <div class="text-3xl">
          <p>{{ $t("confirm_password") }}</p>
          <UFormField name="confirm_password">
            <UInput
              v-model="state.confirm_password"
              type="password"
              placeholder="******"
              class="w-full"
              size="xl"
            />
          </UFormField>
        </div>
        <div class="text-center">
          <UButton
            :label="$t('singup')"
            type="submit"
            color="neutral"
            class="justify-center text-3xl uppercase w-1/2"
          />
          <p class="p-2 text-3xl">
            {{ $t("singin-text") }}
            <a href="/login"><span class="text-emerald-400">{{ $t("singin") }}!</span></a>          </p>
          <UIcon name="logos:facebook" class="text-3xl pl-10" />
          <UIcon name="logos:google-icon" class="text-3xl pr-10" />
        </div>
      </UForm>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { FormError, FormErrorEvent, FormSubmitEvent } from "#ui/types";
const toast = useToast()
import * as v from "valibot"

const schema = v.pipe(
  v.object({
    fullname: v.pipe(v.string(), v.minLength(8, "Você deve preencher seu sobrenome")),
    username: v.pipe(v.string(),v.minLength(4, "Seu nome de usuário deve ter no minimo quatro letras")),
    email: v.pipe(v.string(), v.email('Email Inválido')),
    password: v.pipe(v.string(), v.minLength(8, 'A senha precisa ter no mínimo oito caracteres')),
    confirm_password: v.pipe(v.string(), v.minLength(8, 'A senha precisa ter no mínimo oito caracteres'))
  }),
  v.forward(
    v.check(({ password, confirm_password}) => password == confirm_password, 'As senhas não coincidem'),
    ["confirm_password"]
  )
);

type Schema = v.InferOutput<typeof schema>

const state = reactive({
  fullname: "",
  username: "",
  email: "",
  password: "",
  confirm_password: "",
});

type User = {
  user_id: number;
  username: string;
  email: string;
};

const runtimeConfig = useRuntimeConfig();

async function onSubmit(event: FormSubmitEvent<any>) {
  const formData = {
    "username":event.data.username,
    "email":event.data.email,
    "password":event.data.password,
  }

  $fetch<User>(runtimeConfig.public.apiBase + "/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: formData,
  })
    .then(async (result) => {
      navigateTo("/login");
    })
    .catch(() => alert("Deu Merda"));

    console.log(event.data)
}

async function onError(event: FormErrorEvent) {
  const element = document.getElementById(event.errors[0].id);
  console.log("ERO DO BOM", element);
  
  element?.focus();
  element?.scrollIntoView({ behavior: "smooth", block: "center" });
}
</script>

<style scoped>
.form {
  font-family: "League Gothic";
}
</style>
