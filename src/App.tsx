import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Analytics } from '@vercel/analytics/react';
import './index.css';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import About from './pages/About';
import Products from './pages/Products';
import Pricing from './pages/Pricing';
import Contact from './pages/Contact';
import Features from './pages/Features';
import Security from './pages/Security';
import ApiDocs from './pages/ApiDocs';
import Blog from './pages/Blog';
import Careers from './pages/Careers';
import Legal from './pages/Legal';

function App() {
    return (
        <Router>
            <div className="background-glow">
                <div className="orb orb-1"></div>
                <div className="orb orb-2"></div>
            </div>

            <div style={{ position: 'relative', zIndex: 1, minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
                <Navbar />

                <main style={{ flex: 1 }}>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/about" element={<About />} />
                        <Route path="/products" element={<Products />} />
                        <Route path="/pricing" element={<Pricing />} />
                        <Route path="/contact" element={<Contact />} />
                        <Route path="/features" element={<Features />} />
                        <Route path="/security" element={<Security />} />
                        <Route path="/api-docs" element={<ApiDocs />} />
                        <Route path="/blog" element={<Blog />} />
                        <Route path="/careers" element={<Careers />} />
                        <Route path="/legal" element={<Legal />} />
                    </Routes>
                </main>

                <Footer />
            </div>
            <Analytics />
        </Router>
    );
}

export default App;
