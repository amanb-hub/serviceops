"use client";

import { RefreshCw } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { KpiCard } from "@/components/card";

const KPIS = [
  "Open Tickets",
  "New Today",
  "Closed Today",
  "SLA Compliance",
  "P1 Tickets",
  "P2 Tickets",
  "Avg. TAT",
  ">48 Hours",
];

export default function DashboardPage() {
  return (
    <AppShell>
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-slate-900">Service Operations</h1>
          <p className="text-sm text-slate-500">
            Overview of service tickets and operations across all clients
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <select className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-600">
            <option>Today</option>
          </select>
          <select className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-600">
            <option>All Clients</option>
          </select>
          <select className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-600">
            <option>All Cities</option>
          </select>
          <button className="flex items-center gap-1.5 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-600 hover:bg-slate-50">
            <RefreshCw className="h-4 w-4" />
            Refresh
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
        {KPIS.map((label) => (
          <KpiCard key={label} label={label} value="--" />
        ))}
      </div>
    </AppShell>
  );
}
