/**
 * Resident Health Analytics - Frontend Logic
 * Handles: Time Range Updates, Modal Zooming, and AI Simulation
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. SELECTORS
    const mainTitle = document.getElementById('main-title');
    const zoomModal = document.getElementById('zoomModal');
    const modalBody = document.getElementById('modalBody');
    const timeButtons = document.querySelectorAll('.time-btn');

    // 2. TIME RANGE UPDATER
    window.updateRange = function (range) {
        // Update page title
        const mainTitle = document.getElementById('main-title');
        if (mainTitle) {
            mainTitle.innerText = `${range} Analysis`;
        }
    
        // Remove active state from all buttons
        document.querySelectorAll('.time-btn').forEach(btn => {
            btn.classList.remove('active-btn');
        });
    
        // Add active state to clicked button
        const activeBtn = document.getElementById(`btn-${range}`);
        if (activeBtn) {
            activeBtn.classList.add('active-btn');
        }
    
        console.log(`Loading ${range} data...`);
    };
    

    // 3. ZOOM MODAL LOGIC
    // Uses Event Delegation to handle any element with 'zoom-target' class
    document.addEventListener('click', (e) => {
        const target = e.target.closest('.zoom-target');
        if (target) {
            const clone = target.cloneNode(true);
            clone.style.cursor = 'default';
            clone.style.width = '100%';
            
            modalBody.innerHTML = '';
            modalBody.appendChild(clone);
            zoomModal.style.display = 'flex';
        }
    });

    window.closeZoom = function() {
        zoomModal.style.display = 'none';
    };

    // Close modal on background click
    window.onclick = (event) => {
        if (event.target === zoomModal) {
            closeZoom();
        }
    };

    // 4. FORM SUBMISSION SIMULATION
    // Handles both Resident Registration and Incident Logging
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const submitBtn = form.querySelector('button');
        if (submitBtn) {
            submitBtn.addEventListener('click', function(e) {
                const buttonText = this.innerText;
                this.innerText = 'Processing...';
                this.disabled = true;

                // Simulate AI Backend Sync
                setTimeout(() => {
                    alert(`${buttonText.replace('Add ', '').replace('Log ', '')} successful!`);
                    this.innerText = buttonText;
                    this.disabled = false;
                    form.reset();
                }, 1000);
            });
        }
    });
});


    // Modal Interaction
    const modal = document.getElementById("chartModal");
    const closeBtn = document.getElementById("closeModal");

    function openChart(title, content) {
        document.getElementById("modalTitle").innerText = title;
        document.getElementById("modalContent").innerText = content;
        modal.style.display = "flex";
    }

    closeBtn.onclick = () => modal.style.display = "none";
    window.onclick = (e) => { if (e.target == modal) modal.style.display = "none"; }

