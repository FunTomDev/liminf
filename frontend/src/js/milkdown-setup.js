import { Crepe } from "@milkdown/crepe";
import "@milkdown/crepe/theme/common/style.css";
import "@milkdown/crepe/theme/nord-dark.css";

window.initMilkdown = async function initMilkdown(target = document){
  console.log("Crepe initialized")
  const path = window.location.pathname;

  const contentInput = target.querySelector("#id_content")
  const milkdownRoot = target.querySelector("#milkdown")

  const readonly = milkdownRoot.dataset.readonly === 'true';
  const defaultMarkdown = milkdownRoot.dataset.markdown;

  const crepe = new Crepe({
    root: target.querySelector("#milkdown"),

    defaultValue: defaultMarkdown,

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

  // Get markdown content
  await crepe.create();
  const markdown = crepe.getMarkdown();

  if (readonly) {
      crepe.setReadonly(true);
      document.querySelector(".milkdown-latex-inline-edit").remove();
  }
  else{
    // Register event listeners
    crepe.on((listener) => {
      listener.markdownUpdated((ctx, markdown) => {
        contentInput.value = markdown;
        document.querySelectorAll("form .milkdown button:not([type])").forEach(btn => {
          btn.setAttribute("type", "button");
        });
      });
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.initMilkdown();
});
