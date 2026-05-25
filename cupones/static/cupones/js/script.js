/* ========================= */
/* CONTADOR EN TIEMPO REAL */
/* ========================= */

const startDate = new Date("2025-08-01T12:15:00");

function updateCounter() {

    const now = new Date();
    const difference = now - startDate;

    // TIEMPOS
    const days = Math.floor(
        difference / (1000 * 60 * 60 * 24)
    );

    const hours = Math.floor(
        (difference / (1000 * 60 * 60)) % 24
    );

    const minutes = Math.floor(
        (difference / (1000 * 60)) % 60
    );

    const seconds = Math.floor(
        (difference / 1000) % 60
    );

    // MOSTRAR
    document.getElementById("days-counter").innerHTML =
        `
        ${days} d
        ${hours} h
        ${minutes} m
        ${seconds} s
    `;
}

// Actualizar cada segundo
setInterval(updateCounter, 1000);

// Ejecutar al iniciar
updateCounter();

/* ========================= */
/* LLUVIA DE CORAZONES */
/* ========================= */

function createHeart() {

    const heart = document.createElement("div");

    heart.classList.add("heart");

    heart.innerHTML = "💜";

    heart.style.left = Math.random() * 100 + "vw";

    heart.style.fontSize =
        Math.random() * 20 + 15 + "px";

    document.body.appendChild(heart);

    setTimeout(() => {
        heart.remove();
    }, 4000);
}

/* Corazones automáticos */
setInterval(createHeart, 700);
/* ========================= */
/* BOTONES DE CUPONES */
/* ========================= */

const buttons = document.querySelectorAll(".redeem-btn");

buttons.forEach(button => {

    // 1. Agregamos la palabra 'event' aquí adentro
    button.addEventListener("click", (event) => {

        // 2. Bloqueamos la recarga automática de la página
        event.preventDefault();

        // Preguntamos si está seguro
        const confirmacion = confirm("¿Estás seguro de que deseas canjear este cupón?");

        // Si la respuesta es "Aceptar" (true), ejecutamos el canje
        if (confirmacion) {
            button.innerText = "Ya fue canjeado 💕";
            button.style.background = "#BDBDBD";
            button.disabled = true;

            /* Explosión de corazones */
            for (let i = 0; i < 15; i++) {
                createHeart();
            }
        }

    });

});