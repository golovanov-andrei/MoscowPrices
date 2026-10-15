async function populateMetro() {
    const select = document.getElementById('metro');
    const error = document.getElementById('formError');
    try {
        const response = await fetch('/stations');
        if (!response.ok) throw new Error('Не удалось загрузить станции метро.');
        const stations = await response.json();
        select.replaceChildren();
        stations.forEach(station => {
            const option = document.createElement('option');
            option.value = station;
            option.textContent = station;
            select.appendChild(option);
        });
        select.disabled = false;
    } catch (exception) {
        error.textContent = 'Не удалось загрузить станции метро. Обновите страницу.';
        error.hidden = false;
    }
}
populateMetro();
