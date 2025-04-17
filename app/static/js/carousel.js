import EmblaCarousel from './embla-carousel';

const emblaNode = document.querySelector('.embla');
const options = {};
const plugins = [Autoplay()];
const emblaApi = EmblaCarousel(emblaNode, options, plugins);

console.log(emblaApi.slideNodes());