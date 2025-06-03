import { Crepe } from "@milkdown/crepe";
import "@milkdown/crepe/theme/common/style.css";
import "@milkdown/crepe/theme/nord-dark.css";

const crepe = new Crepe({
  root: "#milkdown",
  features: {
    [Crepe.Feature.BlockEdit]: false,
  },
  featureConfigs: {
    [Crepe.Feature.Placeholder]: {
      text: 'Zacznij pisać...',
      mode: 'block',
    },
  },
});

crepe.create();

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form .milkdown button:not([type])").forEach(btn => {
    btn.setAttribute("type", "button");
  });
});