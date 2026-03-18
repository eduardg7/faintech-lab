import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Memory Management for Production Systems | Faintech Lab",
  description: "Production-grade memory for autonomous AI agents. Persistent state, multi-modal storage, and OS-level integration. Join beta.",
};

export default function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
