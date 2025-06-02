import { defaultValueCtx, Editor, rootCtx } from "https://esm.sh/@milkdown/kit/core";
import { history } from "https://esm.sh/@milkdown/kit/plugin/history";
import { commonmark } from "https://esm.sh/@milkdown/kit/preset/commonmark";
import { nord } from "https://esm.sh/@milkdown/theme-nord";
import { math } from "https://esm.sh/@milkdown/plugin-math"
import { prism } from "https://esm.sh/@milkdown/plugin-prism"
import { listener } from "https://esm.sh/@milkdown/plugin-listener"
import { indent, indentConfig } from "https://esm.sh/@milkdown/plugin-indent"

const editor = await Editor.make()
    .config((ctx) => {
        ctx.set(rootCtx, "#milkdown");
        ctx.set(indentConfig.key, {
            type: 'space',
            size: 4,
        });
    })
    .use(nord)
    .use(commonmark)
    .use(prism)
    .use(math)
    .use(history)
    .use(listener)
    .use(indent)
    .create(document.querySelector('#milkdown'), {
    defaultValue: 'Type here...',
});

console.log("Editor created", editor);