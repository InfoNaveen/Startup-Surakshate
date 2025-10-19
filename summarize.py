import os
import json
from typing import Dict, Any
import openai
from dotenv import load_dotenv
from utils.security import sanitize_text_for_llm

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_ai_summary(scan_results: Dict[str, Any], scan_type: str) -> Dict[str, Any]:
    """
    Generate an AI summary of scan results using OpenAI
    
    Args:
        scan_results: Dictionary containing scan results
        scan_type: Type of scan (repository or website)
        
    Returns:
        Dictionary containing AI-generated summary and recommendations
    """
    try:
        # Check if we're in demo mode
        if os.getenv("DEMO_MODE", "false").lower() == "true":
            return get_demo_summary(scan_results, scan_type)
        
        # Prepare the prompt for OpenAI (sanitized)
        if scan_type == "repository":
            prompt = sanitize_text_for_llm(create_repo_scan_prompt(scan_results))
        else:
            prompt = sanitize_text_for_llm(create_website_scan_prompt(scan_results))
        
        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert analyzing scan results for a startup. Provide a clear, concise summary of the vulnerabilities found, their potential impact, and actionable recommendations to fix them. Use simple language that non-technical founders can understand."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.5
        )
        
        # Extract the summary from the response
        summary_text = response.choices[0].message.content
        
        # Structure the summary
        summary = {
            "overview": extract_section(summary_text, "Overview"),
            "key_findings": extract_section(summary_text, "Key Findings"),
            "recommendations": extract_section(summary_text, "Recommendations"),
            "risk_assessment": extract_section(summary_text, "Risk Assessment"),
            "full_summary": summary_text
        }
        
        return summary
    
    except Exception as e:
        # Return error summary
        return {
            "overview": f"Error generating summary: {str(e)}",
            "key_findings": "Unable to analyze vulnerabilities due to an error.",
            "recommendations": "Please try again or contact support.",
            "risk_assessment": "Unknown",
            "full_summary": f"An error occurred while generating the summary: {str(e)}"
        }

def create_repo_scan_prompt(scan_results: Dict[str, Any]) -> str:
    """Create a prompt for repository scan results"""
    vulnerabilities = scan_results.get("vulnerabilities", [])
    summary = scan_results.get("summary", {})
    
    prompt = f"""
    I need you to analyze the security scan results of a GitHub repository.
    
    Summary:
    - Total vulnerabilities: {summary.get('total', 0)}
    - High severity: {summary.get('high_severity', 0)}
    - Medium severity: {summary.get('medium_severity', 0)}
    - Low severity: {summary.get('low_severity', 0)}
    
    Detailed findings:
    """
    
    # Add details for each vulnerability
    for i, vuln in enumerate(vulnerabilities):
        prompt += f"""
        {i+1}. {vuln.get('type', 'Unknown')}
           - Severity: {vuln.get('severity', 'Unknown')}
           - Description: {vuln.get('description', 'No description')}
           - Recommendation: {vuln.get('recommendation', 'No recommendation')}
        """
    
    prompt += """
    Please provide:
    1. A brief overview of the security posture
    2. Key findings in simple terms that a non-technical founder would understand
    3. Prioritized recommendations for fixing the issues
    4. A risk assessment (Critical, High, Medium, Low)
    
    Format your response with these section headers: "Overview", "Key Findings", "Recommendations", and "Risk Assessment".
    """
    
    return prompt

def create_website_scan_prompt(scan_results: Dict[str, Any]) -> str:
    """Create a prompt for website scan results"""
    vulnerabilities = scan_results.get("vulnerabilities", [])
    summary = scan_results.get("summary", {})
    
    prompt = f"""
    I need you to analyze the security scan results of a website.
    
    Summary:
    - Total vulnerabilities: {summary.get('total', 0)}
    - High severity: {summary.get('high_severity', 0)}
    - Medium severity: {summary.get('medium_severity', 0)}
    - Low severity: {summary.get('low_severity', 0)}
    
    Detailed findings:
    """
    
    # Add details for each vulnerability
    for i, vuln in enumerate(vulnerabilities):
        prompt += f"""
        {i+1}. {vuln.get('type', 'Unknown')}
           - Severity: {vuln.get('severity', 'Unknown')}
           - Description: {vuln.get('description', 'No description')}
           - Recommendation: {vuln.get('recommendation', 'No recommendation')}
        """
    
    prompt += """
    Please provide:
    1. A brief overview of the website's security posture
    2. Key findings in simple terms that a non-technical founder would understand
    3. Prioritized recommendations for fixing the issues
    4. A risk assessment (Critical, High, Medium, Low)
    
    Format your response with these section headers: "Overview", "Key Findings", "Recommendations", and "Risk Assessment".
    """
    
    return prompt

def extract_section(text: str, section_name: str) -> str:
    """Extract a section from the summary text"""
    try:
        # Try to find the section
        start = text.find(f"{section_name}:")
        if start == -1:
            start = text.find(f"{section_name}\n")
        if start == -1:
            start = text.find(f"## {section_name}")
        if start == -1:
            start = text.find(f"**{section_name}**")
            
        if start == -1:
            return f"No {section_name.lower()} provided"
            
        # Find the end of the section (next section or end of text)
        end = len(text)
        next_sections = ["Overview:", "Key Findings:", "Recommendations:", "Risk Assessment:", 
                        "## Overview", "## Key Findings", "## Recommendations", "## Risk Assessment",
                        "**Overview**", "**Key Findings**", "**Recommendations**", "**Risk Assessment**"]
        
        for section in next_sections:
            if section.lower() != f"{section_name.lower()}:":
                next_start = text.find(section, start + len(section_name))
                if next_start != -1 and next_start < end:
                    end = next_start
        
        # Extract and clean the section text
        section_text = text[start:end].strip()
        section_text = section_text.replace(f"{section_name}:", "").strip()
        section_text = section_text.replace(f"{section_name}", "").strip()
        section_text = section_text.replace(f"## {section_name}", "").strip()
        section_text = section_text.replace(f"**{section_name}**", "").strip()
        
        return section_text
    except:
        return f"Error extracting {section_name.lower()}"

def get_demo_summary(scan_results: Dict[str, Any], scan_type: str) -> Dict[str, Any]:
    """Get demo summary for scan results"""
    if scan_type == "repository":
        return {
            "overview": "The repository has several security vulnerabilities that need attention. The most critical issues are related to outdated dependencies and exposed API keys in the codebase.",
            "key_findings": "1. Two high-severity vulnerabilities including an exposed API key in config.js and an outdated axios package with known security issues.\n2. Two medium-severity issues related to outdated lodash dependency and insecure webpack configuration.\n3. One low-severity issue with an outdated React version.",
            "recommendations": "1. Immediately remove the API key from config.js and use environment variables instead.\n2. Update axios to version 0.21.1 or later to fix the server-side request forgery vulnerability.\n3. Update lodash to version 4.17.21 to address the prototype pollution vulnerability.\n4. Fix the insecure webpack configuration to prevent potential attacks.\n5. Consider updating React to the latest version when convenient.",
            "risk_assessment": "High - The exposed API key presents an immediate security risk that could lead to unauthorized access. This should be addressed immediately.",
            "full_summary": "# Security Scan Summary\n\n## Overview\nThe repository has several security vulnerabilities that need attention. The most critical issues are related to outdated dependencies and exposed API keys in the codebase.\n\n## Key Findings\n1. Two high-severity vulnerabilities including an exposed API key in config.js and an outdated axios package with known security issues.\n2. Two medium-severity issues related to outdated lodash dependency and insecure webpack configuration.\n3. One low-severity issue with an outdated React version.\n\n## Recommendations\n1. Immediately remove the API key from config.js and use environment variables instead.\n2. Update axios to version 0.21.1 or later to fix the server-side request forgery vulnerability.\n3. Update lodash to version 4.17.21 to address the prototype pollution vulnerability.\n4. Fix the insecure webpack configuration to prevent potential attacks.\n5. Consider updating React to the latest version when convenient.\n\n## Risk Assessment\nHigh - The exposed API key presents an immediate security risk that could lead to unauthorized access. This should be addressed immediately."
        }
    else:
        return {
            "overview": "The website has several security vulnerabilities that need attention. The most critical issue is the missing Content Security Policy (CSP) header, which could leave the site vulnerable to cross-site scripting (XSS) attacks.",
            "key_findings": "1. One high-severity vulnerability: missing Content Security Policy header.\n2. Four medium-severity issues including missing XSS protection header, mixed content, outdated jQuery library, and insecure cookie settings.",
            "recommendations": "1. Implement a Content Security Policy header to prevent XSS attacks.\n2. Add the X-XSS-Protection header to enable the browser's built-in XSS filter.\n3. Update all HTTP resources to HTTPS to eliminate mixed content warnings.\n4. Update jQuery from version 1.12.4 to 3.6.0 or later.\n5. Set HttpOnly and Secure flags on all cookies containing sensitive information.",
            "risk_assessment": "Medium - While there are no critical vulnerabilities that allow immediate compromise, the missing security headers and outdated libraries create unnecessary risk that should be addressed soon.",
            "full_summary": "# Security Scan Summary\n\n## Overview\nThe website has several security vulnerabilities that need attention. The most critical issue is the missing Content Security Policy (CSP) header, which could leave the site vulnerable to cross-site scripting (XSS) attacks.\n\n## Key Findings\n1. One high-severity vulnerability: missing Content Security Policy header.\n2. Four medium-severity issues including missing XSS protection header, mixed content, outdated jQuery library, and insecure cookie settings.\n\n## Recommendations\n1. Implement a Content Security Policy header to prevent XSS attacks.\n2. Add the X-XSS-Protection header to enable the browser's built-in XSS filter.\n3. Update all HTTP resources to HTTPS to eliminate mixed content warnings.\n4. Update jQuery from version 1.12.4 to 3.6.0 or later.\n5. Set HttpOnly and Secure flags on all cookies containing sensitive information.\n\n## Risk Assessment\nMedium - While there are no critical vulnerabilities that allow immediate compromise, the missing security headers and outdated libraries create unnecessary risk that should be addressed soon."
        }