export default function Products() {
    return (
        <div style={{ paddingTop: '120px', paddingBottom: '4rem', maxWidth: '1200px', margin: '0 auto', paddingLeft: '2rem', paddingRight: '2rem' }}>

            {/* Overview Hero */}
            <section style={{ textAlign: 'center', marginBottom: '6rem' }}>
                <h1 className="hero-title">AI Market Intelligence Suite</h1>
                <p style={{ color: 'var(--text-secondary)', fontSize: '1.3rem', maxWidth: '900px', margin: '0 auto', lineHeight: 1.6 }}>
                    BlockVista Terminal offers unified analytics, algo bots, and deep order-flow intelligence designed for banks, brokers, traders, and professional market participants.
                </p>
            </section>

            {/* Deployment Architecture (New Section) */}
            <section style={{ marginBottom: '6rem' }}>
                <h2 className="hero-title" style={{ fontSize: '2.5rem', marginBottom: '3rem', textAlign: 'center' }}>Deployment Architecture</h2>
                <div className="features-grid">
                    <div className="glass-card">
                        <div className="feature-icon">☁️</div>
                        <h3 className="feature-title">SaaS</h3>
                        <p className="feature-desc">Fast deployment (48 hours), managed infrastructure, automatic updates.</p>
                    </div>
                    <div className="glass-card">
                        <div className="feature-icon">🏢</div>
                        <h3 className="feature-title">Private Cloud</h3>
                        <p className="feature-desc">Maximum control, dedicated hardware security, custom integration, enhanced SLAs.</p>
                    </div>
                    <div className="glass-card">
                        <div className="feature-icon">🛠️</div>
                        <h3 className="feature-title">White-Label SDK</h3>
                        <p className="feature-desc">Brand integration, embeddable PWA/widgets, API-first design.</p>
                    </div>
                </div>
            </section>

            {/* Specialized Modules (Updated Features) */}
            <section style={{ marginBottom: '6rem' }}>
                <h2 className="hero-title" style={{ fontSize: '2.5rem', marginBottom: '3rem', textAlign: 'center' }}>Specialized Modules</h2>
                <div className="features-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))' }}>
                    <div className="glass-card" style={{ borderColor: 'var(--accent-blue)' }}>
                        <h3 className="feature-title">🇮🇳 Bharatiya Market Pulse (BMP)</h3>
                        <p className="feature-desc">Proprietary India Sentiment Index (0–100) tracking real-time market psychology across domestic exchanges.</p>
                        <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                            Combines NIFTY, SENSEX & India VIX • Bharat Udaan → Bharat Mandhi
                        </div>
                    </div>
                    <div className="glass-card">
                        <h3 className="feature-title">⚛️ Quantum Analytics</h3>
                        <p className="feature-desc">Detects hidden institutional orders and liquidity layers using advanced pattern recognition algorithms.</p>
                    </div>
                    <div className="glass-card">
                        <h3 className="feature-title">🧪 Strategy Lab</h3>
                        <p className="feature-desc">Multi-asset backtester with institutional-grade order-flow and microstructure analytics.</p>
                    </div>
                    <div className="glass-card">
                        <h3 className="feature-title">⛓️ Permissioned Blockchain</h3>
                        <p className="feature-desc">Tamper-proof audit trails using immutable ledger hashes, keeping market data off-chain for privacy.</p>
                    </div>
                    <div className="glass-card">
                        <h3 className="feature-title">🤖 AI Automation Bots</h3>
                        <p className="feature-desc">Momentum, Trend, Mean Reversion, and Scalper Pro strategies with customizable parameters.</p>
                    </div>
                    <div className="glass-card">
                        <h3 className="feature-title">⚡ HFT Mode</h3>
                        <p className="feature-desc">20-Level Market Depth with 2–15 ms Latency for high-frequency execution.</p>
                    </div>
                </div>
            </section>

            {/* Pain Points (Kept from previous update) */}
            <section style={{ marginBottom: '6rem' }}>
                <h2 className="hero-title" style={{ fontSize: '2.5rem', marginBottom: '3rem', textAlign: 'center' }}>Current Ecosystem Pain Points</h2>
                <div className="features-grid">
                    <div className="glass-card">
                        <div className="feature-icon">🧩</div>
                        <h3 className="feature-title">Disconnected Tools</h3>
                        <p className="feature-desc">Market participants use 7-10 different applications daily, leading to missed opportunities and inefficiency.</p>
                    </div>
                    <div className="glass-card">
                        <div className="feature-icon">📚</div>
                        <h3 className="feature-title">Manual Research</h3>
                        <p className="feature-desc">Fundamental and technical analysis is scattered across Telegram, YouTube, PDFs, and proprietary sources.</p>
                    </div>
                    <div className="glass-card">
                        <div className="feature-icon">🤖</div>
                        <h3 className="feature-title">No AI Execution</h3>
                        <p className="feature-desc">Traders rely on outdated methods without intelligent, AI-driven signals for execution.</p>
                    </div>
                    <div className="glass-card">
                        <div className="feature-icon">🧊</div>
                        <h3 className="feature-title">Hidden Orders</h3>
                        <p className="feature-desc">Institutional "Iceberg" orders remain invisible, keeping traders blind to significant liquidity and order flow.</p>
                    </div>
                </div>
            </section>

            {/* Business Impact */}
            <section style={{ marginBottom: '6rem' }}>
                <h2 className="hero-title" style={{ fontSize: '2.5rem', marginBottom: '3rem', textAlign: 'center' }}>Business Impact</h2>
                <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem' }}>
                    <div className="glass-card" style={{ textAlign: 'center' }}>
                        <div className="stat-value" style={{ color: 'var(--accent-blue)' }}>3x</div>
                        <div className="stat-label">RM Productivity</div>
                    </div>
                    <div className="glass-card" style={{ textAlign: 'center' }}>
                        <div className="stat-value" style={{ color: 'var(--accent-purple)' }}>50%</div>
                        <div className="stat-label">Churn Reduction</div>
                    </div>
                    <div className="glass-card" style={{ textAlign: 'center' }}>
                        <div className="stat-value" style={{ color: 'var(--accent-cyan)' }}>3x</div>
                        <div className="stat-label">Advisory Scale</div>
                    </div>
                    <div className="glass-card" style={{ textAlign: 'center' }}>
                        <div className="stat-value" style={{ color: '#10b981' }}>5x</div>
                        <div className="stat-label">Research Speed</div>
                    </div>
                </div>
            </section>

            {/* Conclusion */}
            <section style={{ textAlign: 'center', padding: '4rem', background: 'rgba(255,255,255,0.02)', borderRadius: '20px', border: '1px solid var(--glass-border)' }}>
                <h2 className="hero-title" style={{ fontSize: '2rem', marginBottom: '2rem' }}>The Future of Financial Market Intelligence</h2>
                <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', flexWrap: 'wrap', marginBottom: '3rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ color: 'var(--accent-blue)' }}>✓</span> Deploy Fast
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ color: 'var(--accent-purple)' }}>✓</span> Scale Intelligence
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ color: 'var(--accent-cyan)' }}>✓</span> Win Markets
                    </div>
                </div>
                <a
                    href="https://agent.jotform.com/019aaff0529c75ba987ada46debdca400757"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-primary"
                    style={{ padding: '1rem 3rem', textDecoration: 'none', display: 'inline-block' }}
                >
                    Get Started Now
                </a>
            </section>

        </div>
    );
}
