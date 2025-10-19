// Startup Surakshate - Dashboard JavaScript
// Handles: creating/running scans, polling results, demo mode, and report download

document.addEventListener('DOMContentLoaded', function() {
    const scanForm = document.getElementById('scanForm');
    const startScanBtn = document.getElementById('startScanBtn');
    const demoScanBtn = document.getElementById('demoScanBtn');
    const generateReportBtn = document.getElementById('generateReportBtn');
    const newScanBtn = document.getElementById('newScanBtn');

    const scanStatus = document.getElementById('scanStatus');
    const scanStatusText = document.getElementById('scanStatusText');
    const scanResults = document.getElementById('scanResults');

    // Result fields
    const resultScanName = document.getElementById('resultScanName');
    const resultScanUrl = document.getElementById('resultScanUrl');
    const resultScanType = document.getElementById('resultScanType');
    const resultScanStarted = document.getElementById('resultScanStarted');
    const resultScanCompleted = document.getElementById('resultScanCompleted');
    const resultScanStatus = document.getElementById('resultScanStatus');
    const vulnerabilitiesList = document.getElementById('vulnerabilitiesList');

    // Summary counters
    const highCount = document.getElementById('highCount');
    const mediumCount = document.getElementById('mediumCount');
    const lowCount = document.getElementById('lowCount');
    const totalCount = document.getElementById('totalCount');

    // AI sections
    const aiOverview = document.getElementById('aiOverview');
    const aiFindings = document.getElementById('aiFindings');
    const aiRecommendations = document.getElementById('aiRecommendations');
    const aiRisk = document.getElementById('aiRisk');

    let currentJobId = null;

    if (scanForm) {
        scanForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            await handleStartScan();
        });
    }

    if (demoScanBtn) {
        demoScanBtn.addEventListener('click', async function() {
            await handleDemoScan();
        });
    }

    if (newScanBtn) {
        newScanBtn.addEventListener('click', function() {
            resetUI();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    if (generateReportBtn) {
        generateReportBtn.addEventListener('click', function() {
            if (!currentJobId) {
                toast('No completed scan to generate report for', 'error');
                return;
            }
            window.open(`/api/report/${currentJobId}`, '_blank');
        });
    }

    async function handleStartScan() {
        const name = document.getElementById('scanName').value.trim();
        const url = document.getElementById('scanUrl').value.trim();
        const scanType = document.querySelector('input[name="scanType"]:checked')?.value || 'repository';

        if (!url) {
            toast('Please enter a URL to scan', 'error');
            return;
        }

        setLoading(true, 'Creating scan job...');
        try {
            const createRes = await fetch('/api/scan/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url, scan_type: scanType, name })
            });

            if (!createRes.ok) throw new Error((await createRes.json()).detail || 'Failed to create scan');
            const createData = await createRes.json();
            currentJobId = createData.job_id;

            setLoading(true, 'Starting scan...');
            const runRes = await fetch(`/api/scan/run/${currentJobId}`, { method: 'POST' });
            if (!runRes.ok) throw new Error((await runRes.json()).detail || 'Failed to start scan');

            setLoading(true, 'Scan in progress...');
            pollForResults(currentJobId);
        } catch (err) {
            console.error(err);
            toast(err.message || 'Scan failed to start', 'error');
            setLoading(false);
        }
    }

    async function pollForResults(jobId) {
        const pollIntervalMs = 2000;
        const maxWaitMs = 2 * 60 * 1000; // 2 minutes
        const deadline = Date.now() + maxWaitMs;

        while (Date.now() < deadline) {
            try {
                const res = await fetch(`/api/scan/${jobId}`);
                if (res.ok) {
                    const data = await res.json();
                    const scan = data.scan || {};
                    if (scan.status === 'completed') {
                        renderResults(scan);
                        setLoading(false);
                        return;
                    }
                    if (scan.status === 'failed') {
                        setLoading(false);
                        toast('Scan failed. Showing any available details.', 'error');
                        renderResults(scan);
                        return;
                    }
                }
            } catch (e) {
                // keep polling, could be transient
            }
            await sleep(pollIntervalMs);
        }
        setLoading(false);
        toast('Scan timed out. Please try again or use Demo Scan.', 'error');
    }

    async function handleDemoScan() {
        // Build a fake scan using backend demo behavior for both types
        const url = 'https://example.com';
        const scanType = document.querySelector('input[name="scanType"]:checked')?.value || 'website';
        setLoading(true, 'Running demo scan...');
        try {
            const createRes = await fetch('/api/scan/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url, scan_type: scanType, name: 'Demo Scan' })
            });
            if (!createRes.ok) throw new Error('Failed to create demo job');
            const createData = await createRes.json();
            currentJobId = createData.job_id;

            // Directly call run; backend will honor DEMO_MODE if set
            await fetch(`/api/scan/run/${currentJobId}`, { method: 'POST' });
            await sleep(800); // small delay before polling
            await pollForResults(currentJobId);
        } catch (e) {
            console.error(e);
            setLoading(false);
            // Pure front-end fallback if backend is unreachable
            const demoScan = buildPureDemo(scanType, url);
            renderResults(demoScan);
            toast('Showing demo results (offline mode).', 'info');
        }
    }

    function renderResults(scan) {
        try {
            scanResults.classList.remove('hidden');

            const results = scan.results || scan; // support direct object
            const summary = results.summary || scan.summary || { high_severity: 0, medium_severity: 0, low_severity: 0, total: 0 };
            const vulns = (results && results.vulnerabilities) ? results.vulnerabilities : [];

            resultScanName.textContent = scan.name || scan.url || '';
            resultScanUrl.textContent = scan.url || results.repo_url || results.site_url || '';
            resultScanType.textContent = (scan.scan_type || '').toString();
            resultScanStarted.textContent = scan.created_at ? formatDate(scan.created_at) : '';
            resultScanCompleted.textContent = scan.completed_at ? formatDate(scan.completed_at) : '';
            resultScanStatus.textContent = (scan.status || 'Completed').toString();

            highCount.textContent = summary.high_severity || 0;
            mediumCount.textContent = summary.medium_severity || 0;
            lowCount.textContent = summary.low_severity || 0;
            totalCount.textContent = summary.total || vulns.length || 0;

            // AI
            const ai = scan.summary || {};
            aiOverview.textContent = ai.overview || '';
            aiFindings.textContent = ai.key_findings || '';
            aiRecommendations.textContent = ai.recommendations || '';
            aiRisk.textContent = ai.risk_assessment || '';

            // Vulns list
            vulnerabilitiesList.innerHTML = '';
            if (vulns.length === 0) {
                const none = document.createElement('div');
                none.className = 'text-gray-600';
                none.textContent = 'No vulnerabilities found.';
                vulnerabilitiesList.appendChild(none);
            } else {
                vulns.forEach(v => {
                    const item = document.createElement('div');
                    item.className = 'p-4 rounded-md border vulnerability-card';
                    const sev = (v.severity || 'low').toLowerCase();
                    if (sev === 'high') item.classList.add('vulnerability-high');
                    if (sev === 'medium') item.classList.add('vulnerability-medium');
                    if (sev === 'low') item.classList.add('vulnerability-low');
                    item.innerHTML = `
                        <div class="badge badge-${sev} mb-2">${sev.toUpperCase()}</div>
                        <div class="font-semibold">${(v.type || 'Issue').toString().replace('_',' ')}</div>
                        ${v.package ? `<div class="text-sm text-gray-700">Package: ${v.package} ${v.version ? `(${v.version})` : ''}</div>` : ''}
                        ${v.file ? `<div class="text-sm text-gray-700">File: ${v.file}</div>` : ''}
                        ${v.header ? `<div class="text-sm text-gray-700">Header: ${v.header}</div>` : ''}
                        <div class="text-sm text-gray-700 mt-1">${v.description || ''}</div>
                        <div class="text-sm text-gray-800 mt-1"><span class="font-medium">Recommendation:</span> ${v.recommendation || ''}</div>
                    `;
                    vulnerabilitiesList.appendChild(item);
                });
            }
        } catch (e) {
            console.error('Render error:', e);
            toast('Failed to render results', 'error');
        }
    }

    function buildPureDemo(scanType, url) {
        const now = new Date().toISOString();
        const demo = {
            id: 'demo-' + Math.random().toString(36).slice(2),
            name: 'Demo Scan',
            url: url,
            scan_type: scanType,
            status: 'completed',
            created_at: now,
            completed_at: now,
            results: {
                vulnerabilities: [],
                summary: { high_severity: 0, medium_severity: 0, low_severity: 0, total: 0 }
            },
            summary: {
                overview: 'Demo overview of findings.',
                key_findings: 'Sample high and medium issues shown below.',
                recommendations: 'Update vulnerable packages and add security headers.',
                risk_assessment: 'Medium'
            }
        };
        if (scanType === 'repository') {
            demo.results.vulnerabilities = [
                { type: 'outdated_dependency', package: 'axios', version: '0.19.2', severity: 'high', description: 'Known SSRF vulnerability', recommendation: 'Update to >= 0.21.1' },
                { type: 'exposed_secret', file: 'config.js', severity: 'high', description: 'API key present in source', recommendation: 'Move to env vars' }
            ];
        } else {
            demo.results.vulnerabilities = [
                { type: 'missing_header', header: 'Content-Security-Policy', severity: 'high', description: 'CSP missing', recommendation: 'Add CSP header' },
                { type: 'mixed_content', severity: 'medium', description: 'HTTP resources on HTTPS page', recommendation: 'Use HTTPS for all assets' }
            ];
        }
        demo.results.summary.total = demo.results.vulnerabilities.length;
        demo.results.summary.high_severity = demo.results.vulnerabilities.filter(v => v.severity === 'high').length;
        demo.results.summary.medium_severity = demo.results.vulnerabilities.filter(v => v.severity === 'medium').length;
        demo.results.summary.low_severity = demo.results.vulnerabilities.filter(v => v.severity === 'low').length;
        return demo;
    }

    function setLoading(isLoading, text = 'Scanning...') {
        if (!scanStatus) return;
        if (isLoading) {
            scanStatus.classList.remove('hidden');
            scanStatusText.textContent = text;
            scanResults.classList.add('hidden');
        } else {
            scanStatus.classList.add('hidden');
        }
    }

    function formatDate(iso) {
        try {
            return new Date(iso).toLocaleString();
        } catch {
            return iso;
        }
    }

    function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

    function toast(message, type = 'info') {
        // simple toast using alert fallback if styles not present
        try {
            const evt = new CustomEvent('toast', { detail: { message, type } });
            window.dispatchEvent(evt);
        } catch {
            console.log(type.toUpperCase() + ': ' + message);
        }
    }
});


