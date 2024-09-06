document.addEventListener('DOMContentLoaded', () => {
    const reservationModal = document.getElementById('reservation-modal');
    const editProfileModal = document.getElementById('edit-profile-modal');
    const reservationDetails = document.getElementById('reservation-details');
    const closeButtons = document.querySelectorAll('.modal .close');
    const viewDetailsButtons = document.querySelectorAll('.view-details-btn');
    const editProfileButton = document.getElementById('edit-profile-btn');
    
    // Show reservation modal
    viewDetailsButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const reservationId = button.getAttribute('data-reservation-id');
            // Fetch reservation details via AJAX
            fetch(`/api/reservation/${reservationId}/details`)
                .then(response => response.json())
                .then(data => {
                    reservationDetails.innerHTML = `
                        <p><strong>Date :</strong> ${data.date}</p>
                        <p><strong>Heure :</strong> ${data.time}</p>
                        <p><strong>Statut :</strong> ${data.status}</p>
                    `;
                    reservationModal.style.display = 'block';
                });
        });
    });
    
    // Show edit profile modal
    if (editProfileButton) {
        editProfileButton.addEventListener('click', () => {
            editProfileModal.style.display = 'block';
        });
    }

    // Close modals
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            button.closest('.modal').style.display = 'none';
        });
    });
    
    window.addEventListener('click', (event) => {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    });
});
