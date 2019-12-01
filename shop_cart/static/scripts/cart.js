function getPhpRate(){
    time = new Date()
    if (time.getMinutes() == 0) {
        // load('php_rate');
        $('#php_rate').load(' #php_rate');
        for(let i = 1; i <= numberOfItems; i++) {
            updateSection(i);
        }
    }
};
setInterval(getPhpRate, 60000);

function updateItems(number) {
    let tagList = document.querySelectorAll(`div[name='${number}']`);
    let updateQuantity = tagList[0].children.namedItem("quantity").value;
    let updateOrderDetails = tagList[1].children.namedItem("order_details").value;
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            updateSection(number);
        }
    };
    xhttp.open("POST", "/async_update/" + number, true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify({quantity: `${updateQuantity}`, order_details: `${updateOrderDetails}`}));
};

function updateSection(number) {
    $(`#cart_total_price${number}`).load(` #cart_total_price${number}`);
    $(`#order_total_price${number}`).load(` #order_total_price${number}`);
    // load(`cart_total_price${number}`);
    // load(`order_total_price${number}`);
};

// function load(id) {
//     let load_xhttp = new XMLHttpRequest();
//     load_xhttp.onload = function() {
//         document.getElementById(id).innerHTML = this.responseText;
//     };
//     load_xhttp.open("GET", "/cart", true);
//     load_xhttp.send();
// };