// Alusta aika tulosteesta
const clockElem = document.getElementById("clock");
const startTime = new Date(clockElem.textContent.trim());
const pageLoadTime = Date.now();

// Päivitä kello sekunnin välein
function updateClock() {
    const now = new Date(startTime.getTime() + (Date.now() - pageLoadTime));

    // Muodosta aikamuoto DD.MM.YYYY klo HH:MM:SS
    const dd = String(now.getDate()).padStart(2, '0');
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const yyyy = now.getFullYear();
    const hh = String(now.getHours()).padStart(2, '0');
    const mi = String(now.getMinutes()).padStart(2, '0');
    const ss = String(now.getSeconds()).padStart(2, '0');

    const formatted = `${dd}.${mm}.${yyyy} klo ${hh}:${mi}:${ss}`;
    clockElem.textContent = formatted;
}

setInterval(updateClock, 1000);
updateClock(); // päivitä heti sivun latautuessa