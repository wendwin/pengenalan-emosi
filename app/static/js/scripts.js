const colors = ['green', 'blue', 'yellow'];
const randomColor = colors[Math.floor(Math.random() * colors.length)];
const elements = document.querySelectorAll('.randomcolor');
elements.forEach(element => {
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    element.style.color = randomColor;
});