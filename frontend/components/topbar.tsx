"use client";

import { LogOut, UserCircle } from "lucide-react";
import type { User } from "@/types";
import { logout } from "@/lib/auth";

export function Topbar({ user }: { user: User | null }) {
  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-3">
      <div />
      <div className="flex items-center gap-4">
        {user && (
          <div className="flex items-center gap-2 text-sm">
            <UserCircle className="h-6 w-6 text-slate-400" />
            <div className="leading-tight">
              <p className="font-medium text-slate-900">{user.name}</p>
              <p className="text-xs text-slate-500">{user.role.name.replace(/_/g, " ")}</p>
            </div>
          </div>
        )}
        <button
          onClick={logout}
          className="flex items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-50"
        >
          <LogOut className="h-4 w-4" />
          Logout
        </button>
      </div>
    </header>
  );
}
