import { ServiceStatus } from "@/components/service-status";

const capabilities = [
  {
    number: "01",
    title: "Module simulation",
    description:
      "Estimate module performance from explicit specifications, site conditions, and modeling assumptions.",
    stage: "Pending legacy reproduction",
  },
  {
    number: "02",
    title: "Measurement comparison",
    description:
      "Compare predictions with your measurements. Keep original observations and any fitted adjustments traceable.",
    stage: "Planned · optional inputs",
  },
  {
    number: "03",
    title: "Systems & financial assessment",
    description:
      "Extend to connected equipment, energy production, economic assumptions, and financing scenarios.",
    stage: "Planned · after module gates",
  },
  {
    number: "04",
    title: "Interactive site layout",
    description:
      "Place equipment on a map and define electrical connections as separate, explicit system decisions.",
    stage: "Future stage",
  },
];

export default function Home() {
  return (
    <>
      <a className="skip-link" href="#main">Skip to content</a>
      <div className="site-wrap">
        <header className="site-header">
          <a className="wordmark" href="#" aria-label="SUNERGY home">
            <span className="brand-icon" aria-hidden="true">✳</span>
            SUNERGY
          </a>
          <nav aria-label="Main navigation">
            <a href="#workspace">Workspace</a>
            <a href="#approach">Our approach</a>
          </nav>
          <span className="preview-label">Development preview</span>
        </header>

        <main id="main">
          <section className="hero" aria-labelledby="hero-title">
            <div className="hero-copy">
              <p className="eyebrow"><span aria-hidden="true" /> A clearer view of solar</p>
              <h1 id="hero-title">Every solar decision<br />starts with <em>evidence.</em></h1>
              <p className="hero-description">
                A future workspace for understanding PV performance — from a single
                module to the systems you build.
              </p>
              <a className="primary-link" href="#workspace">
                Explore the workspace <span aria-hidden="true">↗</span>
              </a>
            </div>
            <div className="solar-art" aria-hidden="true">
              <div className="orbit orbit-outer" />
              <div className="orbit orbit-inner" />
              <div className="sun" />
              <svg className="panel-illustration" viewBox="0 0 360 290" fill="none">
                <path d="M168 213V254L202 271M168 254L134 270" stroke="#557766" strokeWidth="7" strokeLinecap="round" />
                <path d="M60 82L263 43L316 194L113 234Z" fill="#173E34" stroke="#13382F" strokeWidth="7" strokeLinejoin="round" />
                <path d="M111 72L165 224M162 62L216 214M213 53L267 204M77 131L281 92M95 181L298 142" stroke="#A1BAAA" strokeWidth="3" />
                <path d="M60 82L263 43L316 194L113 234Z" stroke="#D0DDD2" strokeWidth="4" strokeLinejoin="round" />
              </svg>
              <span className="art-caption">Built on explicit inputs.<br />Designed for informed decisions.</span>
            </div>
          </section>

          <section className="foundation-note" aria-labelledby="preview-title">
            <span className="note-icon" aria-hidden="true">i</span>
            <div>
              <h2 id="preview-title">The foundation is here. The simulations are still ahead.</h2>
              <p>
                This preview does not calculate PV performance, accept measurements,
                or produce financial results. Legacy reproduction and scientific
                verification remain pending.
              </p>
            </div>
          </section>

          <section id="workspace" className="workspace-section" aria-labelledby="workspace-title">
            <div className="section-heading">
              <div>
                <p className="eyebrow">The workspace ahead</p>
                <h2 id="workspace-title">From specifications to perspective.</h2>
              </div>
              <span className="section-aside">Capabilities in development</span>
            </div>
            <div className="capability-grid">
              {capabilities.map((capability) => (
                <article className="capability" key={capability.number}>
                  <span className="capability-number">{capability.number}</span>
                  <h3>{capability.title}</h3>
                  <p>{capability.description}</p>
                  <span className="capability-stage">{capability.stage}</span>
                </article>
              ))}
            </div>
          </section>

          <section id="approach" className="approach-section" aria-labelledby="approach-title">
            <div>
              <p className="eyebrow">Transparent by design</p>
              <h2 id="approach-title">Know what goes into<br />every projection.</h2>
              <p className="approach-description">
                Expected performance and measured performance answer different
                questions. SUNERGY will keep them distinct, with visible assumptions
                and traceable sources.
              </p>
            </div>
            <div className="approach-details">
              <details>
                <summary>What will a simulation need?</summary>
                <p>
                  Site coordinates, catalog or manual module specifications, and the
                  weather, orientation, and operating inputs required by the chosen
                  model. Empirical measurements will be optional.
                </p>
              </details>
              <details>
                <summary>How will confidence be established?</summary>
                <p>
                  Reproducing legacy outputs, checking scientific formulations, and
                  comparing predictions with measurements are separate gates. A
                  successful comparison with a legacy result does not establish
                  physical accuracy.
                </p>
              </details>
              <details>
                <summary>How will adjustments stay traceable?</summary>
                <p>
                  Future calibration will retain original measurements and the
                  unadjusted baseline, identify fitted parameters, and distinguish
                  fitting data from held-out evaluation where available.
                </p>
              </details>
            </div>
          </section>

          <ServiceStatus />
        </main>

        <footer className="site-footer">
          <span className="footer-brand">SUNERGY</span>
          <p>Clear assumptions. Traceable evidence. Better solar decisions.</p>
          <span>Foundation · 0.1</span>
        </footer>
      </div>
    </>
  );
}
