import os
import tempfile
from datetime import datetime
from typing import Dict, Any
import jinja2
import pdfkit
from dotenv import load_dotenv
from utils.security import mask_sensitive_in_text

# Load environment variables
load_dotenv()

async def generate_pdf_report(scan_job: Dict[str, Any]) -> str:
    """
    Generate a PDF report for a scan job
    
    Args:
        scan_job: Dictionary containing scan job details
        
    Returns:
        Path to the generated PDF file
    """
    try:
        # Create a temporary file for the PDF
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, f"surakshate_report_{scan_job['id']}.pdf")
        
        # Get scan details
        scan_type = scan_job.get("scan_type", "unknown")
        url = scan_job.get("url", "")
        name = scan_job.get("name", url)
        created_at = scan_job.get("created_at", datetime.now().isoformat())
        completed_at = scan_job.get("completed_at", datetime.now().isoformat())
        
        # Format dates
        try:
            created_date = datetime.fromisoformat(created_at).strftime("%B %d, %Y %H:%M:%S")
        except:
            created_date = created_at
            
        try:
            completed_date = datetime.fromisoformat(completed_at).strftime("%B %d, %Y %H:%M:%S")
        except:
            completed_date = completed_at
        
        # Get results and summary
        results = scan_job.get("results", {})
        summary = scan_job.get("summary", {})
        ai_summary = scan_job.get("summary", {})
        
        # Get vulnerabilities
        vulnerabilities = results.get("vulnerabilities", [])
        
        # Count vulnerabilities by severity
        high_count = sum(1 for v in vulnerabilities if v.get("severity") == "high")
        medium_count = sum(1 for v in vulnerabilities if v.get("severity") == "medium")
        low_count = sum(1 for v in vulnerabilities if v.get("severity") == "low")
        total_count = len(vulnerabilities)
        
        # Create HTML template
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Startup Surakshate Security Report</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .header {
                    background-color: #333;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }
                .logo {
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                .tagline {
                    font-style: italic;
                    margin-bottom: 20px;
                }
                .section {
                    margin-bottom: 30px;
                }
                .section-title {
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 10px;
                    color: #333;
                    border-bottom: 2px solid #ddd;
                    padding-bottom: 5px;
                }
                .info-row {
                    display: flex;
                    margin-bottom: 10px;
                }
                .info-label {
                    font-weight: bold;
                    width: 150px;
                }
                .summary-box {
                    background-color: #f9f9f9;
                    border: 1px solid #ddd;
                    padding: 15px;
                    margin-bottom: 20px;
                }
                .vulnerability {
                    margin-bottom: 20px;
                    padding: 15px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
                .vulnerability-high {
                    border-left: 5px solid #d9534f;
                }
                .vulnerability-medium {
                    border-left: 5px solid #f0ad4e;
                }
                .vulnerability-low {
                    border-left: 5px solid #5bc0de;
                }
                .severity {
                    display: inline-block;
                    padding: 3px 8px;
                    border-radius: 3px;
                    font-size: 12px;
                    font-weight: bold;
                    color: white;
                    margin-bottom: 10px;
                }
                .severity-high {
                    background-color: #d9534f;
                }
                .severity-medium {
                    background-color: #f0ad4e;
                }
                .severity-low {
                    background-color: #5bc0de;
                }
                .footer {
                    text-align: center;
                    margin-top: 50px;
                    font-size: 12px;
                    color: #777;
                }
                .chart {
                    width: 100%;
                    height: 20px;
                    background-color: #eee;
                    margin-bottom: 10px;
                }
                .chart-bar-high {
                    height: 100%;
                    background-color: #d9534f;
                    display: inline-block;
                }
                .chart-bar-medium {
                    height: 100%;
                    background-color: #f0ad4e;
                    display: inline-block;
                }
                .chart-bar-low {
                    height: 100%;
                    background-color: #5bc0de;
                    display: inline-block;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">Startup Surakshate</div>
                    <div class="tagline">Because every Startup deserves protection from day one.</div>
                </div>
                
                <div class="section">
                    <div class="section-title">Security Scan Report</div>
                    <div class="info-row">
                        <div class="info-label">Name:</div>
                        <div>{{ name }}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">URL:</div>
                        <div>{{ url }}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Scan Type:</div>
                        <div>{{ scan_type }}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Scan Started:</div>
                        <div>{{ created_date }}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Scan Completed:</div>
                        <div>{{ completed_date }}</div>
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">Vulnerability Summary</div>
                    <div class="chart">
                        {% if total_count > 0 %}
                        <div class="chart-bar-high" style="width: {{ (high_count / total_count) * 100 }}%;"></div>
                        <div class="chart-bar-medium" style="width: {{ (medium_count / total_count) * 100 }}%;"></div>
                        <div class="chart-bar-low" style="width: {{ (low_count / total_count) * 100 }}%;"></div>
                        {% endif %}
                    </div>
                    <div class="info-row">
                        <div class="info-label">High Severity:</div>
                        <div>{{ high_count }}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Medium Severity:</div>
                        <div>{{ medium_count }}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Low Severity:</div>
                        <div>{{ low_count }}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Total:</div>
                        <div>{{ total_count }}</div>
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">AI Analysis</div>
                    <div class="summary-box">
                        <h3>Overview</h3>
                        <p>{{ ai_summary.overview }}</p>
                        
                        <h3>Key Findings</h3>
                        <p>{{ ai_summary.key_findings }}</p>
                        
                        <h3>Recommendations</h3>
                        <p>{{ ai_summary.recommendations }}</p>
                        
                        <h3>Risk Assessment</h3>
                        <p>{{ ai_summary.risk_assessment }}</p>
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">Detailed Findings</div>
                    {% for vuln in vulnerabilities %}
                    <div class="vulnerability vulnerability-{{ vuln.severity }}">
                        <div class="severity severity-{{ vuln.severity }}">{{ vuln.severity|upper }}</div>
                        <h3>{{ vuln.type|replace('_', ' ')|title }}</h3>
                        {% if vuln.package %}
                        <div class="info-row">
                            <div class="info-label">Package:</div>
                            <div>{{ vuln.package }}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">Version:</div>
                            <div>{{ vuln.version }}</div>
                        </div>
                        {% endif %}
                        {% if vuln.file %}
                        <div class="info-row">
                            <div class="info-label">File:</div>
                            <div>{{ vuln.file }}</div>
                        </div>
                        {% endif %}
                        {% if vuln.header %}
                        <div class="info-row">
                            <div class="info-label">Header:</div>
                            <div>{{ vuln.header }}</div>
                        </div>
                        {% endif %}
                        <div class="info-row">
                            <div class="info-label">Description:</div>
                            <div>{{ vuln.description }}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">Recommendation:</div>
                            <div>{{ vuln.recommendation }}</div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                <div class="footer">
                    <p>Generated by Startup Surakshate - Because every Startup deserves protection from day one.</p>
                    <p>Surakshate means "Protection" in Kannada</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Render the template
        template = jinja2.Template(html_template)
        # mask sensitive data in text fields used in the report
        safe_name = mask_sensitive_in_text(name)
        safe_url = mask_sensitive_in_text(url)
        html_content = template.render(
            name=safe_name,
            url=safe_url,
            scan_type=scan_type.capitalize(),
            created_date=created_date,
            completed_date=completed_date,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count,
            total_count=total_count,
            ai_summary=ai_summary,
            vulnerabilities=vulnerabilities
        )
        
        # Generate PDF
        pdfkit_options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': 'UTF-8',
            'no-outline': None
        }
        
        # Try to generate PDF with pdfkit
        try:
            pdfkit.from_string(html_content, pdf_path, options=pdfkit_options)
        except Exception as e:
            # If pdfkit fails, try to use a different approach or return an error
            # For the hackathon, we'll just save the HTML and return its path
            html_path = os.path.join(temp_dir, f"surakshate_report_{scan_job['id']}.html")
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return html_path
        
        return pdf_path
    
    except Exception as e:
        # If all else fails, create a simple text report
        temp_dir = tempfile.gettempdir()
        txt_path = os.path.join(temp_dir, f"surakshate_report_{scan_job['id']}.txt")
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"Startup Surakshate Security Report\n")
            f.write(f"================================\n\n")
            f.write(f"Scan Name: {scan_job.get('name', 'Unknown')}\n")
            f.write(f"URL: {scan_job.get('url', 'Unknown')}\n")
            f.write(f"Scan Type: {scan_job.get('scan_type', 'Unknown')}\n")
            f.write(f"Created: {scan_job.get('created_at', 'Unknown')}\n")
            f.write(f"Completed: {scan_job.get('completed_at', 'Unknown')}\n\n")
            
            f.write(f"AI Summary:\n")
            f.write(f"-----------\n")
            summary = scan_job.get("summary", {})
            f.write(f"Overview: {summary.get('overview', 'No overview available')}\n\n")
            f.write(f"Key Findings: {summary.get('key_findings', 'No findings available')}\n\n")
            f.write(f"Recommendations: {summary.get('recommendations', 'No recommendations available')}\n\n")
            f.write(f"Risk Assessment: {summary.get('risk_assessment', 'Unknown')}\n\n")
            
            f.write(f"Vulnerabilities:\n")
            f.write(f"---------------\n")
            results = scan_job.get("results", {})
            vulnerabilities = results.get("vulnerabilities", [])
            
            for i, vuln in enumerate(vulnerabilities):
                f.write(f"{i+1}. {vuln.get('type', 'Unknown')} - {vuln.get('severity', 'Unknown').upper()}\n")
                f.write(f"   Description: {vuln.get('description', 'No description')}\n")
                f.write(f"   Recommendation: {vuln.get('recommendation', 'No recommendation')}\n\n")
        
        return txt_path