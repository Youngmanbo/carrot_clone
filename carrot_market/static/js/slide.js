document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('.image-item');
    const radioButtons = document.querySelectorAll('input[type="radio"]');

    radioButtons.forEach((radio, index) => {
      radio.addEventListener('change', function () {
        hideAllSlides();
        slides[index].style.display = 'block';
      });
    });

    function hideAllSlides() {
      slides.forEach(slide => {
        slide.style.display = 'none';
      });
    }
    radioButtons[0].checked = true;
  });