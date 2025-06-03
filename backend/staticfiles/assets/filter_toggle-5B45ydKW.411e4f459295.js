function n(){const e=document.getElementById("filters-wrapper");document.getElementById("toggle-filters-btn"),e.classList.contains("section-visible")?l(e):c(e)}function l(e,i,o){e._hideTimeout&&clearTimeout(e._hideTimeout),e.classList.remove("section-visible"),e.classList.add("section-invisible"),e._hideTimeout=setTimeout(()=>{e.classList.add("hidden"),e._hideTimeout=null},300)}function c(e,i,o){e._hideTimeout&&(clearTimeout(e._hideTimeout),e._hideTimeout=null),e.classList.remove("hidden"),e.offsetWidth,setTimeout(()=>{e.classList.add("section-visible"),e.classList.remove("section-invisible"),e._hideTimeout=null},0)}document.getElementById("toggle-filters-btn").addEventListener("click",n);window.addEventListener("resize",t);function t(){const e=document.getElementById("filters-wrapper");window.innerWidth<1080?(e.classList.remove("desktop"),e.classList.add("mobile")):(e.classList.remove("mobile"),e.classList.add("desktop"))}const s=document.createElement("style");s.textContent=`
    #filters-wrapper {
	transition: margin 0.3s cubic-bezier(0.4, 0, 0.2, 1), width 0.3s cubic-bezier(0.4, 0, 0.2, 1), height 0.3s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s ease;
}

#filters-wrapper.mobile.section-invisible {
	opacity: 0;
    margin-bottom: 0;
    transform: scaleY(0);
	transform-origin: top center;
	pointer-events: none;
}

#filters-wrapper.mobile.section-visible {
	opacity: 1;
    margin-bottom: 2rem;
    transform: scaleY(1);
	transform-origin: top center;
	pointer-events: auto;
}

#filters-wrapper.desktop.section-invisible {
    width: 0;
    overflow-x: hidden;
	transform: scaleX(0);
    transform-origin: center left;
	opacity: 0;
	pointer-events: none;
}

#filters-wrapper.desktop.section-visible {
    width: 350px;
    margin-right: 2rem;
    transform-origin: center left;
	transform: scaleX(1);
	opacity: 1;
	pointer-events: auto;
}
`;document.head.appendChild(s);t();
