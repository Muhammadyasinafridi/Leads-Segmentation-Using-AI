document.getElementById('LeadForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent page reload

    // Collect clustermapping matching FastAPI Pydantic field names
    const clustermapping = {
        TotalVisits: parseInt(document.getElementById('Total_Visits').value) || 0,
        TotalTimeSpent_sec: parseInt(document.getElementById('TotalTimeSpent_sec').value) || 0,
        PageViewsPer_visit: parseInt(document.getElementById('PageViews_PerVisit').value) || 0,
        Lead_Origin: document.getElementById('Lead_Origin').value,
        Lead_Source: document.getElementById('Lead_Source').value,
        Occupation: document.getElementById('Occupation').value
    };

    try {
        //endpoint URL: /Segment_Lead on 127.0.0.1
        const response = await fetch('https://leads-segmentation-using-ai.onrender.com/Segment_Lead', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(clustermapping)
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || `Server status: ${response.status}`);
        }

        // Parse JSON response
        const data = await response.json();
        const pred = data.prediction || {};

        // Populate HTML fields
        const clusterEl = document.getElementById('clusterText');
        const tierEl = document.getElementById('tierBadge');
        const rateEl = document.getElementById('rateText');

        if (clusterEl) clusterEl.innerText = data.cluster_id ?? '-';
        if (tierEl) tierEl.innerText = `Lead Type: ${pred.lead_type || 'N/A'}`;
        if (rateEl) rateEl.innerText = pred.conversion_rate || 'N/A';

        // Unhide result card
        const resultBox = document.getElementById('resultBox');
        if (resultBox) {
            resultBox.hidden = false;
            resultBox.classList.remove('hidden');
        }

    } catch (error) {
        console.error('Frontend Error:', error);
        alert(`Error: ${error.message}`);
    }
});
