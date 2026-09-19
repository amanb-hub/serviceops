import type { TokenResponse, User } from "@/types";
import { apiFetch } from "@/lib/api";

const TOKEN_KEY = "serviceops_token";
const USER_KEY = "serviceops_user";

export async function login(email: string, password: string): Promise<TokenResponse> {
  const data = await apiFetch<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  if (typeof window !== "undefined") {
    window.localStorage.setItem(TOKEN_KEY, data.access_token);
    window.localStorage.setItem(USER_KEY, JSON.stringify(data.user));
  }
  return data;
}

export function logout(): void {
  if (typeof window !== "undefined") {
    window.localStorage.removeItem(TOKEN_KEY);
    window.localStorage.removeItem(USER_KEY);
    window.location.href = "/login";
  }
}

export function getStoredUser(): User | null {
  if (typeof window === "undefined") return null;
  const raw = window.localStorage.getItem(USER_KEY);
  return raw ? (JSON.parse(raw) as User) : null;
}

export function isAuthenticated(): boolean {
  if (typeof window === "undefined") return false;
  return Boolean(window.localStorage.getItem(TOKEN_KEY));
}

export async function fetchCurrentUser(): Promise<User> {
  const user = await apiFetch<User>("/auth/me");
  if (typeof window !== "undefined") {
    window.localStorage.setItem(USER_KEY, JSON.stringify(user));
  }
  return user;
}
