import { Crepe } from "@milkdown/crepe";
import "@milkdown/crepe/theme/common/style.css";
import "@milkdown/crepe/theme/nord-dark.css";

const contentInput = document.getElementById("id_content")

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

await crepe.create();

// Get markdown content
const markdown = crepe.getMarkdown();

// Register event listeners
crepe.on((listener) => {
  listener.markdownUpdated((ctx, markdown) => {
    contentInput.value = markdown;
    console.log("Current input value is ", contentInput.value)
  });
});

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form .milkdown button:not([type])").forEach(btn => {
    btn.setAttribute("type", "button");
  });
});