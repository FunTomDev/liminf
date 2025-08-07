const addTogglePrevNextBtnsActive = (emblaApi, prevBtn, nextBtn) => {
    const togglePrevNextBtnsState = () => {
        if (emblaApi.canScrollPrev()) prevBtn.removeAttribute('disabled');
        else prevBtn.setAttribute('disabled', 'disabled');

        if (emblaApi.canScrollNext()) nextBtn.removeAttribute('disabled');
        else nextBtn.setAttribute('disabled', 'disabled');
    };

    emblaApi
        .on('select', togglePrevNextBtnsState)
        .on('init', togglePrevNextBtnsState)
        .on('reInit', togglePrevNextBtnsState);

    return () => {
        prevBtn.removeAttribute('disabled');
        nextBtn.removeAttribute('disabled');
    };
};

const addPrevNextBtnsClickHandlers = (emblaApi, prevBtn, nextBtn, onButtonClick) => {
    const scrollPrev = () => {
        emblaApi.scrollPrev();
        if (onButtonClick) onButtonClick(emblaApi);
    };
    const scrollNext = () => {
        emblaApi.scrollNext();
        if (onButtonClick) onButtonClick(emblaApi);
    };

    prevBtn.addEventListener('click', scrollPrev, false);
    nextBtn.addEventListener('click', scrollNext, false);

    const removeTogglePrevNextBtnsActive = addTogglePrevNextBtnsActive(
        emblaApi,
        prevBtn,
        nextBtn
    );

    return () => {
        removeTogglePrevNextBtnsActive();
        prevBtn.removeEventListener('click', scrollPrev, false);
        nextBtn.removeEventListener('click', scrollNext, false);
    };
};

document.addEventListener('DOMContentLoaded', function () {
    const emblaNodes = document.querySelectorAll('.embla');
    if (!emblaNodes.length) return;

    emblaNodes.forEach((emblaNode) => {
        console.log('emblaNode', emblaNode);
        const viewportNode = emblaNode.querySelector('.embla__viewport');
        const prevBtnNode = emblaNode.querySelector('.embla__button--prev');
        const nextBtnNode = emblaNode.querySelector('.embla__button--next');

        const OPTIONS = {
            align: 'start',
        };


        const emblaApi = EmblaCarousel(viewportNode, OPTIONS);

        const removePrevNextBtnsClickHandlers = addPrevNextBtnsClickHandlers(
            emblaApi,
            prevBtnNode,
            nextBtnNode,
        );

        emblaApi.on('destroy', removePrevNextBtnsClickHandlers);
    });
});