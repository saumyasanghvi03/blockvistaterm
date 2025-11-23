export default function Blog() {
    const posts = [
        {
            title: "The Reality of Retail Trading: 91% F&O Traders in Loss",
            date: "Feb 15, 2025",
            excerpt: "SEBI data reveals a widening gap in retail losses despite new regulatory measures. Net losses for individual traders widened by 41% in FY25.",
            tag: "Regulation"
        },
        {
            title: "Market Correction 2025: FII Exits & Global Headwinds",
            date: "Mar 02, 2025",
            excerpt: "Indian markets face significant selling pressure as Foreign Institutional Investors offload ₹1.33 lakh crore amid weak corporate earnings.",
            tag: "Market Analysis"
        },
        {
            title: "Navigating the Tariff War: Impact on Indian Exporters",
            date: "Jan 28, 2025",
            excerpt: "With new US tariffs impacting up to 70% of exports, Indian sectors like textiles and gems face a $35 billion challenge.",
            tag: "Global Economy"
        }
    ];

    return (
        <div style={{ paddingTop: '120px', paddingBottom: '80px' }} className="container">
            <h1 className="hero-title" style={{ textAlign: 'center', marginBottom: '3rem' }}>Latest Insights</h1>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
                {posts.map((post, index) => (
                    <div key={index} className="glass-card" style={{ cursor: 'pointer', transition: 'transform 0.2s' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                            <span style={{ fontSize: '0.8rem', color: 'var(--accent-blue)', background: 'rgba(59, 130, 246, 0.1)', padding: '0.2rem 0.6rem', borderRadius: '4px' }}>{post.tag}</span>
                            <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{post.date}</span>
                        </div>
                        <h3 style={{ marginBottom: '1rem', color: 'white' }}>{post.title}</h3>
                        <p style={{ color: 'var(--text-secondary)' }}>{post.excerpt}</p>
                        <div style={{ marginTop: '1.5rem', color: 'var(--accent-purple)', fontWeight: 'bold' }}>Read More →</div>
                    </div>
                ))}
            </div>
        </div>
    );
}
