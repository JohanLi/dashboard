const subreddits = document.querySelector('.subreddits');

if (subreddits) {
    subreddits.addEventListener('click', (event) => {
        const { target } = event;

        if (!target.classList.contains('subreddit')) {
            return;
        }

        document.querySelector(`.subreddits .active`).classList.remove('active');
        target.classList.add('active');

        const subreddit = target.innerText;
        const posts = document.querySelector(`.reddit-posts [data-subreddit="${subreddit}"]`);

        posts.parentNode.prepend(posts);
    });
}
