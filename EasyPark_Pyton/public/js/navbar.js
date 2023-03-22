window.addEventListener("scroll", function() {
    var navbar = document.querySelector(".navbar");
    var scrolled = window.pageYOffset || document.documentElement.scrollTop;
    if (scrolled > 50) { /* Cambia "100" a la cantidad de píxeles que desees antes de cambiar el color de fondo */
      navbar.classList.remove("initial-color");
      navbar.classList.add("new-color"); /* Cambia "new-color" a la clase que tenga el color de fondo que desees */
    } else {
      navbar.classList.add("initial-color");
      navbar.classList.remove("new-color");
    }
  });