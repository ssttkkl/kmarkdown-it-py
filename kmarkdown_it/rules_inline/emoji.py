import importlib.resources as pkg_resources
import json

from markdown_it.rules_inline import StateInline

from kmarkdown_it.rules_inline.helper import *
from .. import assets

with pkg_resources.open_text(assets, "emoji.json") as f:
    emojis = json.load(f)["emojis"]

    support_labels = set([x["en_name"] for x in emojis])
    max_support_labels_len = get_max_label_length(support_labels)

    emoji_mapping = dict()
    for x in emojis:
        emoji_mapping[x["en_name"]] = x["icon"]


def emoji(state: StateInline, silent: bool = False):
    pos = state.pos
    pos_max = state.posMax

    if state.srcCharCode[pos] != 0x3A:  # /* : */
        return False

    # get label
    pos_label_end = get_label(state,
                              pos, min(pos_max, pos + max_support_labels_len),
                              support_labels,
                              0x3A,  # /* : */:
                              0x3A)  # /* : */:
    if pos_label_end == -1:
        return False

    label = state.src[pos + 1:pos_label_end - 1]

    if not silent:
        state.pending += emoji_mapping[label]

    state.pos = pos_label_end
    state.posMax = pos_max
    return True
