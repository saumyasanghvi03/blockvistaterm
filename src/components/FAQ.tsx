import { useState } from 'react';

const faqs = [
    {
        question: "Does BlockVista support multiple brokers?",
        answer: "Yes, BlockVista integrates seamlessly with over 50+ major Indian brokers and institutional execution platforms, allowing you to manage your entire portfolio from a single terminal."
    },
    {
        question: "What is the latency SLA?",
        answer: "We guarantee an internal processing latency of under 50 microseconds. Our direct market access (DMA) pipes ensure you get the fastest possible execution speeds available in the Indian market."
    },
    {
        question: "Is BlockVista SEBI compliant?",
        answer: "Absolutely. BlockVista is built with strict adherence to SEBI regulations and compliance standards required for institutional trading desks and investment advisors."
    },
    {
        question: "Can I use BlockVista for algo trading?",
        answer: "Yes. Our comprehensive API Suite allows you to connect your proprietary algorithms, support high-frequency trading (HFT) strategies, and backtest with historical data."
    },
    {
        question: "What security measures are in place?",
        answer: "We employ enterprise-grade security including 256-bit encryption, mandatory 2FA, IP whitelisting, and regular third-party security audits to ensure your data and assets are protected."
    },
    {
        question: "How do I start?",
        answer: "Simply click the 'Start Pilot' button to begin your 30-day free trial. For institutional requirements, contact our sales team for a personalized demo and onboarding."
    }
];

export default function FAQ() {
    const [openIndex, setOpenIndex] = useState<number | null>(null);

    return (
        <section style={{ padding: '6rem 2rem', maxWidth: '1000px', margin: '0 auto' }}>
            <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
                <h2 className="hero-title" style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>Frequently Asked Questions</h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: '1.2rem' }}>Find answers to common questions</p>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {faqs.map((faq, index) => (
                    <div
                        key={index}
                        className="glass-card"
                        style={{
                            padding: '0',
                            overflow: 'hidden',
                            cursor: 'pointer',
                            transition: 'all 0.3s ease'
                        }}
                        onClick={() => setOpenIndex(openIndex === index ? null : index)}
                    >
                        <div style={{
                            padding: '1.5rem',
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            background: openIndex === index ? 'rgba(255,255,255,0.05)' : 'transparent'
                        }}>
                            <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 500 }}>{faq.question}</h3>
                            <span style={{
                                transform: openIndex === index ? 'rotate(180deg)' : 'rotate(0deg)',
                                transition: 'transform 0.3s ease',
                                fontSize: '1.5rem',
                                color: 'var(--accent-blue)'
                            }}>
                                ▼
                            </span>
                        </div>

                        <div style={{
                            maxHeight: openIndex === index ? '200px' : '0',
                            overflow: 'hidden',
                            transition: 'max-height 0.3s ease',
                            opacity: openIndex === index ? 1 : 0
                        }}>
                            <p style={{
                                padding: '0 1.5rem 1.5rem 1.5rem',
                                color: 'var(--text-secondary)',
                                lineHeight: 1.6,
                                margin: 0
                            }}>
                                {faq.answer}
                            </p>
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
}
