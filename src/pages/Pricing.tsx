import { useState } from 'react';

export default function Pricing() {
    const [segment, setSegment] = useState<'retail' | 'broker'>('retail');
    const jotformLink = "https://agent.jotform.com/019aaff0529c75ba987ada46debdca400757";

    return (
        <div style={{ paddingTop: '120px', paddingBottom: '4rem', maxWidth: '1200px', margin: '0 auto', paddingLeft: '2rem', paddingRight: '2rem', textAlign: 'center' }}>
            <h1 className="hero-title">Transparent Pricing</h1>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '3rem' }}>
                Institutional-grade tools for every market participant.
            </p>

            {/* Segment Toggle */}
            <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginBottom: '4rem' }}>
                <button
                    onClick={() => setSegment('retail')}
                    style={{
                        padding: '0.8rem 2rem',
                        borderRadius: '30px',
                        background: segment === 'retail' ? 'var(--accent-blue)' : 'rgba(255,255,255,0.05)',
                        border: '1px solid var(--glass-border)',
                        color: 'white',
                        cursor: 'pointer',
                        fontSize: '1.1rem',
                        transition: 'all 0.3s'
                    }}
                >
                    Retail Traders
                </button>
                <button
                    onClick={() => setSegment('broker')}
                    style={{
                        padding: '0.8rem 2rem',
                        borderRadius: '30px',
                        background: segment === 'broker' ? 'var(--accent-purple)' : 'rgba(255,255,255,0.05)',
                        border: '1px solid var(--glass-border)',
                        color: 'white',
                        cursor: 'pointer',
                        fontSize: '1.1rem',
                        transition: 'all 0.3s'
                    }}
                >
                    Brokers & Enterprise
                </button>
            </div>

            {/* Retail Pricing */}
            {segment === 'retail' && (
                <div className="features-grid animate-fade-up">
                    <div className="glass-card">
                        <h3 className="feature-title">Starter</h3>
                        <div className="stat-value" style={{ fontSize: '2.5rem', margin: '1rem 0' }}>₹999<span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>/mo</span></div>
                        <p className="feature-desc">Essential analytics for smart trading.</p>
                        <ul className="check-list" style={{ textAlign: 'left', margin: '2rem 0' }}>
                            <li className="check-item"><span className="check-icon">✓</span> Live Portfolio Sync</li>
                            <li className="check-item"><span className="check-icon">✓</span> Basic Charting</li>
                            <li className="check-item"><span className="check-icon">✓</span> 5 Watchlists</li>
                        </ul>
                        <a href={jotformLink} target="_blank" rel="noopener noreferrer" className="btn-primary" style={{ width: '100%', background: 'rgba(255,255,255,0.1)', display: 'block', textDecoration: 'none', textAlign: 'center' }}>Get Started</a>
                    </div>

                    <div className="glass-card" style={{ borderColor: 'var(--accent-blue)', boxShadow: '0 0 30px rgba(59, 130, 246, 0.2)' }}>
                        <div style={{ position: 'absolute', top: 0, right: 0, background: 'var(--accent-blue)', padding: '0.2rem 1rem', borderRadius: '0 0 0 10px', fontSize: '0.8rem', fontWeight: 'bold' }}>POPULAR</div>
                        <h3 className="feature-title">Pro</h3>
                        <div className="stat-value" style={{ fontSize: '2.5rem', margin: '1rem 0' }}>₹2,499<span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>/mo</span></div>
                        <p className="feature-desc">Advanced tools for serious traders.</p>
                        <ul className="check-list" style={{ textAlign: 'left', margin: '2rem 0' }}>
                            <li className="check-item"><span className="check-icon">✓</span> Advanced Options Greeks</li>
                            <li className="check-item"><span className="check-icon">✓</span> AI Momentum Bots</li>
                            <li className="check-item"><span className="check-icon">✓</span> Multi-Broker Hub</li>
                            <li className="check-item"><span className="check-icon">✓</span> Real-time Data</li>
                        </ul>
                        <a href={jotformLink} target="_blank" rel="noopener noreferrer" className="btn-primary" style={{ width: '100%', display: 'block', textDecoration: 'none', textAlign: 'center' }}>Start Trial</a>
                    </div>

                    <div className="glass-card">
                        <h3 className="feature-title">Elite</h3>
                        <div className="stat-value" style={{ fontSize: '2.5rem', margin: '1rem 0' }}>₹4,999<span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>/mo</span></div>
                        <p className="feature-desc">Full institutional power.</p>
                        <ul className="check-list" style={{ textAlign: 'left', margin: '2rem 0' }}>
                            <li className="check-item"><span className="check-icon">✓</span> HFT Mode (2-15ms)</li>
                            <li className="check-item"><span className="check-icon">✓</span> Iceberg Detector</li>
                            <li className="check-item"><span className="check-icon">✓</span> Strategy Lab Backtesting</li>
                            <li className="check-item"><span className="check-icon">✓</span> Priority Support</li>
                        </ul>
                        <a href={jotformLink} target="_blank" rel="noopener noreferrer" className="btn-primary" style={{ width: '100%', background: 'rgba(255,255,255,0.1)', display: 'block', textDecoration: 'none', textAlign: 'center' }}>Contact Sales</a>
                    </div>
                </div>
            )}

            {/* Broker Pricing */}
            {segment === 'broker' && (
                <div className="features-grid animate-fade-up">
                    <div className="glass-card">
                        <h3 className="feature-title">Lite</h3>
                        <div className="stat-value" style={{ fontSize: '2.5rem', margin: '1rem 0' }}>₹25k<span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>/mo</span></div>
                        <p className="feature-desc">Core platform for boutique firms.</p>
                        <ul className="check-list" style={{ textAlign: 'left', margin: '2rem 0' }}>
                            <li className="check-item"><span className="check-icon">✓</span> White-Label Basic</li>
                            <li className="check-item"><span className="check-icon">✓</span> Client Portfolio View</li>
                            <li className="check-item"><span className="check-icon">✓</span> Standard Support</li>
                        </ul>
                        <a href={jotformLink} target="_blank" rel="noopener noreferrer" className="btn-primary" style={{ width: '100%', background: 'rgba(255,255,255,0.1)', display: 'block', textDecoration: 'none', textAlign: 'center' }}>Contact Sales</a>
                    </div>

                    <div className="glass-card" style={{ borderColor: 'var(--accent-purple)', boxShadow: '0 0 30px rgba(139, 92, 246, 0.2)' }}>
                        <h3 className="feature-title">Pro</h3>
                        <div className="stat-value" style={{ fontSize: '2.5rem', margin: '1rem 0' }}>₹50k<span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>/mo</span></div>
                        <p className="feature-desc">Enhanced analytics for growing brokers.</p>
                        <ul className="check-list" style={{ textAlign: 'left', margin: '2rem 0' }}>
                            <li className="check-item"><span className="check-icon">✓</span> Churn Prediction AI</li>
                            <li className="check-item"><span className="check-icon">✓</span> Dealer Desk Analytics</li>
                            <li className="check-item"><span className="check-icon">✓</span> API Integration</li>
                            <li className="check-item"><span className="check-icon">✓</span> Dedicated Account Manager</li>
                        </ul>
                        <a href={jotformLink} target="_blank" rel="noopener noreferrer" className="btn-primary" style={{ width: '100%', background: 'var(--accent-purple)', display: 'block', textDecoration: 'none', textAlign: 'center' }}>Contact Sales</a>
                    </div>

                    <div className="glass-card">
                        <h3 className="feature-title">Max</h3>
                        <div className="stat-value" style={{ fontSize: '2.5rem', margin: '1rem 0' }}>₹1L+<span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>/mo</span></div>
                        <p className="feature-desc">Full enterprise infrastructure.</p>
                        <ul className="check-list" style={{ textAlign: 'left', margin: '2rem 0' }}>
                            <li className="check-item"><span className="check-icon">✓</span> Private Cloud Deployment</li>
                            <li className="check-item"><span className="check-icon">✓</span> Custom AI Models</li>
                            <li className="check-item"><span className="check-icon">✓</span> HSM/KMS Security</li>
                            <li className="check-item"><span className="check-icon">✓</span> 24/7 SLA Support</li>
                        </ul>
                        <a href={jotformLink} target="_blank" rel="noopener noreferrer" className="btn-primary" style={{ width: '100%', background: 'rgba(255,255,255,0.1)', display: 'block', textDecoration: 'none', textAlign: 'center' }}>Contact Sales</a>
                    </div>
                </div>
            )}

            {/* Enterprise Security Add-on */}
            <div style={{ marginTop: '4rem', padding: '2rem', background: 'rgba(255,255,255,0.02)', borderRadius: '16px', border: '1px solid var(--glass-border)' }}>
                <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>🔒 Enterprise Security Add-On</h3>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
                    Turnkey security solutions to satisfy compliance. Setup: ₹2L one-time | Recurring: ₹50k/month.
                </p>
                <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', flexWrap: 'wrap' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>🛡️ SOC Readiness</span>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>🔐 HSM/KMS Integration</span>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>📜 SIEM Compatibility</span>
                </div>
            </div>
        </div>
    );
}
