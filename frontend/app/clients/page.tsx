"use client";

import { useEffect, useState } from "react";
import { Plus, X } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { Card } from "@/components/card";
import { apiFetch, ApiError } from "@/lib/api";
import type { Client } from "@/types";

export default function ClientsPage() {
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [contactName, setContactName] = useState("");
  const [contactEmail, setContactEmail] = useState("");

  async function loadClients() {
    setLoading(true);
    try {
      const data = await apiFetch<Client[]>("/clients");
      setClients(data);
    } catch (err) {
      // Non-fatal for this step — the shell still renders
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadClients();
  }, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await apiFetch<Client>("/clients", {
        method: "POST",
        body: JSON.stringify({
          name,
          code,
          contact_name: contactName || null,
          contact_email: contactEmail || null,
        }),
      });
      setShowForm(false);
      setName("");
      setCode("");
      setContactName("");
      setContactEmail("");
      await loadClients();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to create client");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AppShell>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-slate-900">Clients</h1>
          <p className="text-sm text-slate-500">Manage the clients served on this platform</p>
        </div>
        <button
          onClick={() => setShowForm((s) => !s)}
          className="flex items-center gap-1.5 rounded-lg bg-blue-600 px-3 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          {showForm ? <X className="h-4 w-4" /> : <Plus className="h-4 w-4" />}
          {showForm ? "Cancel" : "New Client"}
        </button>
      </div>

      {showForm && (
        <Card className="mb-6">
          <form onSubmit={handleCreate} className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Name</label>
              <input
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Code</label>
              <input
                required
                value={code}
                onChange={(e) => setCode(e.target.value.toUpperCase())}
                className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Contact Name
              </label>
              <input
                value={contactName}
                onChange={(e) => setContactName(e.target.value)}
                className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Contact Email
              </label>
              <input
                type="email"
                value={contactEmail}
                onChange={(e) => setContactEmail(e.target.value)}
                className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
            </div>

            {error && (
              <p className="sm:col-span-2 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
                {error}
              </p>
            )}

            <div className="sm:col-span-2">
              <button
                type="submit"
                disabled={submitting}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-60"
              >
                {submitting ? "Creating…" : "Create Client"}
              </button>
            </div>
          </form>
        </Card>
      )}

      <Card className="p-0 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-5 py-3">Name</th>
              <th className="px-5 py-3">Code</th>
              <th className="px-5 py-3">Contact</th>
              <th className="px-5 py-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {loading && (
              <tr>
                <td colSpan={4} className="px-5 py-6 text-center text-slate-400">
                  Loading…
                </td>
              </tr>
            )}
            {!loading && clients.length === 0 && (
              <tr>
                <td colSpan={4} className="px-5 py-6 text-center text-slate-400">
                  No clients yet.
                </td>
              </tr>
            )}
            {clients.map((c) => (
              <tr key={c.id}>
                <td className="px-5 py-3 font-medium text-slate-900">{c.name}</td>
                <td className="px-5 py-3 text-slate-500">{c.code}</td>
                <td className="px-5 py-3 text-slate-500">{c.contact_name || "—"}</td>
                <td className="px-5 py-3">
                  <span className="rounded-full bg-green-50 px-2 py-0.5 text-xs font-medium text-green-700">
                    {c.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </AppShell>
  );
}
