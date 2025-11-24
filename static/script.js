document.addEventListener('DOMContentLoaded', () => {
    const startInput = document.getElementById('start-input');
    const endInput = document.getElementById('end-input');
    const startSearchBtn = document.getElementById('start-search-btn');
    const endSearchBtn = document.getElementById('end-search-btn');
    const startStatus = document.getElementById('start-status');
    const endStatus = document.getElementById('end-status');
    const calcBtn = document.getElementById('calc-btn');
    const resultArea = document.getElementById('result-area');
    const distanceValue = document.getElementById('distance-value');
    const mapLink = document.getElementById('map-link');

    let startCoords = null;
    let endCoords = null;

    async function searchLocation(query, type) {
        const statusEl = type === 'start' ? startStatus : endStatus;

        if (!query.trim()) {
            statusEl.textContent = '장소 이름을 입력해주세요.';
            statusEl.className = 'status-msg error';
            return;
        }

        statusEl.textContent = '검색 중...';
        statusEl.className = 'status-msg';

        try {
            const response = await fetch(`/api/geocode?query=${encodeURIComponent(query)}`);
            const data = await response.json();

            if (data.found) {
                statusEl.textContent = `찾음: ${data.address}`;
                statusEl.className = 'status-msg success';

                if (type === 'start') {
                    startCoords = { lat: data.lat, lon: data.lon };
                } else {
                    endCoords = { lat: data.lat, lon: data.lon };
                }
                checkReady();
            } else {
                statusEl.textContent = '위치를 찾을 수 없습니다.';
                statusEl.className = 'status-msg error';
                if (type === 'start') startCoords = null;
                else endCoords = null;
                checkReady();
            }
        } catch (error) {
            statusEl.textContent = '오류가 발생했습니다.';
            statusEl.className = 'status-msg error';
            console.error(error);
        }
    }

    function checkReady() {
        if (startCoords && endCoords) {
            calcBtn.disabled = false;
        } else {
            calcBtn.disabled = true;
            resultArea.classList.add('hidden');
        }
    }

    async function calculateDistance() {
        if (!startCoords || !endCoords) return;

        calcBtn.textContent = '계산 중...';

        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    start: startCoords,
                    end: endCoords
                })
            });

            const data = await response.json();

            distanceValue.textContent = data.distance_km;

            // Set map link
            // https://www.openstreetmap.org/directions?engine=graphhopper_car&route={start_lat}%2C{start_lon}%3B{end_lat}%2C{end_lon}
            const mapUrl = `https://www.openstreetmap.org/directions?engine=graphhopper_car&route=${startCoords.lat}%2C${startCoords.lon}%3B${endCoords.lat}%2C${endCoords.lon}`;
            mapLink.href = mapUrl;

            resultArea.classList.remove('hidden');
        } catch (error) {
            alert('거리 계산 중 오류가 발생했습니다.');
            console.error(error);
        } finally {
            calcBtn.textContent = '거리 계산하기';
        }
    }

    startSearchBtn.addEventListener('click', () => searchLocation(startInput.value, 'start'));
    endSearchBtn.addEventListener('click', () => searchLocation(endInput.value, 'end'));

    // Allow Enter key to trigger search
    startInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchLocation(startInput.value, 'start');
    });
    endInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchLocation(endInput.value, 'end');
    });

    calcBtn.addEventListener('click', calculateDistance);
});
