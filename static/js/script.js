// Search functionality for services page
document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");

  if (searchInput) {
    searchInput.addEventListener("input", function (e) {
      const searchTerm = e.target.value.toLowerCase();
      const serviceCards = document.querySelectorAll(".service-card");

      serviceCards.forEach((card) => {
        const serviceName = card.dataset.service.toLowerCase();
        const serviceText = card.textContent.toLowerCase();

        if (
          serviceName.includes(searchTerm) ||
          serviceText.includes(searchTerm)
        ) {
          card.style.display = "block";
        } else {
          card.style.display = "none";
        }
      });
    });
  }

  // Auto-hide flash messages after 5 seconds
  const flashMessages = document.querySelectorAll(".alert");
  flashMessages.forEach((message) => {
    setTimeout(() => {
      message.style.transition = "opacity 0.5s";
      message.style.opacity = "0";
      setTimeout(() => message.remove(), 500);
    }, 5000);
  });
});


// Phone number validation - only allow digits
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '');
            if (this.value.length > 10) {
                this.value = this.value.slice(0, 10);
            }
        });
    });
    
    // Name validation - no numbers
    const nameInputs = document.querySelectorAll('input[name="full_name"]');
    nameInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            this.value = this.value.replace(/[0-9]/g, '');
        });
    });

// Store login status in localStorage (handled by Flask session)
function checkLoginStatus() {
  return fetch("/api/check-login")
    .then((response) => response.json())
    .then((data) => data.logged_in);
}
