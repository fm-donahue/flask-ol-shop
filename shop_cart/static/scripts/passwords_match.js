let passwordInput = document.querySelector("input[id='password']");
let confirmPasswordInput = document.querySelector("input[id='confirm_password']");
let passwordLength;

passwordInput.onkeyup = function() {
    let passwordPattern = /^(?=.+[a-zA-Z])(?=.+[\d])([a-zA-z\d]){8,16}$/g;
    passwordLength = passwordInput.value.length;
    if (passwordLength >= 8 && passwordLength <= 16 && passwordInput.value.match(passwordPattern)) {
        this.classList.remove("is-invalid");
        this.classList.add("is-valid");
    } else {
        this.classList.add("is-invalid");
    }
};

confirmPasswordInput.onkeyup = function() {
    let confirmPasswordLength = this.value.length;
    passwordLength = passwordInput.value.length;
    if (passwordInput.value.includes(this.value, 0)) {
        this.classList.remove("is-invalid");
        if (passwordLength == confirmPasswordLength) {
            this.classList.add("is-valid");
        } else {
            this.classList.remove("is-valid");
        }
    } else {
        this.classList.remove("is-valid");
        this.classList.add("is-invalid");
    }
};