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
                        <li><a href="#">Features</a></li>
                        <li><a href="#">Pricing</a></li>
                        <li><a href="#">Security</a></li>
                        <li><a href="#">API Docs</a></li>
                    </ul>
                </div>

                {/* Company */}
                <div className="footer-section">
                    <h4>Company</h4>
                    <ul>
                        <li><a href="#">About</a></li>
                        <li><a href="#">Blog</a></li>
                        <li><a href="#">Careers</a></li>
                        <li><a href="#">Contact</a></li>
                    </ul>
                </div>

                {/* Legal */}
                <div className="footer-section">
                    <h4>Legal</h4>
                    <ul>
                        <li><a href="#">Privacy</a></li>
                        <li><a href="#">Terms</a></li>
                        <li><a href="#">Compliance</a></li>
                        <li><a href="#">Security</a></li>
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
                    © 2024 BlockVista Terminal. All rights reserved.
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
