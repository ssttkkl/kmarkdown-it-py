from typing import Mapping, Callable, Union, Optional

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererProtocol, RendererHTML

from .rules_inline.emoji import emoji
from .rules_inline.kmarkdown_label import kmarkdown_label
from .rules_inline.server_emoji import server_emoji
from .rules_inline.text import text


def KMarkdownIt(config: Union[str, Mapping] = "commonmark",
                options_update: Optional[Mapping] = None,
                *,
                renderer_cls: Callable[[MarkdownIt], RendererProtocol] = RendererHTML, ) -> MarkdownIt:
    md = MarkdownIt(config, options_update, renderer_cls=renderer_cls)

    md.block.ruler.disable("table")
    md.block.ruler.disable("list")
    md.block.ruler.disable("html_block")
    md.block.ruler.disable("heading")
    md.block.ruler.disable("lheading")

    md.inline.ruler.disable("image")
    md.inline.ruler.disable("autolink")
    md.inline.ruler.disable("html_inline")

    md.inline.ruler.at("text", text)
    md.inline.ruler.before("link", "server_emoji", server_emoji)
    md.inline.ruler.after("server_emoji", "kmarkdown_label", kmarkdown_label)
    md.inline.ruler.before("entity", "emoji", emoji)

    return md
