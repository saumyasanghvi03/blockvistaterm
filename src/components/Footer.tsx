import { Link } from 'react-router-dom';

export default function Footer() {
    return (
        <footer className="footer">
            <div className="footer-content">
                {/* Brand */}
                <div className="footer-brand">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                        <div style={{ width: 24, height: 24, background: 'var(--accent-blue)', borderRadius: 6 }}></div>
                        <h3 style={{ margin: 0, fontSize: '1.2rem', color: 'var(--accent-purple)' }}>BlockVista Terminal - AI Financial Analytics</h3>
                    </div>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                        India's institutional-grade multi-asset trading platform
                    </p>
                </div>

                {/* Product */}
                <div className="footer-section">
                    <h4>Product</h4>
                    <ul>
                        <li><Link to="/features">Features</Link></li>
                        <li><Link to="/pricing">Pricing</Link></li>
                        <li><Link to="/security">Security</Link></li>
                        <li><Link to="/api-docs">API Docs</Link></li>
                    </ul>
                </div>

                {/* Company */}
                <div className="footer-section">
                    <h4>Company</h4>
                    <ul>
                        <li><Link to="/about">About</Link></li>
                        <li><Link to="/blog">Blog</Link></li>
                        <li><Link to="/careers">Careers</Link></li>
                        <li><Link to="/contact">Contact</Link></li>
                    </ul>
                </div>

                {/* Legal */}
                <div className="footer-section">
                    <h4>Legal</h4>
                    <ul>
                        <li><Link to="/legal#privacy">Privacy</Link></li>
                        <li><Link to="/legal#terms">Terms</Link></li>
                        <li><Link to="/legal#compliance">Compliance</Link></li>
                        <li><Link to="/legal#security">Security</Link></li>
                    </ul>
                </div>
            </div>

            {/* Bottom Bar */}
            <div style={{
                borderTop: '1px solid var(--glass-border)',
                marginTop: '3rem',
                paddingTop: '1.5rem',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: '1rem',
                color: 'var(--text-secondary)',
                fontSize: '0.9rem'
            }}>
                <div>
                    © 2025-2027 BlockVista Terminal. All rights reserved.
                </div>
                <div style={{ display: 'flex', gap: '1.5rem' }}>
                    <a href="#" style={{ color: 'inherit', textDecoration: 'none' }}>Twitter</a>
                    <a href="#" style={{ color: 'inherit', textDecoration: 'none' }}>LinkedIn</a>
                    <a href="#" style={{ color: 'inherit', textDecoration: 'none' }}>GitHub</a>
                </div>
            </div>
        </footer>
    );
}
