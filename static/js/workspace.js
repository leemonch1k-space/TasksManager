function showCreateForm() {
    const emptyState = document.getElementById('empty-state');
    const formContainer = document.getElementById('create-form-container');

    if (emptyState && formContainer) {
        emptyState.classList.add('d-none');
        formContainer.classList.remove('d-none');
    }
}

function hideCreateForm() {
    const emptyState = document.getElementById('empty-state');
    const formContainer = document.getElementById('create-form-container');

    if (emptyState && formContainer) {
        emptyState.classList.remove('d-none');
        formContainer.classList.add('d-none');
    }
}
