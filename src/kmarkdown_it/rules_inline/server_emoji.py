from markdown_it.rules_inline import StateInline

from src.kmarkdown_it.helper import *

label = "emj"
label_len = get_max_label_length(label)


def server_emoji(state: StateInline, silent: bool = False):
    pos = state.pos
    pos_max = state.posMax

    if state.srcCharCode[pos] != 0x28:  # /* ( */
        return False

    # get label
    pos_label_end = get_label(state,
                              pos, min(pos_max, pos + label_len),
                              label)
    if pos_label_end == -1:
        return False

    # get next label
    pos_label2_begin, pos_label2_end = meet_label(state, pos_label_end, pos_max, label)
    if pos_label2_end == -1:
        return False

    if state.srcCharCode[pos_label2_end] != 0x5B:  # /* [ */
        return False

    pos_label3_end = get_label(state,
                               pos_label2_end, pos_max,
                               None,
                               0x5B,  # /* [ */
                               0x5D)  # /* ] */

    if pos_label3_end == -1:
        return False

    if not silent:
        emoji_name = state.src[pos_label_end:pos_label2_begin]
        emoji_id = state.src[pos_label2_end + 1:pos_label3_end - 1]
        token = state.push(label, label, 0)
        token.attrSet("emoji_name", emoji_name)
        token.attrSet("emoji_id", emoji_id)

    state.pos = pos_label2_end
    return True
