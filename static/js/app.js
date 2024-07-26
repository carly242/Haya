new Vue({
    el: '#app',
    data: {
        name: '',
        phone: '',
        date: '',
        time: '',
        message: '',
        messageType: ''  // Propriété pour le type de message (succès ou erreur)
    },
    methods: {
        async submitReservation() {
            // Validation de l'heure (optionnel)
            if (!this.isTimeValid(this.time)) {
                this.message = 'Veuillez choisir une heure entre 9h et 20h.';
                this.messageType = 'error';
                return;
            }

            try {
                const response = await fetch('/api/reserve', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')  // Ajout du token CSRF pour Django
                    },
                    body: JSON.stringify({
                        name: this.name,
                        phone: this.phone,
                        date: this.date,
                        time: this.time
                    })
                });

                const result = await response.json();
                this.message = result.message;
                this.messageType = result.status;  // 'success' ou 'error'
            } catch (error) {
                console.error('Error:', error);
                this.message = 'Erreur lors de la réservation. Veuillez réessayer.';
                this.messageType = 'error';
            }
        },
        isTimeValid(time) {
            // Validation de l'heure
            const hour = parseInt(time.split(':')[0], 10);
            return hour >= 9 && hour <= 20;
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
