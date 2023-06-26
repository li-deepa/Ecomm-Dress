function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


console.log("hello")

let btns=document.getElementsByClassName("product-container")


for (i = 0; i < btns.length; i++) {
    btns[i].addEventListener('click', function () {
        var product_id = this.dataset.product
        var action = this.dataset.action
        var user=this.dataset.user
        console.log('product_id:', product_id, 'action:', action)
        console.log('USER:', user)

        if (user != 'AnonymousUser') {
            addToCart(product_id, action)
        }
        else {
            console.log('User is not logged in,sending data ..')
        }


    })
}

function addToCart(product_id, action) {
    console.log('User is logged in,sending data ..')
    var url = '/add_tocart'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'id': product_id, 'action': action })
    })
        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
        .then(res=>res.json())
    .then(data=>{
        document.getElementById("counter").innerHTML=data
        console.log(data)
    })
    .catch(error=>{
        console.log(error)
    })
    }


