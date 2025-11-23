import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

export default function Legal() {
    const [activeTab, setActiveTab] = useState('privacy');
    const location = useLocation();

    useEffect(() => {
        const hash = location.hash.replace('#', '');
        if (hash && ['privacy', 'terms', 'compliance', 'security'].includes(hash)) {
            setActiveTab(hash);
        }
    }, [location]);

    const tabs = [
        { id: 'privacy', label: 'Privacy Policy' },
        { id: 'terms', label: 'Terms of Service' },
        { id: 'compliance', label: 'Compliance' },
        { id: 'security', label: 'Security' }
    ];

    return (
        <div style={{ paddingTop: '120px', paddingBottom: '80px' }} className="container">
            <h1 className="hero-title" style={{ textAlign: 'center', marginBottom: '3rem' }}>Legal & Compliance</h1>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                {/* Navigation */}
                <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap', marginBottom: '2rem' }}>
                    {tabs.map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => {
                                setActiveTab(tab.id);
                                window.location.hash = tab.id;
                            }}
                            style={{
                                background: activeTab === tab.id ? 'var(--accent-blue)' : 'rgba(255,255,255,0.05)',
                                border: 'none',
                                padding: '0.8rem 1.5rem',
                                borderRadius: '8px',
                                color: 'white',
                                cursor: 'pointer',
                                transition: 'all 0.2s',
                                fontWeight: activeTab === tab.id ? 'bold' : 'normal'
                            }}
                        >
                            {tab.label}
                        </button>
                    ))}
                </div>

                {/* Content Area */}
                <div className="glass-card" style={{ minHeight: '400px' }}>
                    {activeTab === 'privacy' && (
                        <div className="animate-fade-up">
                            <h2>Privacy Policy</h2>
                            <p style={{ color: 'var(--text-secondary)', marginTop: '1rem' }}>
                                Last updated: November 2024
                            </p>
                            <p style={{ marginTop: '1.5rem', lineHeight: 1.6 }}>
                                At BlockVista Terminal, we take your privacy seriously. This policy describes how we collect, use, and protect your personal information.
                            </p>
                            <h3 style={{ marginTop: '2rem' }}>Data Collection</h3>
                            <p style={{ color: 'var(--text-secondary)' }}>We collect information necessary to provide our trading services, including usage data, device information, and trading history to improve your experience.</p>
                        </div>
                    )}

                    {activeTab === 'terms' && (
                        <div className="animate-fade-up">
                            <h2>Terms of Service</h2>
                            <p style={{ color: 'var(--text-secondary)', marginTop: '1rem' }}>
                                Please read these terms carefully before using our platform.
                            </p>
                            <h3 style={{ marginTop: '2rem' }}>Acceptance of Terms</h3>
                            <p style={{ marginTop: '1rem', lineHeight: 1.6 }}>
                                By accessing or using BlockVista Terminal, you agree to be bound by these Terms of Service and all applicable laws and regulations.
                            </p>
                        </div>
                    )}

                    {activeTab === 'compliance' && (
                        <div className="animate-fade-up">
                            <h2>Compliance</h2>
                            <p style={{ marginTop: '1.5rem', lineHeight: 1.6 }}>
                                BlockVista Terminal adheres to all relevant financial regulations in India. We are committed to maintaining a transparent and compliant trading environment.
                            </p>
                            <h3 style={{ marginTop: '2rem' }}>Regulatory Adherence</h3>
                            <p style={{ color: 'var(--text-secondary)' }}>We follow guidelines set by SEBI and other regulatory bodies to ensure fair trading practices and user protection.</p>
                        </div>
                    )}

                    {activeTab === 'security' && (
                        <div className="animate-fade-up">
                            <h2>Security Standards</h2>
                            <p style={{ marginTop: '1.5rem', lineHeight: 1.6 }}>
                                Our platform is built with a security-first approach.
                            </p>
                            <ul style={{ marginTop: '1rem', paddingLeft: '1.5rem', lineHeight: 2, color: 'var(--text-secondary)' }}>
                                <li>End-to-end encryption for all data</li>
                                <li>Regular third-party security audits</li>
                                <li>Multi-factor authentication support</li>
                                <li>Cold storage for digital assets</li>
                            </ul>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
