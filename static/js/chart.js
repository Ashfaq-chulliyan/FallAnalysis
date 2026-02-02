document.addEventListener("DOMContentLoaded", function () {

    // 1️⃣ Make sure data exists
    if (!window.dashboardData) {
        console.error("dashboardData not found");
        return;
    }

    const {
        lineLabels,
        lineCounts,
        barLabels,
        barCounts,
        pie1Labels,
        pie1Counts,
        pie2Labels,
        pie2Counts
    } = window.dashboardData;

    // 2️⃣ Helper to create charts safely
    function createChart(canvasId, config) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        // Destroy old chart if reloaded
        const oldChart = Chart.getChart(canvas);
        if (oldChart) oldChart.destroy();

        new Chart(canvas, config);
    }

    // 3️⃣ LINE CHART
    createChart("lineChart", {
        type: "line",
        data: {
            labels: lineLabels,
            datasets: [{
                label: "Incidents",
                data: lineCounts,
                borderWidth: 2,
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // 4️⃣ PIE – INCIDENT TYPES
    createChart("pieChart2", {
        type: "pie",
        data: {
            labels: pie2Labels,
            datasets: [{
                data: pie2Counts
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    

    // 6️⃣ BAR CHART
    createChart("barChart", {
        type: "bar",
        data: {
            labels: barLabels,
            datasets: [{
                label: "Total",
                data: barCounts,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

});


