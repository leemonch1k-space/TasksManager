document.addEventListener('click', function (event) {
    const target = event.target.closest('.hide_on_click');

    if (target) {
        const block = target.closest('.toggle-block');

        if (block) {
            target.classList.add('d-none');

            const hiddenField = block.querySelector('.open_after_click');
            if (hiddenField) {
                hiddenField.classList.remove('d-none');
            }

            block.classList.remove('border');

        }
    }
});
