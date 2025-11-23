export default function Contact() {
    return (
        <div style={{ paddingTop: '120px', paddingBottom: '4rem', maxWidth: '1200px', margin: '0 auto', paddingLeft: '2rem', paddingRight: '2rem' }}>
            <h1 className="hero-title" style={{ textAlign: 'center' }}>Contact Us</h1>
            <p style={{ textAlign: 'center', color: 'var(--text-secondary)', marginBottom: '4rem' }}>
                Have questions? We'd love to hear from you.
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '3rem' }}>
                {/* Contact Info */}
                <div className="glass-card" style={{ height: 'fit-content' }}>
                    <h3 className="feature-title" style={{ marginBottom: '2rem' }}>Get in Touch</h3>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
                            <div style={{ fontSize: '1.5rem' }}>📧</div>
                            <div>
                                <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '0.3rem' }}>Email</div>
                                <a href="mailto:idcfintechsolutions@zohomail.in" style={{ color: 'white', textDecoration: 'none', fontSize: '1.1rem' }}>
                                    idcfintechsolutions@zohomail.in
                                </a>
                            </div>
                        </div>

                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
                            <div style={{ fontSize: '1.5rem' }}>📞</div>
                            <div>
                                <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '0.3rem' }}>Phone</div>
                                <a href="tel:+919324469590" style={{ color: 'white', textDecoration: 'none', fontSize: '1.1rem' }}>
                                    +91 93244 69590
                                </a>
                            </div>
                        </div>

                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
                            <div style={{ fontSize: '1.5rem' }}>💬</div>
                            <div>
                                <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '0.3rem' }}>WhatsApp</div>
                                <a
                                    href="https://wa.me/+919324469590"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    style={{ color: '#25D366', textDecoration: 'none', fontSize: '1.1rem', fontWeight: 500 }}
                                >
                                    Chat on WhatsApp →
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                {/* AI Agent CTA */}
                <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', textAlign: 'center', minHeight: '300px' }}>
                    <div style={{ fontSize: '3rem', marginBottom: '1.5rem' }}>🤖</div>
                    <h3 className="feature-title" style={{ marginBottom: '1rem' }}>Chat with our AI Agent</h3>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem', maxWidth: '300px' }}>
                        Get instant answers to your questions, schedule a demo, or start your pilot program immediately.
                    </p>
                    <a
                        href="https://agent.jotform.com/019aaff0529c75ba987ada46debdca400757"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn-primary"
                        style={{ padding: '1rem 2rem', textDecoration: 'none', fontSize: '1.1rem' }}
                    >
                        Start Chatting Now
                    </a>
                </div>
            </div>
        </div>
    );
}
