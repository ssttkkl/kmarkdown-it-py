from io import StringIO
from typing import Mapping, Callable, Union, Optional, MutableMapping

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererProtocol, RendererHTML
from markdown_it.tree import SyntaxTreeNode

from .rules_inline import emphasis
from .rules_inline.emoji import emoji
from .rules_inline.kmarkdown_label import kmarkdown_label
from .rules_inline.server_emoji import server_emoji
from .rules_inline.text import text


class KMarkdownIt(MarkdownIt):
    def __init__(self, config: Union[str, Mapping] = "commonmark",
                 options_update: Optional[Mapping] = None,
                 *,
                 renderer_cls: Callable[[MarkdownIt], RendererProtocol] = RendererHTML, ):
        super().__init__(config, options_update, renderer_cls=renderer_cls)

        self.block.ruler.disable("table")
        self.block.ruler.disable("list")
        self.block.ruler.disable("html_block")
        self.block.ruler.disable("heading")
        self.block.ruler.disable("lheading")

        self.inline.ruler.disable("image")
        self.inline.ruler.disable("autolink")
        self.inline.ruler.disable("html_inline")

        self.inline.ruler.enable("strikethrough")
        self.inline.ruler2.enable("strikethrough")

        self.inline.ruler.at("text", text)
        self.inline.ruler.at("emphasis", emphasis.tokenize)
        self.inline.ruler2.at("emphasis", emphasis.postProcess)
        self.inline.ruler.before("link", "server_emoji", server_emoji)
        self.inline.ruler.after("server_emoji", "kmarkdown_label", kmarkdown_label)
        self.inline.ruler.before("entity", "emoji", emoji)

    def extract_plain_text(self, src: str, env: Optional[MutableMapping] = None) -> str:
        tokens = self.parse(src, env)
        tree = SyntaxTreeNode(tokens)

        buffer = StringIO()
        self._extract_plain_text_root(tree, buffer)
        return buffer.getvalue().strip()

    @staticmethod
    def _extract_plain_text_root(node: SyntaxTreeNode, buffer: StringIO):
        for b in node.children:
            KMarkdownIt._extract_plain_text_block(b, buffer)

    @staticmethod
    def _extract_plain_text_block(node: SyntaxTreeNode, buffer: StringIO):
        if node.type == "code_block" or node.type == "fence":
            buffer.write(node.content)
            buffer.write('\n')
        else:
            for b in node.children:
                if b.type == "inline":
                    KMarkdownIt._extract_plain_text_inline(b, buffer)
                    buffer.write('\n')
                else:
                    KMarkdownIt._extract_plain_text_block(b, buffer)

            if node.type == "paragraph":
                buffer.write('\n')

    @staticmethod
    def _extract_plain_text_inline(node: SyntaxTreeNode, buffer: StringIO):
        if node.type == "text" or node.type == "code_inline":
            buffer.write(node.content)
        elif node.type == "softbreak":
            buffer.write('\n')
        else:
            for b in node.children:
                KMarkdownIt._extract_plain_text_inline(b, buffer)
