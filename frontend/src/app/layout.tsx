import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SUNERGY · PV planning, grounded in evidence",
  description:
    "Development preview of SUNERGY, a future workspace for transparent PV simulation and evaluation.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
