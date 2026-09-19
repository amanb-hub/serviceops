"use client";

import { Sidebar } from "@/components/sidebar";
import { Topbar } from "@/components/topbar";
import { useCurrentUser } from "@/hooks/use-current-user";

export function AppShell({ children }: { children: React.ReactNode }) {
  const { user, loading } = useCurrentUser();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <p className="text-sm text-slate-500">Loading ServiceOps…</p>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Topbar user={user} />
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}
