export default function Terminal() {
    return (
        <section className="content-section">
            <div className="content-text">
                <h2 style={{ fontSize: '2.5rem', marginBottom: '1.5rem' }}>Multi-Asset Coverage</h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', lineHeight: 1.6 }}>
                    Trade across all major asset classes with institutional-grade latency and analytics.
                </p>

                <ul className="check-list">
                    <li className="check-item">
                        <span className="check-icon">✓</span> Equity (NSE, BSE)
                    </li>
                    <li className="check-item">
                        <span className="check-icon">✓</span> Futures & Options (F&O)
                    </li>
                    <li className="check-item">
                        <span className="check-icon">✓</span> Commodities (MCX)
                    </li>
                    <li className="check-item">
                        <span className="check-icon">✓</span> Forex (FX)
                    </li>
                    <li className="check-item">
                        <span className="check-icon">✓</span> Options Greeks & IV Surfaces
                    </li>
                    <li className="check-item">
                        <span className="check-icon">✓</span> Real-time Market Breadth
                    </li>
                </ul>
            </div>

            <div className="content-image">
                <img src="/assets/market-depth.png" alt="Multi-Asset Coverage Chart" />
            </div>
        </section>
    );
}
