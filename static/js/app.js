document.addEventListener('DOMContentLoaded', () => {
    console.log('Script chargé');

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
                console.log('submitReservation appelé');

                // Validation de l'heure (optionnel)
                if (!this.isTimeValid(this.time)) {
                    this.message = 'Veuillez choisir une heure entre 9h et 20h.';
                    this.messageType = 'error';
                    return;
                }

                // Afficher les données dans la console avant l'envoi
                console.log('Données envoyées:', {
                    name: this.name,
                    phone: this.phone,
                    date: this.date,
                    time: this.time
                });

                try {
                    const response = await fetch('/api/reserve/', {
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

                    // Afficher la réponse du serveur dans la console
                    const result = await response.json();
                    console.log('Réponse du serveur:', result);

                    // Vérifier si la réponse est OK (status code 200-299)
                    

                    this.message = result.message;
                    this.messageType = result.status;  // 'success' ou 'error'
                } catch (error) {
                    // Afficher l'erreur dans la console
                    console.error('Error:', error);
                    this.message = `Erreur lors de la réservation. Veuillez réessayer. (${error.message})`;
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
});
