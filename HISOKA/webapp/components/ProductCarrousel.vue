<template>
  <UModal
    v-model:open="localOpen"
    class="left-50/100 translate-x-10/100 bg-neutral-50/100 h-65/100"
    :dismissible="false"
    :overlay="false"
  >
    <template #content>
      <div class="flex flex-col">
        <div class="flex pl-20 pt-20">
          <div class="form text-7xl bg-[#474343] rounded-xl">
            <p class="p-2">H.I.S.O.K.A</p>
          </div>
        </div>
        <HisokaBoard class="w-full h-full pt-3" />
      </div>
    </template>
  </UModal>
</template>

<script setup lang="ts">
const props = defineProps<{
  open: boolean;
}>();
const localOpen = ref(props.open);
</script>

<style>
.form {
  font-family: "League Gothic";
}
</style>
