# Frontend scope
Read root AGENTS.md and relevant routing documents first.

Next.js owns presentation/forms only. Scientific, energy, and financial
calculations belong in Python. Use generated OpenAPI TypeScript from
`src/lib/api.generated.ts`; never maintain competing hand-written API schemas.
Keep secrets server-side; do not prefix credentials with NEXT_PUBLIC_. Builds
must not require the API or live weather/catalog services. Clearly label
unimplemented capabilities and do not display example numbers as simulation.
