const form = document.getElementById('apartmentForm');
form.addEventListener('submit', async event => {
    event.preventDefault();
    const button = document.getElementById('predictButton');
    const error = document.getElementById('formError');
    error.hidden = true;
    button.disabled = true;
    button.textContent = 'Рассчитываем…';
    const data = Object.fromEntries(['area', 'rooms', 'floor', 'minutes', 'metro'].map(
        name => [name, document.getElementById(name).value]
    ));
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Не удалось рассчитать стоимость.');
        document.getElementById('predictionResult').textContent =
            'Примерная цена: ' + Math.round(result.prediction).toLocaleString('ru-RU') + ' ₽';
        document.getElementById('predictionDetails').textContent =
            data.area + ' м² · ' + data.rooms + ' комн. · ' + data.floor +
            ' этаж · ' + data.minutes + ' мин до метро · ' + data.metro;
        activateTab('predictions');
    } catch (exception) {
        error.textContent = exception.message || 'Сервис недоступен. Попробуйте позже.';
        error.hidden = false;
    } finally {
        button.disabled = false;
        button.textContent = 'Предсказать цену';
    }
});
