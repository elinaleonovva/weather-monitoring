// ������� ��� �������� �������
async function loadHistory() {
    try {
        // ������ �������
        const historyResponse = await fetch(`/history`);
        const historyData = await historyResponse.json();

        // ����������� �������
        const historyList = document.getElementById('history-list');
        historyList.innerHTML = '';
        historyData.forEach((entry) => {
            const li = document.createElement('li');
            li.textContent = `${entry.city} ${entry.temperature}°C (${entry.condition})`;
            historyList.appendChild(li);
        });
    } catch (error) {
        console.error("Failed to load history:", error);
    }
}

// ���������� �����
document.getElementById('weather-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const city = document.getElementById('city').value;

    try {
        // ������ ������
        const weatherResponse = await fetch(`/weather?city=${city}`);
        const weatherData = await weatherResponse.json();

        // ����������� ������
        document.getElementById('weather-info').innerHTML = `
            <h2>Weather in ${city}</h2>
            <p>Temperature: ${weatherData.temperature}°C</p>
            <p>Condition: ${weatherData.condition}</p>
        `;

        // ���������� �������
        await loadHistory();
    } catch (error) {
        document.getElementById('weather-info').innerHTML = `
            <p style="color: red;">Failed to fetch weather data. Please try again.</p>
        `;
    }
});

// �������� ������� ��� �������� ��������
document.addEventListener('DOMContentLoaded', loadHistory);
