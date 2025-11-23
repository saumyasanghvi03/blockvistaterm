import FeaturesComponent from '../components/Features';
import CTA from '../components/CTA';

export default function Features() {
    return (
        <div style={{ paddingTop: '80px' }}>
            <div className="container">
                <h1 className="hero-title" style={{ textAlign: 'center', marginBottom: '1rem' }}>Platform Features</h1>
                <p style={{ textAlign: 'center', color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto 4rem' }}>
                    Discover the tools that power institutional-grade trading.
                </p>
                <FeaturesComponent />
            </div>
            <CTA />
        </div>
    );
}
