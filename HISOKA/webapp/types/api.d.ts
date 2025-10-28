import type { mande } from "mande";

declare module "#app" {
  interface NuxtApp {
    $api: ReturnType<typeof mande>;
  }
}

declare module "vue" {
  interface ComponentCustomProperties {
    $api: ReturnType<typeof mande>;
  }
}
