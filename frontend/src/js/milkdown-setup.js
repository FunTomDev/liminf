import { Crepe } from "@milkdown/crepe";
import "@milkdown/crepe/theme/common/style.css";
import "@milkdown/crepe/theme/nord-dark.css";

window.initMilkdown = async function initMilkdown(target = document){
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
      document.querySelectorAll('.milkdown-code-block').forEach(editor => {
      // Check if it's a LaTeX editor based on the language button label
      const langButton = editor.querySelector('.language-button');
      if (langButton?.textContent.includes('LaTeX')) {
          // Hide the code editor host
          const codeMirrorHost = editor.querySelector('.codemirror-host');
          if (codeMirrorHost) {
              codeMirrorHost.classList.add('hidden');
          }

          // Remove the toolbar (tools)
          const tools = editor.querySelector('.tools');
          const divider = editor.querySelector('.preview-divider')
          if (tools) {
              tools.remove();
          }
          if (divider){
            divider.remove();
          }
      }
  });
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
