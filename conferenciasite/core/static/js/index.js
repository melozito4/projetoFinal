document.addEventListener("DOMContentLoaded", function () {
  // Redes sociais
  const instagramIcon = document.getElementById("instagram-icon");
  if (instagramIcon) {
    instagramIcon.addEventListener("click", function () {
      window.open("https://www.instagram.com/enauticaa/", "_blank");
    });
  }

  const youtubeIcon = document.getElementById("youtube-icon");
  if (youtubeIcon) {
    youtubeIcon.addEventListener("click", function () {
      window.open("https://www.youtube.com/watch?v=NU9L8hacRak&ab_channel=OeirasValley", "_blank");
    });
  }

  const facebookIcon = document.getElementById("facebook-icon");
  if (facebookIcon) {
    facebookIcon.addEventListener("click", function () {
      window.open("https://www.facebook.com/enautica/?locale=pt_PT", "_blank");
    });
  }

  // Imagens clicáveis
  const supplyImage = document.getElementById('clickable-image');
  if (supplyImage) {
    supplyImage.addEventListener('click', function () {
      window.open('https://www.supplychainmagazine.pt/', '_blank');
    });
  }

  const enidhImage = document.getElementById('clickable-image-enidh');
  if (enidhImage) {
    enidhImage.addEventListener('click', function () {
      window.open('https://www.enautica.pt/', '_blank');
    });
  }

  const oeirasImage = document.getElementById('clickable-image-oeirasvalley');
  if (oeirasImage) {
    oeirasImage.addEventListener('click', function () {
      window.open('https://oeirasvalley.com/', '_blank');
    });
  }

  // Menu dropdown do utilizador
  const menu = document.getElementById('userDropdown');
  const icon = document.querySelector('.user-icon');

  if (icon && menu) {
    icon.addEventListener('click', function (event) {
      event.stopPropagation(); // Evita que feche logo
      menu.classList.toggle('show');
    });

    window.addEventListener('click', function (e) {
      if (!menu.contains(e.target) && !icon.contains(e.target)) {
        menu.classList.remove('show');
      }
    });
  }

});
