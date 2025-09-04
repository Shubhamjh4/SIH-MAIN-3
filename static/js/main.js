// Toggle mobile menu
document.getElementById('mobile-menu-button').addEventListener('click', function() {
    document.getElementById('mobile-menu').classList.toggle('hidden');
});

// Toggle user menu dropdown
document.getElementById('user-menu-button')?.addEventListener('click', function() {
    document.getElementById('user-menu').classList.toggle('hidden');
});

// Close dropdowns when clicking outside
document.addEventListener('click', function(event) {
    const userMenu = document.getElementById('user-menu');
    const userMenuButton = document.getElementById('user-menu-button');
    
    if (userMenu && !userMenu.contains(event.target) && !userMenuButton.contains(event.target)) {
        userMenu.classList.add('hidden');
    }
});

// Handle offline mode
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(registration => {
                console.log('ServiceWorker registration successful');
            })
            .catch(err => {
                console.log('ServiceWorker registration failed: ', err);
            });
    });
}

// Check online/offline status
window.addEventListener('online', function() {
    document.body.classList.remove('offline');
    syncOfflineData();
});

window.addEventListener('offline', function() {
    document.body.classList.add('offline');
});

// Function to sync offline data
async function syncOfflineData() {
    if (navigator.onLine) {
        const offlineData = JSON.parse(localStorage.getItem('offlineData') || '[]');
        if (offlineData.length > 0) {
            try {
                const response = await fetch('/api/sync/sync/sync_offline_changes/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(offlineData)
                });
                
                if (response.ok) {
                    localStorage.removeItem('offlineData');
                    console.log('Offline data synced successfully');
                }
            } catch (error) {
                console.error('Error syncing offline data:', error);
            }
        }
    }
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Handle language selection
const languageSelect = document.getElementById('language-select');
if (languageSelect) {
    languageSelect.addEventListener('change', function() {
        const form = this.closest('form');
        form.submit();
    });
}

// Track game plays for leaderboard (requires logged-in session)
window.trackGame = function(name, points) {
    try {
        fetch('/gamification/api/points-history/track_game/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            credentials: 'same-origin',
            keepalive: true,
            body: JSON.stringify({ name: name, points: points || 5 })
        });
    } catch (e) {
        // ignore
    }
}