const validate = (e) => {

    e.preventDefault();

    const form = document.getElementById('form');
    const name = document.getElementById('name');
    const email = document.getElementById('email');
    const password = document.getElementById('passwd');
    const confPasswd = document.getElementById('confPasswd');
    const terms = document.getElementById('terms');

    if (email.value === '') {
        alert('Email is required');
        e.preventDefault();
        return;
    }

    if (password.value === '') {
        alert('Password is required');
        e.preventDefault();
        return;
    }

    if (confPasswd.value === '') {
        alert('Confirm Password is required');
        e.preventDefault();
        return;
    }

    if (password.value !== confPasswd.value) {
        alert('Passwords do not match');
        e.preventDefault();
        return;
    }

    if (!terms.checked) {
        alert('Please accept terms and conditions');
        e.preventDefault();
        return;
    }

    const emailRE = /^[a-zA-Z0-9]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,3}$/;
    const nameRE = /^[a-zA-z ]+[^ ]$/;
    const passRE = /^(?=.*[A-Z])(?=.*\d).{9,}$/

    if (!emailRE.test(email.value)) {
        alert('Email is invalid');
        e.preventDefault();
        return;
    }

    if(!nameRE.test(name.value)){
        alert('Name is invalid');
        e.preventDefault();
        return;
    }

    if(!passRE.test(password.value)){
        alert('Password is invalid');
        e.preventDefault();
        return;
    }

};

document.getElementById('submitBut').addEventListener('click', validate);