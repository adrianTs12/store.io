btn_menu = document.getElementById('btn-menu');
btn_menu_img = document.getElementById('btn-menu-img')
header = document.getElementById('header');

btn_menu.addEventListener('click', function(){
    if(header.style.height == ''){
        header.style.height = '175px';
        btn_menu_img.src = '/static/img/x.png'
        // header.style.height = 'fit-content';
    } else {
        header.style.height = '';
        btn_menu_img.src = '/static/img/menu.png'
    }
});