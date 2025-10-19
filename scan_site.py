import httpx
import os
from typing import Dict, List, Any
import re
from urllib.parse import urlparse

async def scan_website(url: str) -> Dict[str, Any]:
    """
    Scan a website for security vulnerabilities
    
    Args:
        url: URL of the website
        
    Returns:
        Dict containing scan results
    """
    # Validate URL
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    parsed_url = urlparse(url)
    if not parsed_url.netloc:
        return {
            "status": "error",
            "message": "Invalid website URL",
            "vulnerabilities": []
        }
    
    # Initialize results
    results = {
        "status": "success",
        "site_url": url,
        "vulnerabilities": [],
        "summary": {
            "high_severity": 0,
            "medium_severity": 0,
            "low_severity": 0,
            "total": 0
        }
    }
    
    try:
        # Check if we're in demo mode
        if os.getenv("DEMO_MODE", "false").lower() == "true":
            return get_demo_site_results(url)
        
        async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
            # Fetch the website
            response = await client.get(url)
            status = response.status_code
            headers = response.headers
            content = response.text
            
            # Check for security headers
            await check_security_headers(headers, results)
            
            # Check for mixed content
            await check_mixed_content(content, url, results)
            
            # Check for external forms
            await check_external_forms(content, url, results)
            
            # Check for outdated libraries
            await check_outdated_libraries(content, results)
            
            # Check for common vulnerabilities
            await check_common_vulnerabilities(content, url, results)
        
        # Update summary counts
        for vuln in results["vulnerabilities"]:
            results["summary"]["total"] += 1
            if vuln["severity"] == "high":
                results["summary"]["high_severity"] += 1
            elif vuln["severity"] == "medium":
                results["summary"]["medium_severity"] += 1
            elif vuln["severity"] == "low":
                results["summary"]["low_severity"] += 1
        
        return results
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error scanning website: {str(e)}",
            "vulnerabilities": []
        }

async def check_security_headers(headers: Dict, results: Dict) -> None:
    """Check for missing security headers"""
    # Important security headers to check
    security_headers = {
        "Content-Security-Policy": {
            "severity": "high",
            "description": "Content Security Policy (CSP) header is missing",
            "recommendation": "Implement a Content Security Policy to prevent XSS attacks"
        },
        "X-XSS-Protection": {
            "severity": "medium",
            "description": "X-XSS-Protection header is missing",
            "recommendation": "Add X-XSS-Protection header to enable browser's XSS filter"
        },
        "X-Content-Type-Options": {
            "severity": "medium",
            "description": "X-Content-Type-Options header is missing",
            "recommendation": "Add X-Content-Type-Options: nosniff to prevent MIME type sniffing"
        },
        "X-Frame-Options": {
            "severity": "medium",
            "description": "X-Frame-Options header is missing",
            "recommendation": "Add X-Frame-Options header to prevent clickjacking attacks"
        },
        "Strict-Transport-Security": {
            "severity": "high",
            "description": "HTTP Strict Transport Security (HSTS) header is missing",
            "recommendation": "Implement HSTS to enforce secure connections"
        },
        "Referrer-Policy": {
            "severity": "low",
            "description": "Referrer-Policy header is missing",
            "recommendation": "Add Referrer-Policy header to control how much referrer information is included with requests"
        }
    }
    
    # Check for missing headers
    for header, info in security_headers.items():
        if header not in headers:
            results["vulnerabilities"].append({
                "type": "missing_header",
                "header": header,
                "severity": info["severity"],
                "description": info["description"],
                "recommendation": info["recommendation"]
            })

async def check_mixed_content(content: str, url: str, results: Dict) -> None:
    """Check for mixed content (HTTP resources on HTTPS page)"""
    if url.startswith("https://"):
        # Look for HTTP resources
        http_resources = re.findall(r'src=["\']http://[^"\']+["\']', content)
        http_resources.extend(re.findall(r'href=["\']http://[^"\']+["\']', content))
        
        if http_resources:
            results["vulnerabilities"].append({
                "type": "mixed_content",
                "severity": "medium",
                "description": f"Mixed content found: {len(http_resources)} HTTP resources on HTTPS page",
                "recommendation": "Update all resources to use HTTPS instead of HTTP"
            })

async def check_external_forms(content: str, url: str, results: Dict) -> None:
    """Check for forms submitting to external domains"""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # Find all forms
    forms = re.findall(r'<form[^>]*action=["\']([^"\']+)["\']', content)
    
    for form_action in forms:
        # Check if form submits to external domain
        if form_action.startswith(('http://', 'https://')):
            form_domain = urlparse(form_action).netloc
            if form_domain != domain:
                results["vulnerabilities"].append({
                    "type": "external_form",
                    "severity": "high",
                    "description": f"Form submitting to external domain: {form_domain}",
                    "recommendation": "Ensure forms submit to your own domain or verify the external domain is trusted"
                })

async def check_outdated_libraries(content: str, results: Dict) -> None:
    """Check for outdated JavaScript libraries"""
    # Common outdated libraries to check (simplified for hackathon)
    outdated_libraries = {
        r'jquery[.-]?([1-2]\.[0-9]+\.[0-9]+)\.min\.js': {
            "name": "jQuery",
            "version_pattern": r'([1-2]\.[0-9]+\.[0-9]+)',
            "latest": "3.6.0",
            "severity": "medium",
            "description": "Outdated jQuery library may contain security vulnerabilities",
            "recommendation": "Update to jQuery 3.6.0 or later"
        },
        r'bootstrap[.-]?([1-4]\.[0-9]+\.[0-9]+)\.min\.js': {
            "name": "Bootstrap",
            "version_pattern": r'([1-4]\.[0-9]+\.[0-9]+)',
            "latest": "5.1.3",
            "severity": "low",
            "description": "Outdated Bootstrap library may contain security vulnerabilities",
            "recommendation": "Update to Bootstrap 5.1.3 or later"
        },
        r'angular[.-]?([1]\.[0-9]+\.[0-9]+)\.min\.js': {
            "name": "AngularJS",
            "version_pattern": r'([1]\.[0-9]+\.[0-9]+)',
            "latest": "1.8.2",
            "severity": "medium",
            "description": "Outdated AngularJS library may contain security vulnerabilities",
            "recommendation": "Update to AngularJS 1.8.2 or migrate to Angular"
        }
    }
    
    for pattern, info in outdated_libraries.items():
        matches = re.findall(pattern, content)
        if matches:
            results["vulnerabilities"].append({
                "type": "outdated_library",
                "library": info["name"],
                "version": matches[0],
                "latest": info["latest"],
                "severity": info["severity"],
                "description": info["description"],
                "recommendation": info["recommendation"]
            })

async def check_common_vulnerabilities(content: str, url: str, results: Dict) -> None:
    """Check for common web vulnerabilities"""
    # Check for potential XSS vulnerabilities
    if re.search(r'document\.write\s*\(\s*location\.hash', content) or \
       re.search(r'eval\s*\(\s*location\.hash', content) or \
       re.search(r'innerHTML\s*=\s*location', content):
        results["vulnerabilities"].append({
            "type": "potential_xss",
            "severity": "high",
            "description": "Potential XSS vulnerability: Unfiltered user input used in DOM manipulation",
            "recommendation": "Sanitize user input before using it in DOM manipulation"
        })
    
    # Check for potential SQL injection vulnerabilities
    if re.search(r'SELECT\s+.*\s+FROM\s+.*\s+WHERE\s+.*=\s*[\'"]\s*\+', content) or \
       re.search(r'INSERT\s+INTO\s+.*\s+VALUES\s*\(\s*[\'"]\s*\+', content):
        results["vulnerabilities"].append({
            "type": "potential_sqli",
            "severity": "high",
            "description": "Potential SQL injection vulnerability: Dynamic SQL queries with string concatenation",
            "recommendation": "Use parameterized queries or prepared statements"
        })
    
    # Check for insecure cookie settings
    if not re.search(r'Set-Cookie:.*HttpOnly', str(content)) or \
       not re.search(r'Set-Cookie:.*Secure', str(content)):
        results["vulnerabilities"].append({
            "type": "insecure_cookies",
            "severity": "medium",
            "description": "Insecure cookie settings: Missing HttpOnly or Secure flags",
            "recommendation": "Set HttpOnly and Secure flags on cookies containing sensitive information"
        })

def get_demo_site_results(url: str) -> Dict[str, Any]:
    """Get demo results for website scan"""
    return {
        "status": "success",
        "site_url": url,
        "vulnerabilities": [
            {
                "type": "missing_header",
                "header": "Content-Security-Policy",
                "severity": "high",
                "description": "Content Security Policy (CSP) header is missing",
                "recommendation": "Implement a Content Security Policy to prevent XSS attacks"
            },
            {
                "type": "missing_header",
                "header": "X-XSS-Protection",
                "severity": "medium",
                "description": "X-XSS-Protection header is missing",
                "recommendation": "Add X-XSS-Protection header to enable browser's XSS filter"
            },
            {
                "type": "mixed_content",
                "severity": "medium",
                "description": "Mixed content found: 3 HTTP resources on HTTPS page",
                "recommendation": "Update all resources to use HTTPS instead of HTTP"
            },
            {
                "type": "outdated_library",
                "library": "jQuery",
                "version": "1.12.4",
                "latest": "3.6.0",
                "severity": "medium",
                "description": "Outdated jQuery library may contain security vulnerabilities",
                "recommendation": "Update to jQuery 3.6.0 or later"
            },
            {
                "type": "insecure_cookies",
                "severity": "medium",
                "description": "Insecure cookie settings: Missing HttpOnly or Secure flags",
                "recommendation": "Set HttpOnly and Secure flags on cookies containing sensitive information"
            }
        ],
        "summary": {
            "high_severity": 1,
            "medium_severity": 4,
            "low_severity": 0,
            "total": 5
        }
    }