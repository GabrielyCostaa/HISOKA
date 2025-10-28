// Pinia Store
import { defineStore } from "pinia";

interface State {
  username: string;
  email: string;
  userId: number | null;
  cookie: UserToken | null;
}

type UserSchema = {
  id: number;
  username: string;
  email: string;
};

type UserToken = {
  access_token: string;
  token_type: string;
  user_id: number;
};

export const useAuthUserStore = defineStore("authUser", {
  state: (): State => ({
    username: "",
    email: "",
    userId: null,
    cookie: null,
  }),

  getters: {
    fullName: (state) => `${state.username} ${state.email}`,
    loggedIn: (state) => state.cookie?.access_token !== undefined,
    token(state) {
      return state.cookie;
    },
    api: () => useNuxtApp().$api,
  },
  actions: {
    async hydrateFromCookie() {
      const cookie = useCookie<UserToken>("userCookie");
      this.setToken(cookie.value);
      this.loadUser();
    },

    async setToken(token: UserToken | null) {
      const cookie = useCookie<UserToken | null>("userCookie");
      cookie.value = token;
      refreshCookie("userCookie");
      this.cookie = token;
      this.api.options.headers.Authorization = "Bearer " + token?.access_token;
    },

    async clearToken() {
      delete this.api.options.headers.Authorization;
      await this.setToken(null);
    },

    async loadUser() {
      if (this.userId !== null) throw new Error("Already logged in");
      const res = await this.api.get<UserSchema>("/users/profile");
      this.updateUser(res);
    },

    updateUser(payload: UserSchema) {
      this.username = payload.username;
      this.email = payload.email;
      this.userId = payload.id;
    },

    async logout() {
      await this.clearToken();
      await this.hydrateFromCookie();
      this.clearUser();
    },

    clearUser() {
      this.$reset();
    },
  },
});
