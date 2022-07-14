from abc import ABC, abstractmethod
from typing import Iterable


class Element(ABC):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        raise NotImplementedError()


class SpanElement(Element, ABC):
    pass


class BlockElement(Element, ABC):
    pass


class Paragraph(BlockElement):
    def __init__(self, spans: Iterable[SpanElement]):
        self.spans = spans

    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "Paragraph"


class UnarySpanElement(SpanElement, ABC):
    def __init__(self, x: "Element"):
        self.x = x


class BinarySpanElement(SpanElement, ABC):
    def __init__(self, x: "Element", y: "Element"):
        self.x = x
        self.y = y


class VariadicBlockElement(BlockElement, ABC):
    def __init__(self, blocks: Iterable[BlockElement]):
        self.blocks = blocks


class Text(SpanElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "text"


class Bold(UnarySpanElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "bold"


class Italic(UnarySpanElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "italic"


class LineThrough(UnarySpanElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "line_through"


class Hyperlink(BinarySpanElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "hyperlink"


class Splitter(BlockElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "splitter"


class Quoted(VariadicBlockElement):
    def __init__(self, blocks: Iterable[BlockElement]):
        super().__init__(blocks)
        self.blocks = blocks

    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "quoted"


class Underlined(UnarySpanElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "underlined"


class Masked(UnarySpanElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "masked"


class Emoji(SpanElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "emoji"


class ServerEmoji(SpanElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "server_emoji"


class Channel(SpanElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "channel"


class User(SpanElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "user"


class Role(SpanElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "role"


class InlineCode(SpanElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "inline_code"


class BlockCode(BlockElement):
    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return "block_code"
