"use client";

import { useState } from "react";
import type { components } from "@/lib/api.generated";

type HealthResponse = components["schemas"]["HealthResponse"];

export function ServiceStatus() {
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState("Connection has not been checked.");

  async function checkConnection() {
    setPending(true);
    setMessage("Checking the application service…");
    try {
      const response = await fetch("/api/health", {
        cache: "no-store",
        signal: AbortSignal.timeout(6000),
      });
      if (!response.ok) throw new Error("Service unavailable");
      const health: HealthResponse = await response.json();
      if (health.status !== "ok" || health.service !== "sunergy") {
        throw new Error("Unexpected health response");
      }
      setMessage("Application service is reachable. Simulation remains unavailable.");
    } catch {
      setMessage("Application service is unavailable. The preview is still available.");
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="service-status" aria-labelledby="service-title">
      <div>
        <h2 id="service-title">Application service</h2>
        <p role="status" aria-live="polite">{message}</p>
      </div>
      <button type="button" onClick={checkConnection} disabled={pending}>
        {pending ? "Checking…" : "Check connection"}
        <span aria-hidden="true">↗</span>
      </button>
    </section>
  );
}
