document.addEventListener('DOMContentLoaded', () => {
    const userSelect = document.getElementById('userSelect');
    const modelSelect = document.getElementById('modelSelect');
    const topKSelect = document.getElementById('topKSelect');
    const generateBtn = document.getElementById('generateBtn');
    const resultsBox = document.getElementById('resultsBox');
    const movieList = document.getElementById('movieList');
    const resultsTitle = document.getElementById('resultsTitle');

    generateBtn.addEventListener('click', () => {
        const userId = userSelect.value;
        const selectedModel = modelSelect.value;
        const topK = topKSelect.value;

        // Button state change while loading
        generateBtn.innerHTML = `Analyzing... ⏳`;
        generateBtn.disabled = true;

        // API Call to Flask backend
        fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                algorithm: selectedModel,
                top_k: topK
            })
        })
            .then(res => res.json())
            .then(data => {
                movieList.innerHTML = '';
                if (data.status === 'success' && data.data.length > 0) {
                    data.data.forEach(movie => {
                        const item = `
                        <div class="movie-item">
                            <span class="movie-name">${movie.name}</span>
                            <span class="movie-score">${movie.score}% Match</span>
                        </div>
                    `;
                        movieList.insertAdjacentHTML('beforeend', item);
                    });
                    resultsTitle.innerText = `Top Matches (${selectedModel})`;
                    resultsBox.style.display = 'block';
                }

                generateBtn.innerHTML = `Get Recommendations 🚀`;
                generateBtn.disabled = false;
            })
            .catch(err => {
                console.error('Error fetching predictions:', err);
                generateBtn.innerHTML = `Get Recommendations 🚀`;
                generateBtn.disabled = false;
            });
    });
});