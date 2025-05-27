function toggleFiltersAnimated() {
	const filtersWrapper = document.getElementById('filters-wrapper');
	const toggleBtn = document.getElementById('toggle-filters-btn');
	const isMobile = window.innerWidth < 1080;
	const isVisible = filtersWrapper.classList.contains('section-visible');

	if (isVisible) {
		hideFilters(filtersWrapper, toggleBtn, isMobile);
	} else {
		showFilters(filtersWrapper, toggleBtn, isMobile);
	}
}

function hideFilters(filtersWrapper, toggleBtn, isMobile) {
    // Clear any existing timeout
    if (filtersWrapper._hideTimeout) {
        clearTimeout(filtersWrapper._hideTimeout);
    }

    filtersWrapper.classList.remove('section-visible');
    filtersWrapper.classList.add('section-invisible');

    filtersWrapper._hideTimeout = setTimeout(() => {
        filtersWrapper.classList.add('hidden');
        filtersWrapper._hideTimeout = null; // Clear reference
    }, 300); // Match the CSS transition duration
}

function showFilters(filtersWrapper, toggleBtn, isMobile) {
    // Clear any existing timeout so it doesn’t apply .hidden after reopening
    if (filtersWrapper._hideTimeout) {
        clearTimeout(filtersWrapper._hideTimeout);
        filtersWrapper._hideTimeout = null;
    }

    filtersWrapper.classList.remove('hidden');
    setTimeout(() => {
        filtersWrapper.classList.remove('section-invisible');
        filtersWrapper.classList.add('section-visible');
    }, 0); // Force reflow
}

document.getElementById('toggle-filters-btn').addEventListener('click', toggleFiltersAnimated);
window.addEventListener('resize', handleFilterResize);

function handleFilterResize() {
	const filtersWrapper = document.getElementById('filters-wrapper');
	const isMobile = window.innerWidth < 1080;

	if (isMobile) {
		filtersWrapper.classList.remove('desktop');
		filtersWrapper.classList.add('mobile');
	} else {
		filtersWrapper.classList.remove('mobile');
		filtersWrapper.classList.add('desktop');
	}
}

// Add some CSS for smooth transitions (add this to your stylesheet)
const style = document.createElement('style');
style.textContent = `
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
`;
document.head.appendChild(style);
handleFilterResize(); // Initial call to set the correct state on page load