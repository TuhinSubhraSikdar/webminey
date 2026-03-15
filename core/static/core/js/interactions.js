const cards = document.querySelectorAll('.tool-card');

cards.forEach(card => {
    card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        card.style.transform =
            `rotateX(${-(y - rect.height/2)/20}deg)
             rotateY(${(x - rect.width/2)/20}deg)
             scale(1.02)`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'rotateX(0) rotateY(0)';
    });
});