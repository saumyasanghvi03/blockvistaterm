export default function ApiDocs() {
    return (
        <div style={{ paddingTop: '120px', paddingBottom: '80px' }} className="container">
            <h1 className="hero-title" style={{ textAlign: 'center', marginBottom: '2rem' }}>API Documentation</h1>
            <div className="glass-card" style={{ maxWidth: '800px', margin: '0 auto', textAlign: 'center' }}>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
                    Build your own trading algorithms and integrations with the BlockVista API.
                </p>
                <div style={{ padding: '2rem', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', fontFamily: 'monospace', textAlign: 'left' }}>
                    <div style={{ color: '#a5d6ff' }}>// Example Request</div>
                    <div style={{ color: '#ff7b72' }}>GET</div> <span style={{ color: '#fff' }}>/api/v1/market/quote?symbol=RELIANCE</span>
                    <br /><br />
                    <div style={{ color: '#a5d6ff' }}>// Response</div>
                    <div style={{ color: '#fff' }}>
                        {`{`}
                        <br />&nbsp;&nbsp;"symbol": "RELIANCE",
                        <br />&nbsp;&nbsp;"price": 2450.55,
                        <br />&nbsp;&nbsp;"change": "+1.2%"
                        <br />{`}`}
                    </div>
                </div>
                <button className="btn-primary" style={{ marginTop: '2rem' }}>View Full Documentation</button>
            </div>
        </div>
    );
}
