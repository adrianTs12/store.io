let productos = document.getElementsByClassName('producto');
let search = document.getElementById('search');

search.addEventListener('input', () => {
    let buscar = search.value.toLowerCase();
    let resultado = false

    for (let i = 0; i < productos.length; i++) {
        productText = productos[i].innerText.toLowerCase();

        if (productText.includes(buscar)) {
            productos[i].style.display = '';
        } else {
            productos[i].style.display = 'none';
        };

    };
});