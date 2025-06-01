import { defaultValueCtx, Editor, rootCtx } from "https://esm.sh/@milkdown/kit/core";
import { history } from "https://esm.sh/@milkdown/kit/plugin/history";
import { commonmark } from "https://esm.sh/@milkdown/kit/preset/commonmark";
import { nord } from "https://esm.sh/@milkdown/theme-nord";
import { math } from "https://esm.sh/@milkdown/plugin-math"
import { prism } from "https://esm.sh/@milkdown/plugin-prism"
import { listener } from "https://esm.sh/@milkdown/plugin-listener"
import { indent, indentConfig } from "https://esm.sh/@milkdown/plugin-indent"
import { tooltipFactory } from "https://esm.sh/@milkdown/plugin-tooltip"
import { TooltipProvider } from "https://esm.sh/@milkdown/kit/plugin/tooltip"

const tooltip = tooltipFactory('my-tooltip')

function tooltipPluginView(view) {
  const content = document.createElement('div')

  const provider = new TooltipProvider({
    content: this.content,
  })

  return {
    update: (updatedView, prevState) => {
      provider.update(updatedView, prevState)
    },
    destroy: () => {
      provider.destroy()
      content.remove()
    },
  }
}

const editor = await Editor.make()
    .config((ctx) => {
        ctx.set(rootCtx, "#milkdown");
        ctx.set(indentConfig.key, {
            type: 'space',
            size: 4,
        });
        ctx.set(tooltip.key, {
            view: tooltipPluginView,
        });
    })
    .use(nord)
    .use(commonmark)
    .use(prism)
    .use(math)
    .use(history)
    .use(listener)
    .use(indent)
    .use(tooltip)
    .create(document.querySelector('#milkdown'), {
    defaultValue: 'Type here...',
});

console.log("Editor created", editor);