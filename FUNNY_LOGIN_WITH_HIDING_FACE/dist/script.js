const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const animation1 = document.getElementById('animation1');
const animation2 = document.getElementById('animation2');
const animation3 = document.getElementById('animation3');

emailInput.addEventListener('focus', () => {
    animation1.style.display = "none";
    animation3.style.display = "block";
    animation2.style.display = "none";
});

passwordInput.addEventListener('focus', () => {
    animation1.style.display = "none";
    animation2.style.display = "block";
    animation3.style.display = "none";
});

const showAnimation1 = () => {
    animation1.style.display = "block";
    animation2.style.display = "none";
    animation3.style.display = "none";
};

emailInput.addEventListener('blur', showAnimation1);
passwordInput.addEventListener('blur', showAnimation1);