let emailInput = document.querySelector("input[id='email']");

emailInput.onkeyup = function() {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        let response = xhttp.response;
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            let emailDiv = document.getElementById("feedback_email");
            if (response != 'null') {
                if (response == 'true') {
                    emailDiv.setAttribute("class", "valid-feedback");
                    emailDiv.innerHTML = "Email is available.";
                } else if (response == 'false') { 
                    emailDiv.setAttribute("class", "invalid-feedback");
                    emailDiv.innerHTML = "Email is taken. Please use different one.";
                }
                emailDiv.style.display = 'block';
                emailDiv.previousElementSibling.classList.remove("is-invalid");
            }
            else {
                emailDiv.style.display = 'none';
            }
        }
    };
    xhttp.open("GET", "/check_email?email=" + this.value, true);
    xhttp.send()
};

$("#password").tooltip({placement: "right", trigger:"focus", title: "Must have 8-16 characters with at least 1 number."})
