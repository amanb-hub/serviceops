import { cn } from "@/lib/utils";

export function Card({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div
      className={cn(
        "rounded-xl border border-slate-200 bg-white p-5 shadow-sm",
        className
      )}
    >
      {children}
    </div>
  );
}

export function KpiCard({ label, value }: { label: string; value: string }) {
  return (
    <Card className="flex flex-col gap-1">
      <span className="text-xs font-medium uppercase tracking-wide text-slate-500">
        {label}
      </span>
      <span className="text-2xl font-semibold text-slate-900">{value}</span>
    </Card>
  );
}

export function PlaceholderModule({ title }: { title: string }) {
  return (
    <Card className="flex flex-col items-center justify-center gap-2 py-20 text-center">
      <h2 className="text-lg font-semibold text-slate-800">{title}</h2>
      <p className="text-sm text-slate-500">Module coming in the next development phase.</p>
    </Card>
  );
}
