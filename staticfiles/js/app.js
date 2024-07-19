new Vue({
    el: '#app',
    data: {
        name: '',
        phone: '',
        date: '',
        time: '',
        message: ''
    },
    methods: {
        async submitReservation() {
            try {
                const response = await fetch('/api/reserve', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')  // Add CSRF token for Django
                    },
                    body: JSON.stringify({
                        name: this.name,
                        phone: this.phone,
                        date: this.date,
                        time: this.time
                    })
                });
                const result = await response.json();
                if (result.status === 'success') {
                    this.message = result.message;
                } else {
                    this.message = result.message;
                }
            } catch (error) {
                this.message = 'Erreur lors de la réservation. Veuillez réessayer.';
            }
        }
    }
});

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
