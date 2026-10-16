export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const baseUrl = process.env.SUNERGY_API_URL ?? "http://127.0.0.1:8000";
    const endpoint = new URL("/health", baseUrl);
    if (!["http:", "https:"].includes(endpoint.protocol)) {
      throw new Error("Unsupported service protocol");
    }
    const upstream = await fetch(endpoint, {
      cache: "no-store",
      signal: AbortSignal.timeout(4000),
      redirect: "error",
    });
    if (!upstream.ok) {
      return new Response(null, { status: 503 });
    }
    return new Response(await upstream.text(), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "no-store",
      },
    });
  } catch {
    return new Response(null, { status: 503 });
  }
}
