document.addEventListener("DOMContentLoaded", function() {
    const motorcycleAnimation = document.querySelector(".motorcycle-animation");
    const motorcycle = motorcycleAnimation.querySelector(".motorcycle");
    const containerWidth = motorcycleAnimation.clientWidth;
    const cookingAnimation = document.querySelector(".cooking-animation");
    const fire = cookingAnimation.querySelector(".fire");
    const skillet = cookingAnimation.querySelector(".skillet");
    let angle = 0;

    const barrierWidthPadding = 0.03; // 3% padding
    const barrierHeightPadding = 0.05; // 5% padding
    const imageWidth = fire.clientWidth; // Assuming both images have the same width
    const imageHeight = fire.clientHeight; // Assuming both images have the same height

    function animateCooking() {
        const xOffset = Math.cos(angle) * 100;
        const yOffset = Math.sin(angle) * 40;

        const maxXOffset = (cookingAnimation.clientWidth / 2) - (1 + barrierWidthPadding) * imageWidth;
        const maxYOffset = (cookingAnimation.clientHeight / 2) - (1 + barrierHeightPadding) * imageHeight;

        const clampedXOffset = Math.max(-maxXOffset, Math.min(xOffset, maxXOffset));
        const clampedYOffset = Math.max(-maxYOffset, Math.min(yOffset, maxYOffset));

        fire.style.transform = `translate(${clampedXOffset}px, ${clampedYOffset}px)`;
        skillet.style.transform = `translate(${-clampedXOffset}px, ${-clampedYOffset}px)`;

        angle += 0.05; // Increment angle for next frame

        requestAnimationFrame(animateCooking);
    }


    function animateMotorcycle() {
        motorcycle.style.left = containerWidth + "px";
        setTimeout(() => {
            motorcycle.style.left = "-100px";
        }, 5000); // 5 seconds for one cycle
    }
    
    animateMotorcycle();
    animateCooking();

    setInterval(() => {
        animateMotorcycle();
    }, 10000); // Loop every 10 seconds (twice the animation cycle time)

    
});
