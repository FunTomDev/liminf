function updateTilt(event) {
        const element = event.currentTarget;
        const { width, height, left, top } = element.getBoundingClientRect();
        const centerX = left + width / 2;
        const centerY = top + height / 2;

        const deltaX = event.clientX - centerX;
        const deltaY = event.clientY - centerY;

        const rotateX = (deltaY / height) * 20; // 20 degrees of tilt on the X axis
        const rotateY = (deltaX / width) * -20; // -20 degrees of tilt on the Y axis

        element.style.setProperty('--rotate-x', `${-rotateX}deg`);
        element.style.setProperty('--rotate-y', `${-rotateY}deg`);
		
    }

window.updateTilt = updateTilt;