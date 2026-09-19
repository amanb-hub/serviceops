"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import type { User } from "@/types";
import { fetchCurrentUser, getStoredUser, isAuthenticated } from "@/lib/auth";

export function useCurrentUser() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(getStoredUser());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace("/login");
      return;
    }

    fetchCurrentUser()
      .then(setUser)
      .catch(() => router.replace("/login"))
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { user, loading };
}
