/**
 * CampusAI - Client Script
 * Handles incident reporting, image previews, 1-click sample presets, Kanban workflow, and Chart.js analytics
 */

// ==========================================
// Incident Image Upload & Preview Handler
// ==========================================

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById("dropzoneContent").style.display = "none";
        const previewContainer = document.getElementById("imagePreviewContainer");
        previewContainer.style.display = "block";
        document.getElementById("imagePreview").src = e.target.result;
        document.getElementById("previewFilename").textContent = file.name;
    };
    reader.readAsDataURL(file);
}

function handleBuildingChange(val) {
    const otherBox = document.getElementById("otherBuildingContainer");
    const otherInput = document.getElementById("otherBuilding");
    if (!otherBox) return;
    if (val === "Other") {
        otherBox.style.display = "block";
        if (otherInput) {
            otherInput.required = true;
            otherInput.focus();
        }
    } else {
        otherBox.style.display = "none";
        if (otherInput) {
            otherInput.required = false;
            otherInput.value = "";
        }
    }
}


// ==========================================
// Form Submission & Multimodal AI Triage
// ==========================================

async function handleIncidentSubmit(e) {
    e.preventDefault();
    const btn = document.getElementById("btnSubmitIncident");
    const originalText = btn.innerHTML;

    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing with Vertex AI & Gemini Vision...`;

    const form = document.getElementById("incidentForm");
    const formData = new FormData(form);

    try {
        const response = await fetch("/api/incidents/report", {
            method: "POST",
            body: formData
        });

        const res = await response.json();

        if (response.ok && res.success) {
            const inc = res.incident;
            const diag = inc.ai_diagnosis;

            // Populate Modal
            document.getElementById("mTicketTitle").textContent = inc.title;
            document.getElementById("mTicketMeta").textContent = `Ticket ID: ${inc.id} • ${inc.building} (${inc.room})`;
            document.getElementById("mCategory").textContent = diag.category;

            // Severity styling
            const sevPill = document.getElementById("mSeverityPill");
            const sevText = document.getElementById("mSeverity");
            sevText.textContent = diag.severity;
            sevPill.className = `severity-pill-large ${diag.severity.toLowerCase()}`;

            // Hazard alert box
            const hazardBox = document.getElementById("mHazardBox");
            if (diag.hazard_detected) {
                hazardBox.style.display = "flex";
                document.getElementById("mHazardType").textContent = diag.hazard_type;
            } else {
                hazardBox.style.display = "none";
            }

            document.getElementById("mDiagnosis").textContent = diag.diagnosis;
            document.getElementById("mRecommendedAction").textContent = diag.recommended_action;
            document.getElementById("mTechnician").textContent = diag.required_technician;
            document.getElementById("mRepairTime").textContent = `${diag.estimated_repair_hours} Hours`;

            // Confidence bar
            document.getElementById("mConfidenceBar").style.width = `${diag.confidence_score}%`;
            document.getElementById("mConfidenceText").textContent = `${diag.confidence_score}% AI Confidence (${diag.ai_engine || 'Gemini Vision'})`;
            document.getElementById("mTicketId").textContent = inc.id;

            // Show modal
            document.getElementById("diagnosticModal").classList.add("active");
        } else {
            let errorMsg = "Submission failed";
            if (res && res.detail) {
                if (Array.isArray(res.detail)) {
                    errorMsg = res.detail.map(d => `${d.loc ? d.loc.slice(-1)[0] + ': ' : ''}${d.msg}`).join('\n');
                } else if (typeof res.detail === 'object') {
                    errorMsg = JSON.stringify(res.detail);
                } else {
                    errorMsg = res.detail;
                }
            }
            alert("Error analyzing incident:\n" + errorMsg);
        }
    } catch (err) {
        console.error("Submission failed:", err);
        alert("Server error occurred while dispatching incident.");
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

function closeDiagnosticModal() {
    document.getElementById("diagnosticModal").classList.remove("active");
}

window.addEventListener("click", function(e) {
    const modal = document.getElementById("diagnosticModal");
    if (e.target === modal) {
        closeDiagnosticModal();
    }
});


// ==========================================
// Maintenance Dispatcher Kanban
// ==========================================

let allIncidentsCache = [];

async function fetchAndRenderKanban() {
    try {
        const res = await fetch("/api/incidents");
        allIncidentsCache = await res.json();
        renderKanban(allIncidentsCache);
    } catch (err) {
        console.error("Error loading incidents:", err);
    }
}

function renderKanban(incidents) {
    const cols = {
        "Reported": document.getElementById("colReported"),
        "Dispatched": document.getElementById("colDispatched"),
        "In Repair": document.getElementById("colInRepair"),
        "Resolved": document.getElementById("colResolved")
    };

    if (!cols["Reported"]) return;

    // Reset columns
    Object.values(cols).forEach(c => c.innerHTML = "");
    const counts = { "Reported": 0, "Dispatched": 0, "In Repair": 0, "Resolved": 0 };

    incidents.forEach(inc => {
        const status = inc.status || "Reported";
        counts[status] = (counts[status] || 0) + 1;
        const targetCol = cols[status] || cols["Reported"];

        const diag = inc.ai_diagnosis || {};
        const sevClass = (diag.severity || "moderate").toLowerCase();

        const card = document.createElement("div");
        card.className = "incident-card";
        card.innerHTML = `
            <div class="inc-card-top">
                <span class="inc-id-tag">${inc.id}</span>
                <span class="severity-pill-large ${sevClass}" style="font-size: 0.65rem; padding: 0.2rem 0.5rem;">
                    ${diag.severity || 'Moderate'}
                </span>
            </div>
            <h4 class="inc-card-title">${escapeHtml(inc.title)}</h4>
            <div class="inc-card-loc">
                <i class="fa-solid fa-location-dot"></i>
                <span>${escapeHtml(inc.building)} • ${escapeHtml(inc.room)}</span>
            </div>
            <div class="inc-card-diag">
                <strong>AI Category:</strong> ${diag.category || 'General'}<br>
                <small>${diag.hazard_detected ? '🚨 ' + diag.hazard_type : diag.recommended_action || ''}</small>
            </div>
            <div class="inc-card-footer">
                <small style="color: var(--text-muted); font-size: 0.7rem;">${(inc.timestamp || '').substring(0, 10)}</small>
                ${getNextStageButton(inc.id, status)}
            </div>
        `;
        targetCol.appendChild(card);
    });

    // Render empty state for zero-count columns
    Object.keys(cols).forEach(st => {
        if (counts[st] === 0) {
            cols[st].innerHTML = `
                <div class="empty-column-placeholder" style="text-align: center; color: var(--text-muted); font-size: 0.82rem; padding: 2.5rem 1rem; border: 1px dashed rgba(255, 255, 255, 0.08); border-radius: 10px;">
                    <i class="fa-solid fa-folder-open" style="font-size: 1.6rem; margin-bottom: 0.6rem; opacity: 0.35; display: block;"></i>
                    No ${st.toLowerCase()} tickets
                </div>`;
        }
    });

    // Update header count badges
    document.getElementById("countReported").textContent = counts["Reported"] || 0;
    document.getElementById("countDispatched").textContent = counts["Dispatched"] || 0;
    document.getElementById("countInRepair").textContent = counts["In Repair"] || 0;
    document.getElementById("countResolved").textContent = counts["Resolved"] || 0;
}

function getNextStageButton(id, currentStatus) {
    if (currentStatus === "Reported") {
        return `<button class="btn-move-stage" onclick="updateIncidentStage('${id}', 'Dispatched')">Dispatch &rarr;</button>`;
    } else if (currentStatus === "Dispatched") {
        return `<button class="btn-move-stage" onclick="updateIncidentStage('${id}', 'In Repair')">Start Repair &rarr;</button>`;
    } else if (currentStatus === "In Repair") {
        return `<button class="btn-move-stage" style="background: rgba(16, 185, 129, 0.2); color: #4ade80;" onclick="updateIncidentStage('${id}', 'Resolved')">Resolve &check;</button>`;
    } else {
        return `<small style="color: #4ade80; font-weight: 700;">Closed</small>`;
    }
}

async function updateIncidentStage(incidentId, nextStatus) {
    try {
        const res = await fetch(`/api/incidents/${incidentId}/status`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: nextStatus })
        });
        if (res.ok) {
            await fetchAndRenderKanban();
        }
    } catch (err) {
        console.error("Failed to update status:", err);
    }
}

function filterKanbanCards() {
    const cat = document.getElementById("filterCategory").value;
    const sev = document.getElementById("filterSeverity").value;
    const bld = document.getElementById("filterBuilding").value;
    const search = document.getElementById("kanbanSearch").value.toLowerCase().trim();

    const filtered = allIncidentsCache.filter(inc => {
        const diag = inc.ai_diagnosis || {};
        const matchCat = !cat || diag.category === cat;
        const matchSev = !sev || diag.severity === sev;
        const matchBld = !bld || inc.building === bld;
        const matchSearch = !search || 
            (inc.title || '').toLowerCase().includes(search) || 
            (inc.id || '').toLowerCase().includes(search) || 
            (inc.room || '').toLowerCase().includes(search);

        return matchCat && matchSev && matchBld && matchSearch;
    });

    renderKanban(filtered);
}


// ==========================================
// Executive Analytics Charts (Chart.js)
// ==========================================

let trendsChartInstance = null;
let deptChartInstance = null;
let bldChartInstance = null;
let sevChartInstance = null;

async function initAnalyticsDashboard() {
    try {
        const [kpiRes, trendsRes] = await Promise.all([
            fetch("/api/analytics/summary"),
            fetch("/api/analytics/trends")
        ]);

        const kpiData = await kpiRes.json();
        const trendsData = await trendsRes.json();

        // 1. Time Series Line Chart (Reported vs Resolved)
        const trendsCtx = document.getElementById("incidentTrendsChart");
        if (trendsCtx) {
            if (trendsChartInstance) trendsChartInstance.destroy();
            trendsChartInstance = new Chart(trendsCtx.getContext("2d"), {
                type: "line",
                data: {
                    labels: trendsData.dates,
                    datasets: [
                        {
                            label: "Incidents Reported",
                            data: trendsData.reported_counts,
                            borderColor: "#3b82f6",
                            backgroundColor: "rgba(59, 130, 246, 0.15)",
                            borderWidth: 3,
                            fill: true,
                            tension: 0.35
                        },
                        {
                            label: "Work Orders Resolved",
                            data: trendsData.resolved_counts,
                            borderColor: "#10b981",
                            backgroundColor: "rgba(16, 185, 129, 0.15)",
                            borderWidth: 3,
                            fill: true,
                            tension: 0.35
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, grid: { color: "rgba(255, 255, 255, 0.05)" } },
                        x: { grid: { color: "rgba(255, 255, 255, 0.05)" } }
                    }
                }
            });
        }

        // 2. Department Breakdown Doughnut Chart
        const deptCtx = document.getElementById("deptDistributionChart");
        if (deptCtx) {
            if (deptChartInstance) deptChartInstance.destroy();
            deptChartInstance = new Chart(deptCtx.getContext("2d"), {
                type: "doughnut",
                data: {
                    labels: kpiData.department_breakdown.labels,
                    datasets: [{
                        data: kpiData.department_breakdown.data,
                        backgroundColor: ["#3b82f6", "#06b6d4", "#8b5cf6", "#10b981", "#f59e0b"],
                        borderColor: "#111827",
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: "bottom", labels: { color: "#9ca3af", font: { size: 11 } } }
                    }
                }
            });
        }

        // 3. Building Breakdown Bar Chart
        const bldCtx = document.getElementById("buildingChart");
        if (bldCtx) {
            if (bldChartInstance) bldChartInstance.destroy();
            bldChartInstance = new Chart(bldCtx.getContext("2d"), {
                type: "bar",
                data: {
                    labels: kpiData.building_breakdown.labels,
                    datasets: [{
                        label: "Incident Frequency",
                        data: kpiData.building_breakdown.data,
                        backgroundColor: "#8b5cf6",
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, grid: { color: "rgba(255, 255, 255, 0.05)" } },
                        x: { grid: { color: "rgba(255, 255, 255, 0.05)" } }
                    }
                }
            });
        }

        // 4. Severity Distribution Chart
        const sevCtx = document.getElementById("severityChart");
        if (sevCtx) {
            if (sevChartInstance) sevChartInstance.destroy();
            sevChartInstance = new Chart(sevCtx.getContext("2d"), {
                type: "doughnut",
                data: {
                    labels: kpiData.severity_breakdown.labels,
                    datasets: [{
                        data: kpiData.severity_breakdown.data,
                        backgroundColor: ["#ef4444", "#f59e0b", "#3b82f6", "#10b981"],
                        borderColor: "#111827",
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: "bottom", labels: { color: "#9ca3af", font: { size: 11 } } }
                    }
                }
            });
        }

    } catch (err) {
        console.error("Error loading analytics:", err);
    }
}

function escapeHtml(text) {
    if (!text) return '';
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
