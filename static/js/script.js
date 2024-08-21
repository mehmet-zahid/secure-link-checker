document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('urlForm');
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const url = document.getElementById('url').value;
        const formData = new FormData();
        formData.append('url', url);

        // Show loading spinner
        loadingDiv.classList.remove('hidden');
        resultsDiv.innerHTML = '';

        fetch('/url-check', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            // Hide loading spinner
            loadingDiv.classList.add('hidden');
            resultsDiv.innerHTML = html;
            animateProgressBars();
        })
        .catch(error => {
            console.error('Error:', error);
            // Hide loading spinner
            loadingDiv.classList.add('hidden');
            resultsDiv.innerHTML = '<div class="error-message">An error occurred while processing your request.</div>';
        });
    });

    function animateProgressBars() {
        const progressBars = document.querySelectorAll('.progress-bar');
        progressBars.forEach(bar => {
            const harmless = bar.querySelector('.progress.harmless');
            const suspicious = bar.querySelector('.progress.suspicious');
            const malicious = bar.querySelector('.progress.malicious');

            if (harmless && suspicious && malicious) {
                harmless.style.width = '0%';
                suspicious.style.width = '0%';
                malicious.style.width = '0%';

                setTimeout(() => {
                    harmless.style.transition = 'width 1s ease-out';
                    suspicious.style.transition = 'width 1s ease-out';
                    malicious.style.transition = 'width 1s ease-out';

                    harmless.style.width = harmless.dataset.width + '%';
                    suspicious.style.width = suspicious.dataset.width + '%';
                    malicious.style.width = malicious.dataset.width + '%';
                }, 100);
            }
        });
    }

    // Initial animation if results are present on page load
    if (resultsDiv.innerHTML.trim() !== '') {
        animateProgressBars();
    }
});