// Custom Modal for Delete Confirmations
document.addEventListener("DOMContentLoaded", function () {
  // Create modal HTML
  const modalHTML = `
        <div id="deleteModal" class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h3>Confirm Deletion</h3>
                </div>
                <div class="modal-body">
                    <p id="modalMessage">Are you sure you want to delete this item?</p>
                    <p class="modal-warning">This action cannot be undone.</p>
                </div>
                <div class="modal-footer">
                    <button id="cancelDelete" class="btn-modal-cancel">Cancel</button>
                    <button id="confirmDelete" class="btn-modal-confirm">Delete</button>
                </div>
            </div>
        </div>
    `;

  // Add modal to body
  document.body.insertAdjacentHTML("beforeend", modalHTML);

  const modal = document.getElementById("deleteModal");
  const cancelBtn = document.getElementById("cancelDelete");
  const confirmBtn = document.getElementById("confirmDelete");
  const modalMessage = document.getElementById("modalMessage");

  let deleteUrl = "";

  // Handle all delete links
  document.addEventListener("click", function (e) {
    const deleteLink = e.target.closest(".delete-action");
    if (deleteLink) {
      e.preventDefault();
      deleteUrl = deleteLink.href;

      // Get custom message if exists
      const customMessage = deleteLink.getAttribute("data-message");
      if (customMessage) {
        modalMessage.textContent = customMessage;
      } else {
        modalMessage.textContent = "Are you sure you want to delete this item?";
      }

      // Show modal
      modal.style.display = "flex";
    }
  });

  // Cancel button
  cancelBtn.addEventListener("click", function () {
    modal.style.display = "none";
    deleteUrl = "";
  });

  // Confirm button
  confirmBtn.addEventListener("click", function () {
    if (deleteUrl) {
      window.location.href = deleteUrl;
    }
  });

  // Close on outside click
  modal.addEventListener("click", function (e) {
    if (e.target === modal) {
      modal.style.display = "none";
      deleteUrl = "";
    }
  });

  // Close on ESC key
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && modal.style.display === "flex") {
      modal.style.display = "none";
      deleteUrl = "";
    }
  });
});
