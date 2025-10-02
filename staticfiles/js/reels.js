// ===========================
// Reels Autoplay + Scroll + Keyboard
// ===========================
document.addEventListener("DOMContentLoaded", () => {
  const reels = document.querySelectorAll(".reel-video");
  const container = document.querySelector(".reels-container");

  // Intersection Observer for autoplay/pause
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.play();
      } else {
        entry.target.pause();
      }
    });
  }, { threshold: 0.8 });

  reels.forEach(video => {
    observer.observe(video);
  });

  // Keyboard Arrow Navigation
  document.addEventListener("keydown", (e) => {
    const currentScroll = container.scrollTop;
    const viewportHeight = window.innerHeight;

    if (e.key === "ArrowDown") {
      container.scrollTo({ top: currentScroll + viewportHeight, behavior: 'smooth' });
    } else if (e.key === "ArrowUp") {
      container.scrollTo({ top: currentScroll - viewportHeight, behavior: 'smooth' });
    }
  });
});
