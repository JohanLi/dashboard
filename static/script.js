const subreddits = document.querySelector('.subreddits');

if (subreddits) {
    subreddits.addEventListener('click', (event) => {
        document.querySelector(`.subreddits .active`).classList.remove('active');
        event.target.classList.add('active');

        const subreddit = event.target.innerText;
        const posts = document.querySelector(`.reddit-posts [data-subreddit="${subreddit}"]`);

        posts.parentNode.prepend(posts);
    });
}
