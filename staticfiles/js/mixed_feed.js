const feedItems = document.querySelectorAll('.feed-item');
const modal = document.getElementById('fullscreenModal');
const modalContent = modal.querySelector('.fullscreen-content');
const closeFull = document.getElementById('closeFull');

let currentIndex = 0;

feedItems.forEach((item, index) => {
    item.addEventListener('click', () => {
        currentIndex = index;
        openFullscreen(currentIndex);
    });
});

function openFullscreen(index){
    const post = feedItems[index];
    const clone = post.querySelector('video, img').cloneNode(true);
    clone.autoplay = true;
    clone.muted = true;
    modalContent.innerHTML = '';
    modalContent.appendChild(clone);
    modal.style.display = 'block';
}

closeFull.addEventListener('click', () => {
    modal.style.display = 'none';
});

window.addEventListener('wheel', e => {
    if(modal.style.display === 'block'){
        if(e.deltaY > 0){
            currentIndex = Math.min(currentIndex+1, feedItems.length-1);
        } else {
            currentIndex = Math.max(currentIndex-1, 0);
        }
        openFullscreen(currentIndex);
    }
});

let startY = 0;
window.addEventListener('touchstart', e => { startY = e.touches[0].clientY; });
window.addEventListener('touchend', e => {
    if(modal.style.display==='block'){
        let endY = e.changedTouches[0].clientY;
        if(startY - endY > 50){ currentIndex = Math.min(currentIndex+1, feedItems.length-1); openFullscreen(currentIndex); }
        else if(endY - startY > 50){ currentIndex = Math.max(currentIndex-1, 0); openFullscreen(currentIndex); }
    }
});

document.addEventListener('click', e => {
    if(e.target.classList.contains('like-btn')){
        const id = e.target.dataset.id;
        fetch(`/like/${id}/`, {
            method:'POST',
            headers:{'X-CSRFToken': getCookie('csrftoken')}
        })
        .then(res => res.json())
        .then(data => {
            if(data.status==='liked'){ e.target.textContent='Unlike'; }
            else{ e.target.textContent='❤️ Like'; }
        });
    }
});

function getCookie(name) {
    let cookieValue = null;
    if(document.cookie && document.cookie !== ''){
        const cookies = document.cookie.split(';');
        for(let i=0;i<cookies.length;i++){
            const cookie = cookies[i].trim();
            if(cookie.substring(0,name.length+1) === (name+'=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length+1));
                break;
            }
        }
    }
    return cookieValue;
}
