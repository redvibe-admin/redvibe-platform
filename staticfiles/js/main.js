// main.js — handles feed autoplay/pause + tap-to-play/pause + mark-watched + unmute flow
document.addEventListener("DOMContentLoaded", () => {
  const feedVideos = Array.from(document.querySelectorAll(".feed-video"));
  if (feedVideos.length === 0) return;

  // IntersectionObserver: play most visible video, pause others
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const vid = entry.target;
      const postContainer = vid.closest(".feed-item");
      const postId = postContainer ? postContainer.dataset.postId : null;

      if (entry.isIntersecting && entry.intersectionRatio >= 0.6) {
        feedVideos.forEach(v => { if (v !== vid) v.pause(); });

        vid.muted = false;
        const playPromise = vid.play();
        if (playPromise !== undefined) {
          playPromise.then(() => { hideUnmuteButton(vid); scheduleMarkWatched(postId, vid); })
                     .catch(() => { vid.muted = true; vid.play().catch(()=>{}); showUnmuteButton(vid); scheduleMarkWatched(postId, vid); });
        } else { scheduleMarkWatched(postId, vid); }
      } else { vid.pause(); }
    });
  }, { threshold: [0.25,0.5,0.65] });

  feedVideos.forEach(v => io.observe(v));

  // Tap-to-play/pause for feed videos
  feedVideos.forEach(vid => {
    vid.addEventListener("click", () => {
      if (vid.paused) vid.play().catch(()=>{});
      else vid.pause();
    });
  });

  // Unmute button logic
  function showUnmuteButton(video) {
    const wrap = video.closest(".feed-video-wrap");
    if (!wrap) return;
    const btn = wrap.querySelector(".unmute-btn");
    if (btn) btn.style.display = "block";
    if (btn && !btn.dataset.bound) {
      btn.dataset.bound = "1";
      btn.addEventListener("click", () => { video.muted = false; video.play().catch(()=>{}); btn.style.display = "none"; });
    }
  }
  function hideUnmuteButton(video) {
    const wrap = video.closest(".feed-video-wrap");
    if (!wrap) return;
    const btn = wrap.querySelector(".unmute-btn");
    if (btn) btn.style.display = "none";
  }

  // mark-watched
  const watchedTimers = {};
  function scheduleMarkWatched(postId, videoEl) {
    if (!postId) return;
    if (watchedTimers[postId]) return;
    const t = setTimeout(() => { sendMarkWatched(postId); delete watchedTimers[postId]; }, 5000);
    watchedTimers[postId] = t;

    videoEl.addEventListener("ended", function onEnded() {
      sendMarkWatched(postId);
      videoEl.removeEventListener("ended", onEnded);
      if (watchedTimers[postId]) { clearTimeout(watchedTimers[postId]); delete watchedTimers[postId]; }
    });
  }

  function sendMarkWatched(postId) {
    if (!postId) return;
    fetch("/mark-watched/", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": window.CSRF_TOKEN || "" },
      body: JSON.stringify({ post_id: postId })
    }).then(r => r.json()).catch(()=>{});
  }
});
