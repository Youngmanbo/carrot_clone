// function previewImage(event) {
//   let reader = new FileReader();
//   reader.onload = function () {
//     let output = document.getElementById("imagePreview");
//     output.src = reader.result;
//     output.classList.add("img-upload-fit");
//   };
//   reader.readAsDataURL(event.target.files[0]);
// }

function previewImage(event) {
  let cnt = 0;
  const length = document.querySelectorAll('.image-item').length;
  if (length) {
    for (i = 0; i < length; i++) {
      document.querySelectorAll(".image-item")[i].remove();
      document.querySelector(".controls").children[i].remove();
    }
    cnt = 0;
  }

  for(let image of event.target.files) {
    let reader = new FileReader();
    
    reader.onload = function () {
      // image
      let imglist = document.createElement("li");
      imglist.setAttribute('class', 'image-item');
      cnt += 1;
      imglist.setAttribute('id', 'slider' + cnt);
      let img = document.createElement("img");
      img.setAttribute('src', reader.result);
      img.setAttribute('class', 'img-upload-fit');
      imglist.appendChild(img);
      document.querySelector(".image-list").appendChild(imglist);

      // radio
      let radio = document.createElement("input");
      radio.setAttribute('type', 'radio');
      radio.setAttribute('name', 'slider');
      
      if (length) {
        radio.setAttribute('id', 'radio' + (cnt+length));
      } else {
        if (cnt == 1) {
          radio.setAttribute('id', 'radio' + cnt);
          radio.setAttribute('checked', 'checked');
        } else {
          radio.setAttribute('id', 'radio' + cnt);
        };
      };
      document.querySelector(".controls").appendChild(radio);
    };
    reader.readAsDataURL(image);
  }
}

function slide () {
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
};