export default function Security() {
    return (
        <div style={{ paddingTop: '120px', paddingBottom: '80px' }} className="container">
            <h1 className="hero-title" style={{ textAlign: 'center', marginBottom: '2rem' }}>Security First</h1>
            <div className="glass-card" style={{ maxWidth: '800px', margin: '0 auto' }}>
                <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>
                    At BlockVista Terminal, security is not an afterthought—it's our foundation. We employ state-of-the-art encryption and security practices to ensure your data and assets remain safe.
                </p>

                <h3 style={{ color: 'var(--accent-blue)', marginTop: '2rem' }}>Bank-Grade Encryption</h3>
                <p style={{ color: 'var(--text-secondary)' }}>
                    All data in transit and at rest is encrypted using AES-256 standards.
                </p>

                <h3 style={{ color: 'var(--accent-blue)', marginTop: '2rem' }}>Two-Factor Authentication (2FA)</h3>
                <p style={{ color: 'var(--text-secondary)' }}>
                    Mandatory 2FA for all sensitive actions to prevent unauthorized access.
                </p>

                <h3 style={{ color: 'var(--accent-blue)', marginTop: '2rem' }}>Regular Audits</h3>
                <p style={{ color: 'var(--text-secondary)' }}>
                    We conduct frequent security audits and penetration testing with top-tier firms.
                </p>
            </div>
        </div>
    );
}
