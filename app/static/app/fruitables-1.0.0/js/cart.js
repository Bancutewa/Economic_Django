const addToCartBtns = document.getElementsByClassName("updated-cart");

Array.from(addToCartBtns).forEach(element => {
    element.addEventListener('click', () => {
        const productId = element.dataset.product;
        const action = element.dataset.action;
        if (user === 'AnonymousUser') {
            console.log(user);
            console.log('user not logged in');
        } else {
            updateUserOrder(productId, action)

        }
    });
});

const updateUserOrder = (productId, action) => {
    const url = '/update_item/'
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json; charset=UTF-8",
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
        }),
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log(data);
            location.reload()
        })
}
