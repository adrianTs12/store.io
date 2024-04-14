let pendientes = document.getElementById('pendientes');
let realizadas = document.getElementById('realizadas')

let total_pendientes = document.getElementById('total-pendientes');
let total_realizadas = document.getElementById('total-realizadas');

const select = document.querySelector('select');
let precio_total = document.querySelector('.precio_total')

total_pendientes.style.display = ''
pendientes.style.display = ''


select.addEventListener('change', function(){
    realizadas.style.display = 'none';
    pendientes.style.display = 'none';
    total_pendientes.style.display = 'none';
    total_realizadas.style.display = 'none';

    suma = 0

    if(select.value === realizadas.id){
        realizadas.style.display = '';
        total_realizadas.style.display = '';

    } else {
        pendientes.style.display = '';
        total_pendientes.style.display = '';
    };

});