"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Ticket,
  Building2,
  Truck,
  Wrench,
  Boxes,
  AlarmClock,
  BarChart3,
  Sparkles,
  Bell,
  Settings,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Tickets", href: "/tickets", icon: Ticket },
  { label: "Clients", href: "/clients", icon: Building2 },
  { label: "Vehicles", href: "/vehicles", icon: Truck },
  { label: "Technicians", href: "/technicians", icon: Wrench },
  { label: "Parts & Inventory", href: "/inventory", icon: Boxes },
  { label: "SLA & Escalations", href: "/sla", icon: AlarmClock },
  { label: "Reports", href: "/reports", icon: BarChart3 },
  { label: "AI Insights", href: "/ai-insights", icon: Sparkles },
  { label: "Notifications", href: "/notifications", icon: Bell },
  { label: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden lg:flex lg:w-64 lg:flex-col bg-navy-900 text-slate-200 min-h-screen border-r border-navy-800">
      <div className="px-5 py-6 border-b border-navy-800">
        <p className="text-lg font-semibold text-white tracking-tight">ServiceOps</p>
        <p className="text-xs text-slate-400 mt-0.5">Multi-Client Service Platform</p>
      </div>

      <nav className="flex-1 overflow-y-auto py-4 px-2 space-y-0.5">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const active = pathname?.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                active
                  ? "bg-blue-600 text-white"
                  : "text-slate-300 hover:bg-navy-800 hover:text-white"
              )}
            >
              <Icon className="h-4 w-4 shrink-0" />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
