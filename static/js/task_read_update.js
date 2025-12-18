document.addEventListener('DOMContentLoaded', function() {
    const fields = document.querySelectorAll('.editable-field');
    const saveBtnContainer = document.getElementById('save-btn-container');
    const originalValues = {};

    fields.forEach(field => {
        const display = field.querySelector('.display-value');
        const control = field.querySelector('.edit-control');
        const fieldName = field.getAttribute('data-field');
        const inputs = control.querySelectorAll('input, textarea, select');

        if (display && control && inputs.length > 0) {

            display.addEventListener('click', () => {
                display.classList.add('d-none');
                control.classList.remove('d-none');

                inputs.forEach(input => {
                    const key = input.id || input.name;
                    if (!(key in originalValues)) {
                        originalValues[key] = (input.type === 'checkbox') ? input.checked : input.value;
                    }
                });

                if (inputs[0]) inputs[0].focus();
            });

            inputs.forEach(input => {
                const handleChange = () => {
                    checkAllChanges();
                };
                input.addEventListener('input', handleChange);
                input.addEventListener('change', handleChange);
            });
        }
    });

    function checkAllChanges() {
        let anyChange = false;

        for (const [id, originalValue] of Object.entries(originalValues)) {
            const input = document.getElementById(id) || document.querySelector(`[name="${id}"]`);
            if (input) {
                const currentValue = (input.type === 'checkbox') ? input.checked : input.value;
                if (currentValue !== originalValue) {
                    anyChange = true;
                    break;
                }
            }
        }

        if (anyChange) {
            saveBtnContainer.classList.remove('d-none');
            saveBtnContainer.classList.add('animate-fade-in');
        } else {
            saveBtnContainer.classList.add('d-none');
        }
    }
});