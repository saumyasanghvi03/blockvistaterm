export default function About() {
    return (
        <div style={{ paddingTop: '120px', paddingBottom: '4rem', maxWidth: '1200px', margin: '0 auto', paddingLeft: '2rem', paddingRight: '2rem' }}>
            <h1 className="hero-title">About BlockVista</h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '1.2rem', lineHeight: 1.6, maxWidth: '800px' }}>
                BlockVista Terminal is India's leading institutional-grade multi-asset trading platform.
                We empower brokers, hedge funds, and professional traders with real-time intelligence,
                advanced analytics, and enterprise-grade security.
            </p>

            <div style={{ marginTop: '4rem', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
                <div className="glass-card">
                    <h3 className="feature-title">Our Mission</h3>
                    <p className="feature-desc">To democratize institutional-grade trading technology for the Indian market.</p>
                </div>
                <div className="glass-card">
                    <h3 className="feature-title">Our Vision</h3>
                    <p className="feature-desc">To be the backbone of India's financial infrastructure.</p>
                </div>
            </div>
        </div>
    );
}
