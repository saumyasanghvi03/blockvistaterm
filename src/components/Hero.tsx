export default function Hero() {
    return (
        <section className="hero-section">
            <div style={{ maxWidth: 1200, margin: '0 auto', padding: '0 2rem' }}>
                <h1 className="hero-title animate-fade-up delay-100">
                    Institutional Precision. <br />
                    <span className="gradient-text-accent">Retail Power.</span>
                </h1>

                <p className="hero-subtitle animate-fade-up delay-200">
                    India's institutional-grade multi-asset trading platform.
                    Real-time intelligence, advanced options analytics, and blockchain-grade audit trails.
                </p>

                <div className="animate-fade-up delay-300" style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '2rem' }}>
                    <a
                        href="https://agent.jotform.com/019aaff0529c75ba987ada46debdca400757"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn-primary"
                        style={{ padding: '1rem 2.5rem', fontSize: '1.1rem', textDecoration: 'none' }}
                    >
                        Request Demo
                    </a>
                    <a
                        href="https://agent.jotform.com/019aaff0529c75ba987ada46debdca400757"
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                            background: 'rgba(255,255,255,0.05)',
                            border: '1px solid var(--glass-border)',
                            color: 'white',
                            padding: '1rem 2.5rem',
                            borderRadius: '8px',
                            fontSize: '1.1rem',
                            cursor: 'pointer',
                            transition: 'all 0.3s',
                            textDecoration: 'none'
                        }}
                    >
                        Explore Docs
                    </a>
                </div>

                <div className="dashboard-preview animate-fade-up delay-300">
                    <img src="/assets/hero-dashboard.png" alt="BlockVista Dashboard" />
                </div>
            </div>

            <div className="stats-grid animate-fade-up delay-300">
                <div>
                    <div className="stat-value">50+</div>
                    <div className="stat-label">Broker Partners</div>
                </div>
                <div>
                    <div className="stat-value">₹1,00,000 Cr+</div>
                    <div className="stat-label">Daily Volume</div>
                </div>
                <div>
                    <div className="stat-value">99.99%</div>
                    <div className="stat-label">Uptime SLA</div>
                </div>
            </div>

            <div style={{ textAlign: 'center', marginTop: '3rem', color: 'var(--text-secondary)', fontSize: '1.2rem', fontStyle: 'italic' }}>
                "Trade Smarter. Act Faster. Think Ahead."
            </div>
        </section>
    );
}
