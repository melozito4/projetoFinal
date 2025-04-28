document.addEventListener("DOMContentLoaded", function () {
  const instagramIcon = document.getElementById("instagram-icon");
  if (instagramIcon) {
    instagramIcon.addEventListener("click", function () {
      window.open("https://www.instagram.com/conference_site/", "_blank");
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const youtubeIcon = document.getElementById("youtube-icon");
  if (youtubeIcon) {
    youtubeIcon.addEventListener("click", function () {
      window.open("https://www.youtube.com/watch?v=NU9L8hacRak&ab_channel=OeirasValley", "_blank");
    });
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const clickableImage = document.getElementById('clickable-image');

  if (clickableImage) {
    clickableImage.addEventListener('click', function () {
      window.open('https://www.supplychainmagazine.pt/', '_blank');
    });
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const clickableImage = document.getElementById('clickable-image-enidh');

  if (clickableImage) {
    clickableImage.addEventListener('click', function () {
      window.open('https://www.enautica.pt/', '_blank');
    });
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const clickableImage = document.getElementById('clickable-image-oeirasvalley');

  if (clickableImage) {
    clickableImage.addEventListener('click', function () {
      window.open('https://oeirasvalley.com/', '_blank');
    });
  }
});

