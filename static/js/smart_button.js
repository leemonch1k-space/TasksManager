const SmartFormWatcher = {
    storeState: function (container) {
        const inputs = container.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            if (input.type === 'checkbox' || input.type === 'radio') {
                input.dataset.original = input.checked;
            } else {
                input.dataset.original = input.value;
            }
        });
    },

    checkChanges: function (container) {
        const buttons = container.querySelectorAll('.appear-on-change');
        const inputs = container.querySelectorAll('input, textarea, select');
        let hasChanges = false;

        inputs.forEach(input => {
            let current = (input.type === 'checkbox' || input.type === 'radio')
                ? String(input.checked)
                : input.value;

            if (current !== String(input.dataset.original)) {
                hasChanges = true;
            }
        });

        buttons.forEach(btn => {
            if (hasChanges) {
                btn.classList.remove('d-none');
            } else {
                btn.classList.add('d-none');
            }
        });
    },

    resetToOriginal: function (container) {
        const inputs = container.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            if (input.type === 'checkbox' || input.type === 'radio') {
                input.checked = (input.dataset.original === 'true');
            } else {
                input.value = input.dataset.original;
            }
            input.dispatchEvent(new Event('change', {bubbles: true}));
        });

        this.checkChanges(container);
    },

    init: function (rootElement = document) {
        const blocks = rootElement.querySelectorAll('.btn-on-change');

        blocks.forEach(container => {
            this.storeState(container);

            container.addEventListener('input', (e) => {
                if (e.target.matches('input, textarea, select')) {
                    this.checkChanges(container);
                }
            });

            const cancelBtn = container.querySelector('.btn-cancel');
            if (cancelBtn) {
                cancelBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.resetToOriginal(container);
                });
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', () => SmartFormWatcher.init());
document.addEventListener('htmx:afterSwap', (e) => SmartFormWatcher.init(e.detail.target));
