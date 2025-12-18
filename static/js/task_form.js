document.addEventListener('DOMContentLoaded', function () {
    const wrappers = document.querySelectorAll('.expandable-wrapper');

    wrappers.forEach(wrapper => {
        const btn = wrapper.querySelector('.add-btn');
        const container = wrapper.querySelector('.field-container');

        if (btn && container) {
            btn.addEventListener('click', function () {
                btn.classList.add('d-none');
                container.classList.remove('d-none');

                const input = container.querySelector('input, textarea, select');
                if (input) input.focus();
            });
        }
    });

    const cancelBtn = document.getElementById('cancel-btn');
    const form = document.getElementById('task-form');

    if (cancelBtn && form) {
        cancelBtn.addEventListener('click', function (e) {
            e.preventDefault();
            form.style.display = 'none';
        });
    }
});
