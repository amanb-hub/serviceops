import type { Metadata } from "next";
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: "ServiceOps — Multi-Client Service Management Platform",
  description: "Multi-Client Service Management Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
