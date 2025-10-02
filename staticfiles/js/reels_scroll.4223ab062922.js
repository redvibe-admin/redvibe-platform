// reels_scroll.js — handles scroll-based autoplay/pause + tap play/pause + sound toggle
document.addEventListener("DOMContentLoaded", () => {
  const reels = Array.from(document.querySelectorAll(".reel"));
  if (reels.length === 0) return;

  // IntersectionObserver: play most visible reel, pause others
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const reel = entry.target;
      const video = reel.querySelector("video");
      const postId = reel.dataset.postId;

      if (entry.isIntersecting && entry.intersectionRatio >= 0.6) {
        // Pause other videos
        reels.forEach(r => {
          const v = r.querySelector("video");
          if (v !== video) {
            v.pause();
          }
        });

        // Play current video
        video.muted = false;
        const playPromise = video.play();
        if (playPromise !== undefined) {
          playPromise.catch(() => { video.muted = true; video.play().catch(()=>{}); });
        }

        // Schedule mark-watched
        scheduleMarkWatched(reel);

      } else {
        // Not visible enough -> pause
        video.pause();
      }
    });
  }, { threshold: [0.25, 0.5, 0.6] });

  // Observe all reels
  reels.forEach(r => io.observe(r));

  // Tap to play/pause
  reels.forEach(reel => {
    const video = reel.querySelector("video");

    video.addEventListener("click", () => {
      if (video.paused) video.play().catch(()=>{});
      else video.pause();
    });

    // Sound toggle
    const sbtn = reel.querySelector(".sound-toggle");
    if (sbtn) {
      sbtn.addEventListener("click", () => {
        video.muted = !video.muted;
        sbtn.textContent = video.muted ? "🔇" : "🔊";
      });
    }
  });

  // mark-watched timers
  const watchedTimers = {};
  function scheduleMarkWatched(reelEl) {
    const postId = reelEl.dataset.postId;
    if (!postId) return;
    if (watchedTimers[postId]) { clearTimeout(watchedTimers[postId]); delete watchedTimers[postId]; }

    watchedTimers[postId] = setTimeout(() => {
      sendMarkWatched(postId);
      delete watchedTimers[postId];
    }, 5000);

    const videoEl = reelEl.querySelector("video");
    const endedHandler = function() {
      sendMarkWatched(postId);
      videoEl.removeEventListener('ended', endedHandler);
      if (watchedTimers[postId]) { clearTimeout(watchedTimers[postId]); delete watchedTimers[postId]; }
    };
    videoEl.addEventListener('ended', endedHandler);
  }

  function sendMarkWatched(postId) {
    fetch("/mark-watched/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": window.CSRF_TOKEN || ""
      },
      body: JSON.stringify({ post_id: Number(postId) })
    }).then(()=>{}).catch(()=>{});
  }
});
