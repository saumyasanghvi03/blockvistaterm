# Security Policy

## Overview

BlockVista-Terminal is a financial market application that integrates with various APIs to provide blockchain and cryptocurrency market data. Security is a top priority for this project, and we take all security vulnerabilities seriously. This document outlines our security practices and how to report vulnerabilities.

## Supported Versions

We provide security updates for the following versions of BlockVista-Terminal:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

We recommend always using the latest stable release to ensure you have the most recent security patches.

## Reporting Security Vulnerabilities

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in BlockVista-Terminal, please report it responsibly by following these steps:

1. **Email**: Send details to the repository owner at saumyasanghvi03@github.com
2. **Include**:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact assessment
   - Suggested fix (if available)

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Updates**: We will provide regular updates on our progress at least every 7 days
- **Timeline**: We aim to resolve critical vulnerabilities within 30 days
- **Disclosure**: Once the vulnerability is patched, we will coordinate with you on public disclosure
- **Credit**: Security researchers who responsibly disclose vulnerabilities will be credited (unless they prefer to remain anonymous)

### Vulnerability Assessment

- **Accepted**: If the vulnerability is accepted, we will develop a fix and release a security patch
- **Declined**: If the report is declined, we will provide a detailed explanation of our decision

## Best Practices

When using BlockVista-Terminal, please follow these security best practices:

### API Keys and Credentials
- **Never commit API keys** or credentials to version control
- Store sensitive credentials in environment variables or secure credential managers
- Rotate API keys regularly
- Use read-only API keys when write access is not required

### Data Protection
- Keep all dependencies up to date
- Review third-party packages for known vulnerabilities
- Use HTTPS for all API communications
- Validate and sanitize all user inputs

### Application Security
- Run the application with minimal required permissions
- Implement rate limiting for API requests to prevent abuse
- Log security-relevant events for auditing
- Regularly backup important data

### Network Security
- Use secure network connections
- Avoid running the application on untrusted networks
- Consider using VPN when accessing financial APIs

## Security Features

BlockVista-Terminal implements the following security measures:

- Secure API communication over HTTPS
- Input validation and sanitization
- Error handling that doesn't expose sensitive information
- Regular dependency updates

## Contact Information

For security-related inquiries:

- **Repository Owner**: [@saumyasanghvi03](https://github.com/saumyasanghvi03)
- **Security Issues**: Use GitHub Security Advisories (preferred) or email the repository owner
- **General Issues**: [GitHub Issues](https://github.com/saumyasanghvi03/BlockVista-Terminal/issues) (for non-security bugs)

## Security Updates

Security updates will be released as:
- Patch versions for backward-compatible security fixes
- Announced in release notes with severity indicators
- Documented in the project's changelog

## Acknowledgments

We thank all security researchers and users who help keep BlockVista-Terminal secure by responsibly disclosing vulnerabilities.

---

**Last Updated**: November 2025
