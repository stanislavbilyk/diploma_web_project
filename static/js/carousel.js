document.addEventListener("DOMContentLoaded", () => {
    const carousel = document.querySelector(".Carousel");
    const originals = [...document.querySelectorAll(".Carousel a")];

    if (originals.length === 0) return;

    const gap = 16;
    const delay = 3000;
    let currentIndex = originals.length;

    originals.forEach(slide => {
        const clone1 = slide.cloneNode(true);
        const clone2 = slide.cloneNode(true);
        carousel.appendChild(clone1);
        carousel.insertBefore(clone2, originals[0]);
    });

    let slides = document.querySelectorAll(".Carousel a");

    function getSlideWidth() {
        return slides[0].clientWidth;
    }

    function updatePosition(animate = true) {
        const slideWidth = getSlideWidth();
        const centerOffset = (document.querySelector(".CarouselContainer").clientWidth - slideWidth) / 2;
        const totalOffset = (slideWidth + gap) * currentIndex;
        carousel.style.transition = animate ? "transform 0.5s ease-in-out" : "none";
        carousel.style.transform = `translateX(${centerOffset - totalOffset}px)`;
    }

    function updateActiveClass() {
        slides.forEach(slide => slide.classList.remove("active"));
        slides[currentIndex].classList.add("active");    }


    updatePosition(false);
    updateActiveClass();

    function nextSlide() {
        currentIndex++;
        updatePosition();
        updateActiveClass();

        if (currentIndex >= slides.length - originals.length) {
            setTimeout(() => {
                carousel.style.transition = "none";
                currentIndex = originals.length;
                updatePosition(false);
                updateActiveClass();
            }, 500);
        }
    }

    setInterval(nextSlide, delay);
});
