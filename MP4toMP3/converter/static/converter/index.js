document.addEventListener('DOMContentLoaded', function() {
    function getCSRFToken() {
        return window.CSRF_TOKEN;
    }
    let currentAudio = null;
    let currentAudioId = null;

    if (document.querySelector('#convert-form')) {
        document.querySelector('#convert-form').addEventListener('submit', function (event) {
            event.preventDefault();

            document.querySelector('#spinner').style.display = 'block';
            document.querySelector('#convert-btn').style.display = 'none';

            const form = new FormData(this);
            fetch('/convert', {
                method: 'POST',
                body: form,
                headers: {
                    'X-CSRFToken': window.CSRF_TOKEN
                }
            })
            .then(response => {
                const contentType = response.headers.get('Content-Type');

                if (contentType && contentType.includes('application/json')) {
                    return response.json();
                }
                else {
                    window.location.href = response.url;
                }
            })
            .then(data => {
                document.querySelector('#spinner').style.display = 'none';
                document.querySelector('#convert-btn').style.display = 'block';

                if (auth != "True") {
                    if (data.mp3_file_url) {
                        const link = document.createElement('a');
                        link.href = data.mp3_file_url;
                        link.download = data.mp3_file_url.split('/').pop();

                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);

                        const fileSizeMB = data.file_size / (1024 * 1024);
                        const estimatedDownloadTime = fileSizeMB * 1000;

                        setTimeout(() => {
                            fetch('/delete_file', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': window.CSRF_TOKEN
                                },
                                body: JSON.stringify({ "mp3_file_url": data.mp3_file_url })
                            })
                            .then(response => {
                                const contentType = response.headers.get('Content-Type');

                                if (contentType && contentType.includes('application/json')) {
                                    return response.json();
                                }
                                else {
                                    window.location.href = response.url;
                                }
                            })
                            .then(result => {
                                if (result.message) {
                                    console.log(result.message);
                                }
                                else {
                                    console.error(result.error);
                                }
                            })
                            .catch(error => {
                                console.error('Error during file deletion:', error);
                            });
                        }, estimatedDownloadTime);
                    }
                    else {
                        alert('Error during conversion.');
                    }
                }
                else {
                    window.location.href = response.url;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.querySelector('#spinner').style.display = 'none';
                document.querySelector('#convert-btn').style.display = 'block';
                alert('An error occured.');
            });
        });
    }
    

    if (document.querySelector('.download-btn')) {
        document.querySelectorAll('.download-btn').forEach(button => {
            button.addEventListener('click', function(event) {
                
                const file_path = this.dataset.mp3Url;

                const link = document.createElement('a');
                link.href = file_path;
                link.download = file_path.split('/').pop();

                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
            })
        })
    }

    if (document.querySelector('.play-pause-btn')){
        document.querySelectorAll('.play-pause-btn').forEach(button => {
            const audioId = button.id.split('-')[2];
            const audio = document.getElementById(`audio-${audioId}`)
            const progressBar = document.getElementById(`progress-bar-${audioId}`)
            progressBar.value = 0;
            const currentTimeSpan = document.getElementById(`current-time-${audioId}`)
            const totalTimeSpan = document.getElementById(`total-time-${audioId}`)

            function formatTime(seconds) {
                const mins = Math.floor(seconds / 60);
                const secs = Math.floor(seconds % 60);
                return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
            }

            audio.addEventListener('loadedmetadata', () => {
                totalTimeSpan.textContent = formatTime(audio.duration);
            });

            button.addEventListener('click', () => {
                if (currentAudio && currentAudio !== audio) {
                    currentAudio.pause();
                    currentAudio.currentTime = 0;
                    const oldButton = document.getElementById(`play-pause-${currentAudioId}`);
                    oldButton.style.borderTop = "15px solid transparent";
                    oldButton.style.borderBottom = "15px solid transparent";
                    oldButton.style.borderLeft = "20px solid rgb(0, 40, 160)";
                    oldButton.style.borderRight = "transparent";
                    oldButton.style.height = "0px";

                }
                if (audio.paused) {
                    audio.play();
                    currentAudio = audio;
                    currentAudioId = audioId;

                    button.style.borderTop = "transparent";
                    button.style.borderBottom = "transparent";
                    button.style.borderLeft = "10px solid rgb(0, 40, 160)";
                    button.style.borderRight = "10px solid rgb(0, 40, 160)";
                    button.style.height = "32px";
                    button.style.width = "30px";
                }
                else {
                    audio.pause();
                    currentAudio = null;
                    currentAudioId = null;
                    button.style.borderTop = "15px solid transparent";
                    button.style.borderBottom = "15px solid transparent";
                    button.style.borderLeft = "20px solid rgb(0, 40, 160)";
                    button.style.borderRight = "transparent";
                    button.style.height = "0px";
                }
            });

            audio.addEventListener('timeupdate', () => {
                const progress = (audio.currentTime / audio.duration) * 100;
                progressBar.value = progress;
                currentTimeSpan.textContent = formatTime(audio.currentTime);
            });

            progressBar.addEventListener('input', () => {
                const seekTime = (progressBar.value / 100) * audio.duration;
                audio.currentTime = seekTime;
            });
        });
    }
})