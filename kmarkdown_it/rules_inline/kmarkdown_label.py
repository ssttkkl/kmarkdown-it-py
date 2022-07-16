from markdown_it.rules_inline import StateInline

from kmarkdown_it.rules_inline.helper import *

support_labels = {"ins", "spl", "chn", "met", "rol"}
max_support_labels_len = get_max_label_length(support_labels)


def kmarkdown_label(state: StateInline, silent: bool = False):
    pos = state.pos
    pos_max = state.posMax

    if state.srcCharCode[pos] != 0x28:  # /* ( */
        return False

    # get label
    pos_label_end = get_label(state,
                              pos, min(pos_max, pos + max_support_labels_len),
                              support_labels)
    if pos_label_end == -1:
        return False

    label = state.src[pos + 1:pos_label_end - 1]

    # get next label
    pos_label2_begin, pos_label2_end = meet_label(state, pos_label_end, pos_max, label)
    if pos_label2_end == -1:
        return False

    if not silent:
        if label == "ins":
            state.push("ins_open", "u", 1)

            state.pos = pos_label_end
            state.posMax = pos_label2_begin
            state.md.inline.tokenize(state)

            state.push("ins_close", "u", -1)
        elif label == "spl":
            state.push("spl_open", "mask", 1)

            state.pos = pos_label_end
            state.posMax = pos_label2_begin
            state.md.inline.tokenize(state)

            state.push("spl_close", "mask", -1)
        else:
            content = state.src[pos_label_end:pos_label2_begin]
            token = state.push(label, label, 0)
            token.content = content

    state.pos = pos_label2_end
    state.posMax = pos_max
    return True
