# Startup Surakshate

![Startup Surakshate](https://img.shields.io/badge/Startup-Surakshate-black?style=for-the-badge&logo=shield)

> Because every Startup deserves protection from day one.

Startup Surakshate is an AI-powered cybersecurity platform that scans startup codebases or websites for vulnerabilities, then generates AI-driven summaries and remediation advice for founders.

## 🛡️ Project Overview

Startup Surakshate empowers startups with smart, scalable cybersecurity using AI. The platform allows users to scan GitHub repositories or websites for security vulnerabilities, providing actionable insights and remediation steps.

### Core Features

- **User Authentication**: Sign up/login via Supabase auth
- **Security Scanning**:
  - GitHub Repository Scanning: Check for outdated dependencies, exposed keys, insecure configs
  - Website Scanning: Check for missing headers, phishing patterns, mixed content, etc.
- **AI-Powered Analysis**: Uses OpenAI to summarize findings in a user-friendly way
- **Vulnerability Dashboard**: Displays issues, severity levels, and remediation steps
- **PDF Report Generation**: Generate comprehensive security reports
- **Demo Mode**: Quickly test functionality with sample data

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (3.9 recommended)
- Node.js and npm (for frontend development)
- Supabase account (free tier works fine)
- OpenAI API key
- wkhtmltopdf (for PDF generation)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/InfoNaveen/Startup-Surakshate-MVP.git
   cd Startup-Surakshate-MVP
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install wkhtmltopdf:
   - **Windows**: Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html) and add to PATH
   - **macOS**: `brew install wkhtmltopdf`
   - **Linux**: `sudo apt-get install wkhtmltopdf`

5. Set up environment variables:
   ```bash
   # Copy the example file
   cp .env.example .env
   ```

6. Edit the `.env` file with your credentials:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   OPENAI_API_KEY=your_openai_api_key
   APP_NAME=Startup Surakshate
   ENVIRONMENT=development
   DEBUG=true
   DEMO_MODE=true  # Set to false in production
   ```

7. Run the application:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

8. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

### Demo Mode

For quick testing without setting up API keys:

1. Ensure `DEMO_MODE=true` in your `.env` file
2. Start the application as normal
3. Use the "Run Demo Scan" button on the dashboard to see sample results

## 🧰 Tech Stack

- **Backend**: Python (FastAPI)
- **Database/Auth**: Supabase
- **Frontend**: HTML/CSS/JS with Tailwind CSS
- **AI Integration**: OpenAI API (GPT-4 or GPT-4o-mini)
- **PDF Generation**: pdfkit
- **Deployment**: Vercel/Render

## 📊 Demo Flow

1. **Landing Page**: Visit the homepage to learn about Startup Surakshate
2. **Sign Up/Login**: Create an account or log in
3. **Dashboard**: Access the main dashboard
4. **Start a Scan**:
   - Enter a GitHub repository URL or website URL
   - Select scan type (repository or website)
   - Click "Start Scan" or try "Run Demo Scan"
5. **View Results**:
   - See vulnerability summary with severity levels
   - Read AI-generated analysis and recommendations
   - Review detailed findings for each vulnerability
6. **Generate Report**: Create a PDF report of the scan results
7. **View Recent Scans**: Access history of previous scans

## 🔧 Development

### Project Structure

```
/startup-surakshate
├── main.py                # FastAPI entry point
├── /api                   # API routes
│   ├── __init__.py
│   ├── auth.py            # Authentication endpoints
│   ├── scan.py            # Scanning endpoints
│   └── report.py          # Report generation endpoints
├── /utils                 # Helper functions
│   ├── __init__.py
│   ├── supabase_client.py # Supabase integration
│   ├── scan_repo.py       # GitHub repository scanner
│   ├── scan_site.py       # Website scanner
│   ├── summarize.py       # OpenAI integration
│   └── pdf_generator.py   # PDF report generation
├── /static                # Static files
│   ├── /css
│   │   └── style.css
│   ├── /js
│   │   ├── main.js        # Landing page JavaScript
│   │   └── dashboard.js   # Dashboard JavaScript
│   └── /img
├── /templates             # HTML templates
│   ├── index.html         # Landing page
│   └── dashboard.html     # Dashboard page
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables example
├── vercel.json            # Vercel configuration
├── Procfile               # Render configuration
└── README.md              # Project documentation
```

### API Endpoints

- **Authentication**:
  - `POST /api/auth/signup`: Create a new user account
  - `POST /api/auth/login`: Log in an existing user
  - `POST /api/auth/logout`: Log out the current user
  - `GET /api/auth/me`: Get the current user's information

- **Scanning**:
  - `POST /api/scan`: Create a new scan job
  - `POST /api/scan/{scan_id}/run`: Run a scan job
  - `GET /api/scan/{scan_id}/status`: Get the status of a scan job
  - `GET /api/scan/{scan_id}`: Get the results of a scan job
  - `GET /api/scan`: Get a list of scan jobs

- **Reporting**:
  - `GET /api/report/{scan_id}`: Generate a PDF report for a scan job

## 🔒 Security Features

### Repository Scanning

- **Outdated Dependencies**: Identifies outdated npm and Python packages
- **Exposed API Keys**: Detects hardcoded API keys and secrets
- **Insecure Configurations**: Finds insecure settings in configuration files

### Website Scanning

- **Security Headers**: Checks for missing security headers (CSP, X-Frame-Options, etc.)
- **Mixed Content**: Identifies HTTP resources loaded on HTTPS pages
- **External Forms**: Detects forms submitting to external domains
- **Outdated Libraries**: Finds outdated JavaScript libraries with known vulnerabilities
- **Common Vulnerabilities**: Checks for XSS, SQL injection, and other common web vulnerabilities

## 🚢 Deployment

### Deploying to Vercel

1. Fork this repository to your GitHub account
2. Sign up for a [Vercel](https://vercel.com) account if you don't have one
3. Create a new project in Vercel and import your GitHub repository
4. Configure the following environment variables in Vercel:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `OPENAI_API_KEY`
   - `APP_NAME`
   - `ENVIRONMENT=production`
   - `DEBUG=false`
   - `DEMO_MODE=false` (or true for demo purposes)
5. Deploy the project
6. Vercel will automatically build and deploy your application using the `vercel.json` configuration

### Deploying to Render

1. Fork this repository to your GitHub account
2. Sign up for a [Render](https://render.com) account if you don't have one
3. Create a new Web Service in Render
4. Connect your GitHub repository
5. Configure the service with these settings:
   - **Name**: startup-surakshate (or your preferred name)
   - **Environment**: Docker
   - **Region**: Choose the closest to your users
6. Add the following environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `OPENAI_API_KEY`
   - `APP_NAME`
   - `ENVIRONMENT=production`
   - `DEBUG=false`
   - `DEMO_MODE=false` (or true for demo purposes)
7. Click "Create Web Service"
8. Render will automatically build and deploy your application using the `Dockerfile`

## 🔧 Troubleshooting

### Common Issues

1. **PDF Generation Fails**:
   - Ensure wkhtmltopdf is properly installed
   - Check file permissions for the output directory
   - If issues persist, the application will fall back to HTML or text output

2. **API Key Issues**:
   - Verify your Supabase and OpenAI API keys are correct
   - Check that your Supabase project has the correct tables and policies
   - Use demo mode for testing without API keys

3. **Deployment Issues**:
   - For Vercel: Ensure `vercel.json` is properly configured
   - For Render: Ensure `Dockerfile` is in the root directory
   - Check deployment logs for specific error messages

## 📝 Notes

- The name "Surakshate" means "Protection" in Kannada
- For hackathon purposes, a demo mode is available to showcase functionality without requiring actual scanning
- The application is designed to be deployed on Vercel or Render

## 👨‍💻 Developer Information

Created for CODEPOCALYPSE Hackathon

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Secure. Scale. Succeed.

## Security Audit & Enhancements

### Status Overview
- ✅ Repo Scanner: outdated deps, exposed secrets, insecure configs (heuristic)
- ✅ Website Scanner: missing headers, mixed content, external forms, outdated libs, common risks
- ✅ AI Summary Layer: prompts sanitized to redact likely secrets before sending to LLM
- ✅ PDF Report: sensitive tokens/long IDs masked in rendered output
- ✅ API & Backend: CORS enabled, security headers (X-Content-Type-Options, X-Frame-Options, Referrer-Policy), simple rate limiting
- ⚠️ Supabase Security: depends on your table RLS policies; ensure RLS is ON and policies restrict access per user
- ⚠️ Rate limiting: basic in-memory, scale with Redis in production

### New Layers Added
- Security middleware in `main.py`:
  - Adds `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`
  - Simple per-IP rate limiting (60 req/min)
- `utils/security.py`:
  - `is_url_safe` to block risky schemes and embedded credentials
  - `sanitize_text_for_llm` to scrub secrets and truncate data before LLM calls
  - `mask_sensitive_in_text` to hide tokens in reports/logs
  - `SimpleRateLimiter` for throttling
- `api/scan.py`: validates URL with `is_url_safe` before creating jobs
- `utils/summarize.py`: sanitizes prompts before OpenAI
- `utils/pdf_generator.py`: masks sensitive data in report fields

### Why This Helps
- Reduces XSS/clickjacking risks and information leakage
- Prevents obvious SSRF/phishing via dangerous URL schemes
- Limits abuse and accidental DoS with throttling
- Avoids leaking secrets to third-party LLMs and in generated PDFs

### Remaining Recommendations
- Enable and enforce Supabase RLS with per-user policies on `profiles` and `scans`
- Replace in-memory rate limiter with Redis-backed limiter
- Add CSP header policy when you control frontend domain (template pages currently use external CDNs)
- Add audit log table (user, action, timestamp, severity) for traceability
- Optional: integrate a free threat intel check (e.g., AbuseIPDB) behind a feature flag