export default function Features() {
    return (
        <section className="features-container">
            <h2 className="hero-title" style={{ fontSize: '2.5rem', marginBottom: '3rem', textAlign: 'center' }}>
                Unified Trading Hub
            </h2>

            <div className="features-grid">
                <div className="glass-card">
                    <div className="feature-icon">🇮🇳</div>
                    <h3 className="feature-title">Bharatiya Market Pulse</h3>
                    <p className="feature-desc">Proprietary India Sentiment Index (0–100) tracking real-time market psychology.</p>
                </div>
                <div className="glass-card">
                    <div className="feature-icon">⚛️</div>
                    <h3 className="feature-title">Quantum Analytics</h3>
                    <p className="feature-desc">Detect hidden institutional orders and liquidity layers with pattern recognition.</p>
                </div>
                <div className="glass-card">
                    <div className="feature-icon">🤖</div>
                    <h3 className="feature-title">AI Automation Bots</h3>
                    <p className="feature-desc">Momentum, Trend, and Mean Reversion strategies with real-time tracking.</p>
                </div>
                <div className="glass-card">
                    <div className="feature-icon">📊</div>
                    <h3 className="feature-title">Advanced Options</h3>
                    <p className="feature-desc">Complete F&O terminal with Greeks, IV surfaces, and strategy laboratory.</p>
                </div>
                <div className="glass-card">
                    <div className="feature-icon">🔗</div>
                    <h3 className="feature-title">Multi-Broker Hub</h3>
                    <p className="feature-desc">Seamless integration with Zerodha, Upstox, and other major brokers.</p>
                </div>
                <div className="glass-card">
                    <div className="feature-icon">🛡️</div>
                    <h3 className="feature-title">Risk & Compliance</h3>
                    <p className="feature-desc">Automated stop-loss management and volatility-adjusted risk limits.</p>
                </div>
            </div>
        </section>
    );
}
