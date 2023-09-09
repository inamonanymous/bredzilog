function toggle(inputId, btnId, hiddenInputId) {
    const input = document.getElementById(inputId);
    const btn = document.getElementById(btnId);
    const hiddenInput = document.getElementById(hiddenInputId);

    if (input && btn && hiddenInput) {
        if (hiddenInput.value === "0") {
            input.removeAttribute('readonly');
            btn.removeAttribute('disabled');
            hiddenInput.value = "4096";
        } else {
            input.setAttribute('readonly', 'readonly');
            btn.setAttribute('disabled', 'disabled');
            hiddenInput.value = "0";
        }
    }
}
