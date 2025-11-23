export default function CTA() {
    return (
        <section style={{
            textAlign: 'center',
            padding: '8rem 2rem',
            background: 'linear-gradient(to bottom, transparent, rgba(59, 130, 246, 0.05))',
            position: 'relative',
            overflow: 'hidden'
        }}>
            {/* Background Glow */}
            <div style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                width: '600px',
                height: '600px',
                background: 'radial-gradient(circle, rgba(139, 92, 246, 0.1) 0%, transparent 70%)',
                zIndex: -1,
                pointerEvents: 'none'
            }}></div>

            <h2 style={{
                fontSize: 'clamp(2.5rem, 5vw, 3.5rem)',
                fontWeight: 700,
                marginBottom: '1.5rem',
                color: 'white'
            }}>
                Ready to Transform Your Trading?
            </h2>

            <p style={{
                color: 'var(--text-secondary)',
                fontSize: '1.2rem',
                marginBottom: '3rem',
                maxWidth: '600px',
                marginLeft: 'auto',
                marginRight: 'auto'
            }}>
                Join 50+ brokers and institutional traders using BlockVista Terminal
            </p>

            <div style={{ display: 'flex', gap: '1.5rem', justifyContent: 'center', flexWrap: 'wrap' }}>
                <button className="btn-primary" style={{ padding: '1rem 2.5rem', fontSize: '1.1rem' }}>
                    Start 30-Day Pilot
                </button>
                <button style={{
                    background: 'rgba(255,255,255,0.05)',
                    border: '1px solid var(--glass-border)',
                    color: 'white',
                    padding: '1rem 2.5rem',
                    borderRadius: '8px',
                    fontSize: '1.1rem',
                    cursor: 'pointer',
                    transition: 'all 0.3s'
                }}
                    onMouseOver={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.1)'}
                    onMouseOut={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.05)'}
                >
                    Get Early Access
                </button>
            </div>
        </section>
    );
}
