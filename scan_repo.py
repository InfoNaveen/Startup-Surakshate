import httpx
import json
import os
from typing import Dict, List, Any
import re

async def scan_github_repo(repo_url: str) -> Dict[str, Any]:
    """
    Scan a GitHub repository for security vulnerabilities
    
    Args:
        repo_url: URL of the GitHub repository
        
    Returns:
        Dict containing scan results
    """
    # Parse GitHub URL to extract owner and repo name
    # Example: https://github.com/owner/repo
    pattern = r"github\.com\/([^\/]+)\/([^\/]+)"
    match = re.search(pattern, repo_url)
    
    if not match:
        return {
            "status": "error",
            "message": "Invalid GitHub repository URL",
            "vulnerabilities": []
        }
    
    owner = match.group(1)
    repo = match.group(2)
    
    # Initialize results
    results = {
        "status": "success",
        "repo_url": repo_url,
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
            return get_demo_repo_results(repo_url)
        
        async with httpx.AsyncClient(timeout=10) as client:
            # Check for package.json to detect dependencies
            package_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/package.json"
            response = await client.get(package_url)
            if response.status_code == 200:
                package_data = response.json()
                results["vulnerabilities"].extend(
                    await check_npm_dependencies(package_data)
                )
            
            # Check for requirements.txt to detect Python dependencies
            requirements_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/requirements.txt"
            response = await client.get(requirements_url)
            if response.status_code == 200:
                requirements_text = response.text
                results["vulnerabilities"].extend(
                    await check_python_dependencies(requirements_text)
                )
            
            # Check for exposed API keys and secrets in common files
            await check_exposed_secrets(client, owner, repo, results)
            
            # Check for insecure configurations
            await check_insecure_configs(client, owner, repo, results)
        
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
            "message": f"Error scanning repository: {str(e)}",
            "vulnerabilities": []
        }

async def check_npm_dependencies(package_data: Dict) -> List[Dict]:
    """Check NPM dependencies for known vulnerabilities"""
    vulnerabilities = []
    
    # Known vulnerable packages (simplified for hackathon)
    vulnerable_packages = {
        "lodash": {"versions": ["<4.17.21"], "severity": "high", "description": "Prototype pollution vulnerability"},
        "axios": {"versions": ["<0.21.1"], "severity": "medium", "description": "Server-side request forgery"},
        "jquery": {"versions": ["<3.5.0"], "severity": "medium", "description": "Cross-site scripting vulnerability"},
        "express": {"versions": ["<4.17.0"], "severity": "low", "description": "Denial of service vulnerability"},
        "react": {"versions": ["<16.13.1"], "severity": "low", "description": "Potential memory leak"}
    }
    
    # Check dependencies
    dependencies = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}
    
    for package, version in dependencies.items():
        if package in vulnerable_packages:
            # Simple version check (in a real app, use semver)
            version_num = version.replace("^", "").replace("~", "")
            if version_num.startswith("<"):
                vulnerabilities.append({
                    "type": "outdated_dependency",
                    "package": package,
                    "version": version,
                    "severity": vulnerable_packages[package]["severity"],
                    "description": vulnerable_packages[package]["description"],
                    "recommendation": f"Update {package} to the latest version"
                })
    
    return vulnerabilities

async def check_python_dependencies(requirements_text: str) -> List[Dict]:
    """Check Python dependencies for known vulnerabilities"""
    vulnerabilities = []
    
    # Known vulnerable packages (simplified for hackathon)
    vulnerable_packages = {
        "django": {"versions": ["<3.2.0"], "severity": "high", "description": "SQL injection vulnerability"},
        "flask": {"versions": ["<2.0.0"], "severity": "medium", "description": "Session cookie vulnerability"},
        "requests": {"versions": ["<2.25.0"], "severity": "low", "description": "SSL certificate validation issue"},
        "pillow": {"versions": ["<8.2.0"], "severity": "high", "description": "Buffer overflow vulnerability"},
        "cryptography": {"versions": ["<3.3.2"], "severity": "medium", "description": "Timing attack vulnerability"}
    }
    
    # Parse requirements.txt
    for line in requirements_text.split("\n"):
        if line and not line.startswith("#"):
            # Simple parsing (in a real app, use a proper parser)
            parts = line.split("==")
            if len(parts) == 2:
                package = parts[0].strip()
                version = parts[1].strip()
                
                if package in vulnerable_packages:
                    # Simple version check
                    if version in vulnerable_packages[package]["versions"]:
                        vulnerabilities.append({
                            "type": "outdated_dependency",
                            "package": package,
                            "version": version,
                            "severity": vulnerable_packages[package]["severity"],
                            "description": vulnerable_packages[package]["description"],
                            "recommendation": f"Update {package} to the latest version"
                        })
    
    return vulnerabilities

async def check_exposed_secrets(client: httpx.AsyncClient, owner: str, repo: str, results: Dict) -> None:
    """Check for exposed API keys and secrets"""
    # Files to check for secrets
    files_to_check = [
        ".env",
        ".env.local",
        ".env.development",
        "config.js",
        "config.json",
        "settings.py"
    ]
    
    # Patterns for common API keys and secrets
    secret_patterns = [
        (r"api[_-]?key['\"]?\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{20,})['\"]", "API Key"),
        (r"secret[_-]?key['\"]?\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{20,})['\"]", "Secret Key"),
        (r"password['\"]?\s*[:=]\s*['\"]([^'\"]{8,})['\"]", "Password"),
        (r"aws[_-]?access[_-]?key[_-]?id['\"]?\s*[:=]\s*['\"]([A-Z0-9]{20})['\"]", "AWS Access Key"),
        (r"aws[_-]?secret[_-]?access[_-]?key['\"]?\s*[:=]\s*['\"]([a-zA-Z0-9/+]{40})['\"]", "AWS Secret Key")
    ]
    
    for file in files_to_check:
        file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{file}"
        try:
            response = await client.get(file_url)
            if response.status_code == 200:
                content = response.text
                for pattern, secret_type in secret_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        results["vulnerabilities"].append({
                            "type": "exposed_secret",
                            "file": file,
                            "severity": "high",
                            "description": f"Exposed {secret_type} found in {file}",
                            "recommendation": f"Remove the {secret_type} from the code and use environment variables or a secure vault"
                        })
        except:
            # Skip if file doesn't exist or can't be accessed
            pass

async def check_insecure_configs(client: httpx.AsyncClient, owner: str, repo: str, results: Dict) -> None:
    """Check for insecure configurations"""
    # Files to check for insecure configs
    config_files = [
        "package.json",
        "webpack.config.js",
        "next.config.js",
        "nuxt.config.js",
        "vue.config.js",
        "settings.py",
        "config.py"
    ]
    
    # Insecure patterns to check
    insecure_patterns = [
        (r"\"allowInsecureProtocol\":\s*true", "Insecure protocol allowed"),
        (r"\"strict\":\s*false", "Strict mode disabled"),
        (r"\"noVerify\":\s*true", "Verification disabled"),
        (r"DEBUG\s*=\s*True", "Debug mode enabled"),
        (r"ALLOWED_HOSTS\s*=\s*\[\s*['\"]\\*['\"]\s*\]", "All hosts allowed")
    ]
    
    for file in config_files:
        file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{file}"
        try:
            response = await client.get(file_url)
            if response.status_code == 200:
                content = response.text
                for pattern, issue in insecure_patterns:
                    if re.search(pattern, content):
                        results["vulnerabilities"].append({
                            "type": "insecure_config",
                            "file": file,
                            "severity": "medium",
                            "description": f"{issue} in {file}",
                            "recommendation": f"Update configuration to use secure settings"
                        })
        except:
            # Skip if file doesn't exist or can't be accessed
            pass

def get_demo_repo_results(repo_url: str) -> Dict[str, Any]:
    """Get demo results for repository scan"""
    return {
        "status": "success",
        "repo_url": repo_url,
        "vulnerabilities": [
            {
                "type": "outdated_dependency",
                "package": "axios",
                "version": "0.19.2",
                "severity": "high",
                "description": "Server-side request forgery vulnerability in axios before 0.21.1 allows attackers to bypass a proxy by providing a URL that responds with a redirect to a UNIX socket.",
                "recommendation": "Update axios to version 0.21.1 or later"
            },
            {
                "type": "outdated_dependency",
                "package": "lodash",
                "version": "4.17.15",
                "severity": "medium",
                "description": "Prototype pollution vulnerability in lodash before 4.17.21 allows attackers to modify object properties via the set, setWith, and update functions.",
                "recommendation": "Update lodash to version 4.17.21 or later"
            },
            {
                "type": "exposed_secret",
                "file": "config.js",
                "severity": "high",
                "description": "Exposed API Key found in config.js",
                "recommendation": "Remove the API Key from the code and use environment variables or a secure vault"
            },
            {
                "type": "insecure_config",
                "file": "webpack.config.js",
                "severity": "medium",
                "description": "Insecure protocol allowed in webpack.config.js",
                "recommendation": "Update configuration to use secure settings"
            },
            {
                "type": "outdated_dependency",
                "package": "react",
                "version": "16.8.0",
                "severity": "low",
                "description": "Potential memory leak in React before 16.13.1",
                "recommendation": "Update react to version 16.13.1 or later"
            }
        ],
        "summary": {
            "high_severity": 2,
            "medium_severity": 2,
            "low_severity": 1,
            "total": 5
        }
    }