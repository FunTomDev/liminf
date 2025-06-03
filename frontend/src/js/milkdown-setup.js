import { Crepe } from "@milkdown/crepe";
import "@milkdown/crepe/theme/common/style.css";
import "@milkdown/crepe/theme/nord-dark.css";

const crepe = new Crepe({
  root: "#milkdown",
  features: {
    [Crepe.Feature.BlockEdit]: false,
  },
});

crepe.create();

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form .crepe button:not([type])").forEach(btn => {
    btn.setAttribute("type", "button");
  });
});