document.addEventListener('DOMContentLoaded', function() {
    const tweetTextarea = document.querySelector('.tweet-form textarea');
    
    if (tweetTextarea) {
        tweetTextarea.addEventListener('input', function() {
            console.log('Tweet length:', this.value.length);
        });
    }
});
