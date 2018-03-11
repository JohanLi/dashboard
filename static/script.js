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

const plantsWaterNodeList = document.querySelectorAll('.plants-water');

if (plantsWaterNodeList) {
    plantsWaterNodeList.forEach((plantsWater) => {
        plantsWater.addEventListener('click', (event) => {
            const { target } = event;
            const lastWatered = target.parentElement.previousElementSibling;

            target.remove();
            lastWatered.textContent = 'Just now';

            fetch('/plants/water', {
                headers: {
                    'content-type': 'application/json',
                },
                method: 'PUT',
                body: JSON.stringify({
                    id: plantsWater.dataset.id,
                }),
            })
        });
    })
}
