const form = document.getElementById('apartmentForm');
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        area: document.getElementById('area').value,
        rooms: document.getElementById('rooms').value,
        floor: document.getElementById('floor').value,
        minutes: document.getElementById('minutes').value,
        metro: document.getElementById('metro').value
    };

    const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    const result = await response.json();
    document.getElementById('predictionResult').innerText = `Примерная цена: ${Math.round(result.prediction).toLocaleString()} ₽`;

    // Автоматически переключаем вкладку на "Предсказания"
    document.querySelector('.tab[data-tab="predictions"]').click();
});