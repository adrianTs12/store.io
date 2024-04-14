const btn_menos = document.getElementById('btn-menos');
const btn_mas = document.getElementById('btn-mas');
let cantidad = document.getElementById('cantidad');
let precio = document.getElementById('precio');
const cantidad_max = document.getElementById('cantidad-max');


let input = document.getElementById('input');

precio_base = precio.textContent.replace('$', ' ')

valor = 1

btn_menos.addEventListener('click', function () {
    if (valor > 1) {
        valor -= 1
    }

    cantidad.textContent = valor;
    precio.textContent = `$${precio_base * valor}`;
    input.value = cantidad.textContent
});

btn_mas.addEventListener('click', function () {
    if (valor < cantidad_max.value) {
        valor += 1
        cantidad.textContent = valor;
        precio.textContent = `$${precio_base * valor}`;
        input.value = cantidad.textContent
    }
});