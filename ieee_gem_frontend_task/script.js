let allVideos = [];

window.onload = function() {
    fetchVideos();
};

function fetchVideos() {
    fetch('https://ypapi.formz.in/api/public/videos')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        allVideos = data.videos;
        displayVideos(allVideos);
    })
    .catch(error => {
        console.error('Error fetching videos:', error);
    });
}

function displayVideos(videos) {
    const videosContainer = document.getElementById('videos-container');
    videosContainer.innerHTML = '';

    videos.forEach(video => {
        const videoCard = document.createElement('div');
        videoCard.className = 'col-md-4 video-card';
        videoCard.innerHTML = `
            <div class="card">
                <img src="${video.thumbnail}" class="card-img-top" alt="${video.title}">
                <div class="card-body">
                    <h5 class="card-title">${video.title}</h5>
                    <p class="card-text">${video.description}</p>
                </div>
            </div>
        `;
        videosContainer.appendChild(videoCard);
    });
}

function filterVideos(category) {
    let filteredVideos = allVideos;

    if (category !== 'All') {
        filteredVideos = allVideos.filter(video => video.category === category);
    }

    displayVideos(filteredVideos);
}

document.getElementById('search-input').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const filteredVideos = allVideos.filter(video => video.title.toLowerCase().includes(searchTerm));
    displayVideos(filteredVideos);
});
