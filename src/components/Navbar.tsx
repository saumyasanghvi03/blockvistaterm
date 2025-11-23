import { Link } from 'react-router-dom';

export default function Navbar() {
    return (
        <nav className="navbar animate-fade-up">
            <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <div style={{ width: 32, height: 32, background: 'var(--accent-blue)', borderRadius: 8 }}></div>
                    <span style={{ fontWeight: 700, fontSize: '1.2rem', color: 'white' }}>BlockVista Terminal</span>
                </div>
            </Link>

            <div className="nav-links hidden md:flex">
                <Link to="/" className="nav-link">Home</Link>
                <Link to="/about" className="nav-link">About</Link>
                <Link to="/products" className="nav-link">Products</Link>
                <Link to="/pricing" className="nav-link">Pricing</Link>
                <Link to="/features" className="nav-link">Features</Link>
                <Link to="/contact" className="nav-link">Contact</Link>
            </div>

            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                <a
                    href="https://agent.jotform.com/019aaff0529c75ba987ada46debdca400757"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-primary"
                    style={{ textDecoration: 'none' }}
                >
                    Start Pilot
                </a>
            </div>
        </nav>
    );
}
