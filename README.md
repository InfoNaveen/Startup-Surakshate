
# 🛡️ **Startup Surakshate**

![Startup Surakshate](https://img.shields.io/badge/Startup-Surakshate-black?style=for-the-badge\&logo=shield)

> **Because every startup deserves protection from day one.**

**Startup Surakshate** is an AI-powered cybersecurity platform that scans startup codebases or websites for vulnerabilities, then provides AI-driven summaries, severity ratings, and remediation advice — helping founders secure their projects effortlessly.

---

## 🌍 **Overview**

**Startup Surakshate** empowers startups with **smart, scalable cybersecurity** using AI.
It analyzes GitHub repositories or websites for vulnerabilities and delivers actionable insights — all in a clean, beginner-friendly interface.

### 🔑 **Core Features**

* 🔐 **User Authentication** – Secure login/signup using **Supabase**
* 🧠 **AI-Powered Analysis** – Generates plain-language summaries via **OpenAI**
* 🧰 **Security Scanning**

  * **Repository Scanning:** Detects outdated dependencies, exposed keys, insecure configs
  * **Website Scanning:** Checks for missing headers, phishing, mixed content, outdated JS libs
* 📊 **Vulnerability Dashboard** – Shows risks, severity, and recommended fixes
* 📄 **PDF Report Generation** – Export scan results professionally
* ⚡ **Demo Mode** – Try all features instantly without API setup

---

## 🚀 **Quick Start Guide**

### 📋 **Prerequisites**

* Python 3.8 + (3.9 recommended)
* Node.js + npm (for frontend)
* Supabase account (free tier)
* OpenAI API key
* wkhtmltopdf (for PDF generation)

### 🧩 **Installation**

```bash
# 1️⃣ Clone repo
git clone https://github.com/InfoNaveen/Startup-Surakshate.git
cd Startup-Surakshate

# 2️⃣ Create virtual environment
python -m venv venv
# Activate
venv\Scripts\activate    # Windows
source venv/bin/activate # macOS/Linux

# 3️⃣ Install dependencies
pip install -r requirements.txt
```

### 🧱 **Setup wkhtmltopdf**

* **Windows:** [Download installer](https://wkhtmltopdf.org/downloads.html) → add to PATH
* **macOS:** `brew install wkhtmltopdf`
* **Linux:** `sudo apt-get install wkhtmltopdf`

### ⚙️ **Environment Variables**

```bash
cp .env.example .env
```

Then edit `.env`:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_api_key
APP_NAME=Startup Surakshate
ENVIRONMENT=development
DEBUG=true
DEMO_MODE=true
```

### ▶️ **Run the App**

```bash
uvicorn main:app --reload --port 8000
```

Then open **[http://localhost:8000](http://localhost:8000)**

---

## 💡 **Demo Mode**

Don’t want to set up keys yet?
Set `DEMO_MODE=true` and click **“Run Demo Scan”** to preview the system with sample results.

---

## ⚙️ **Tech Stack**

| Layer         | Technology                         |
| ------------- | ---------------------------------- |
| Backend       | **Python (FastAPI)**               |
| Database/Auth | **Supabase**                       |
| Frontend      | **HTML + Tailwind CSS + JS**       |
| AI Engine     | **OpenAI GPT-4o-mini**             |
| Security Scan | Custom Python analyzers + Snyk API |
| Reports       | **pdfkit / wkhtmltopdf**           |
| Deployment    | **Vercel** / **Render**            |

---

## 🧭 **Usage Flow**

1. Visit landing page → learn about the product
2. Sign up / Login
3. Choose **Scan Type** → (Repository / Website)
4. Click **Start Scan** or **Run Demo Scan**
5. View vulnerabilities, AI-generated insights, and remediation steps
6. Generate 📄 PDF report
7. Review scan history on dashboard

---

## 📁 **Project Structure**

```
/startup-surakshate
├── main.py
├── /api
│   ├── auth.py
│   ├── scan.py
│   └── report.py
├── /utils
│   ├── supabase_client.py
│   ├── scan_repo.py
│   ├── scan_site.py
│   ├── summarize.py
│   ├── pdf_generator.py
│   └── security.py
├── /static
│   ├── /css/style.css
│   ├── /js/dashboard.js
│   └── /img/
├── /templates
│   ├── index.html
│   └── dashboard.html
├── requirements.txt
├── .env.example
├── Dockerfile
├── Procfile
├── vercel.json
└── README.md
```

---

## 🔒 **Security Layers**

✅ **Implemented**

* Repository scanner (outdated deps, exposed keys, insecure configs)
* Website scanner (headers, mixed content, XSS, SQL injection, outdated libs)
* AI prompt sanitization before LLM calls
* Sensitive data masking in reports/logs
* Backend security headers and rate limiting
* Input validation for scan URLs

⚙️ **New Modules**

* `utils/security.py` → URL validation, text scrubbing, token masking
* `main.py` → Adds headers (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`), basic rate limiter
* `api/scan.py` → Verifies safe URLs before processing

⚠️ **Recommendations**

* Enable RLS (Row Level Security) in Supabase
* Use Redis-based rate limiter for production
* Add Content-Security-Policy when frontend is hosted
* Keep `.env` and keys private

---

## ☁️ **Deployment**

### 🚀 Deploy to Vercel

1. Fork this repo
2. Import it in [Vercel](https://vercel.com)
3. Add env variables
4. Deploy → Done!

### 🐳 Deploy to Render

1. Fork repo → [Render](https://render.com)
2. Create **Web Service** with Docker environment
3. Add env variables
4. Deploy automatically via `Dockerfile`

---

## 🧩 **Troubleshooting**

| Issue                | Solution                                       |
| -------------------- | ---------------------------------------------- |
| ❌ PDF not generating | Ensure `wkhtmltopdf` is installed & accessible |
| ⚠️ Invalid API keys  | Re-check `.env` or use Demo Mode               |
| 🐛 Deployment fails  | Verify Dockerfile / vercel.json paths & logs   |
| 🔑 Secrets exposed   | Remove `.env` & confirm `.gitignore` rules     |

---

## 📘 **Notes**

* “**Surakshate**” means “Protection” in Kannada 🇮🇳
* Built for **CODEPOCALYPSE Hackathon 2025**
* Created entirely using AI tools (Trae AI + Cursor + ChatGPT) 💡

---

## 👨‍💻 **Developer**

**Naveen Patil**
💼 CSE @ VTU | Tech Entrepreneur in the Making
🔗 [GitHub → InfoNaveen](https://github.com/InfoNaveen)

---

## 📄 **License**

Licensed under the **MIT License** — see `LICENSE` for details.

---

### 💬 *Secure • Scale • Succeed* 🚀

