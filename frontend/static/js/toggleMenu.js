function toggleMenu() {
	const menu_button = document.querySelector('.menu-button');
	const menu_icon = document.querySelector('.menu-button').querySelector('.menu-icon');
	const mobile_nav = document.querySelector('.mobile-nav');
	const curtain = document.querySelector('.bg-curtain');
	document.body.classList.toggle('overflow-hidden');
	menu_icon.classList.toggle('menu-icon__open');
	mobile_nav.classList.toggle('mobile-nav__open');
	menu_button.classList.toggle('menu-button__open');
	curtain.classList.toggle('bg-curtain__open');
	menu_icon.classList.toggle('menu-icon__close');
	mobile_nav.classList.toggle('mobile-nav__close');
	menu_button.classList.toggle('menu-button__close');
	curtain.classList.toggle('bg-curtain__close');
}

document.querySelector('.menu-button').addEventListener('click', toggleMenu);
