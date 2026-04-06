
// static/script.js

// Register Form Validation
document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            const username = document.getElementById('username').value;
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const phone = document.getElementById('phone').value;

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const phoneRegex = /^\d{10}$/;
            const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

            if (username.length < 3) {
                e.preventDefault();
                alert('Username must be at least 3 characters long.');
                return;
            }

            if (name.length < 2) {
                e.preventDefault();
                alert('Full name must be at least 2 characters long.');
                return;
            }

            if (!emailRegex.test(email)) {
                e.preventDefault();
                alert('Please enter a valid email address.');
                return;
            }

            if (!passwordRegex.test(password)) {
                e.preventDefault();
                alert('Password must be at least 8 characters long and contain at least one letter and one number.');
                return;
            }

            if (!phoneRegex.test(phone)) {
                e.preventDefault();
                alert('Please enter a valid 10-digit phone number.');
                return;
            }
        });
    }

    // Login Form Validation
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!emailRegex.test(email)) {
                e.preventDefault();
                alert('Please enter a valid email address.');
                return;
            }

            if (password.length < 8) {
                e.preventDefault();
                alert('Password must be at least 8 characters long.');
                return;
            }
        });
    }

    // Upload Form Validation
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function (e) {
            const fileInput = document.getElementById('file');
            const file = fileInput.files[0];

            if (!file) {
                e.preventDefault();
                alert('Please select a CSV file to upload.');
                return;
            }

            if (!file.name.endsWith('.csv')) {
                e.preventDefault();
                alert('Only CSV files are allowed.');
                return;
            }
        });
    }

    // Predict Form Validation
    const predictForm = document.getElementById('predictForm');
    if (predictForm) {
        predictForm.addEventListener('submit', function (e) {
            const inputs = predictForm.querySelectorAll('input[type="number"]');
            let valid = true;

            inputs.forEach(input => {
                const value = input.value.trim();
                if (value === '' || isNaN(value)) {
                    valid = false;
                    alert(`Please enter a valid number for ${input.name}.`);
                    input.focus();
                }
            });

            if (!valid) {
                e.preventDefault();
            }
        });
    }

    // Navbar Animation on Scroll
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // Smooth Scroll for Navigation Links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            window.location.href = href; // Follow Flask routing
        });
    });
});
