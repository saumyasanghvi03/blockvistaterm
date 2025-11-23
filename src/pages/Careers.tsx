export default function Careers() {
    return (
        <div style={{ paddingTop: '120px', paddingBottom: '80px' }} className="container">
            <h1 className="hero-title" style={{ textAlign: 'center', marginBottom: '2rem' }}>Join Our Mission</h1>
            <p style={{ textAlign: 'center', color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto 4rem' }}>
                We're building the future of financial analytics in India. Come help us democratize institutional-grade tools.
            </p>

            <div className="glass-card" style={{ maxWidth: '800px', margin: '0 auto' }}>
                <h3 style={{ marginBottom: '2rem' }}>Open Positions</h3>

                <div style={{ borderBottom: '1px solid var(--glass-border)', paddingBottom: '1.5rem', marginBottom: '1.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                            <h4 style={{ margin: 0, fontSize: '1.2rem' }}>Senior Frontend Engineer</h4>
                            <p style={{ margin: '0.5rem 0 0', color: 'var(--text-secondary)' }}>Remote • Full-time</p>
                        </div>
                        <button className="btn-secondary">Apply</button>
                    </div>
                </div>

                <div style={{ borderBottom: '1px solid var(--glass-border)', paddingBottom: '1.5rem', marginBottom: '1.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                            <h4 style={{ margin: 0, fontSize: '1.2rem' }}>Quantitative Analyst</h4>
                            <p style={{ margin: '0.5rem 0 0', color: 'var(--text-secondary)' }}>Mumbai • Hybrid</p>
                        </div>
                        <button className="btn-secondary">Apply</button>
                    </div>
                </div>

                <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                            <h4 style={{ margin: 0, fontSize: '1.2rem' }}>Product Designer</h4>
                            <p style={{ margin: '0.5rem 0 0', color: 'var(--text-secondary)' }}>Remote • Contract</p>
                        </div>
                        <button className="btn-secondary">Apply</button>
                    </div>
                </div>
            </div>
        </div>
    );
}
