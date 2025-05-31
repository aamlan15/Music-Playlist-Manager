function toggleOtherGenre(select) {
    const otherInput = document.getElementById('otherGenre');
    if (select.value === 'Other') {
        otherInput.style.display = 'block';
        otherInput.required = true;
        select.removeAttribute('name');          // Avoid double name for genre
        otherInput.setAttribute('name', 'genre'); // Set name to otherGenre input
    } else {
        otherInput.style.display = 'none';
        otherInput.removeAttribute('required');
        otherInput.removeAttribute('name');       // Clear name from input
        select.setAttribute('name', 'genre');     // Restore name to select
    }
}
