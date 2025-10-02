document.addEventListener("DOMContentLoaded", () => {
  const videos = document.querySelectorAll(".feed-video");

  videos.forEach(video => {
    video.addEventListener("click", () => {
      if(video.paused) video.play();
      else video.pause();
    });
  });
});
