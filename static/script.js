document.querySelector('.subreddits').addEventListener('click', (event) => {
    document.querySelector(`.subreddits .active`).classList.remove('active');
    event.target.classList.add('active');

    const subreddit = event.target.innerText;
    const posts = document.querySelector(`.posts [data-subreddit="${subreddit}"]`);

    posts.parentNode.prepend(posts);
});

document.querySelector(`.subreddits > div:first-child`).classList.add('active');
