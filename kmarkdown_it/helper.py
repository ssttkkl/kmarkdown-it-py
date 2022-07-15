from markdown_it.rules_inline import StateInline

__all__ = ("check_label", "get_max_label_length", "get_label", "meet_label")


def check_label(state: StateInline, label_start: int, label_end: int, label_name: str | set | None = None):
    label = state.src[label_start + 1:label_end - 1]
    if (isinstance(label_name, str) and label != label_name) \
            or (isinstance(label_name, set) and label not in label_name):
        return False
    else:
        return True


def get_max_label_length(label_name: str | set | None = None):
    if isinstance(label_name, str):
        return len(label_name) + 2
    elif isinstance(label_name, set):
        return max(map(len, label_name)) + 2
    else:
        return -1


def get_label(state: StateInline,
              pos: int, pos_max: int,
              label_name: str | set | None = None,
              start_marker: int = 0x28,  # /* ( */
              end_marker: int = 0x29):  # /* ) */
    """
    if there begins a label, return the end position (inclusive) of it,
    or -1 if it's not a valid label
    :param state: StateInline
    :param pos: beginning position of a label
    :param pos_max: max position where we will search
    :param label_name: specify label name
    :param start_marker: start marker of a label
    :param end_marker: end marker of a label
    :return: the end position (inclusive) of it, or -1 if it's not a valid label
    """
    if state.srcCharCode[pos] != start_marker:
        return -1

    label_start = pos
    label_end = label_start + 1

    while label_end < pos_max:
        if state.srcCharCode[label_end] == end_marker:
            break
        label_end += 1

    label_end += 1

    if label_end <= pos_max:
        if check_label(state, label_start, label_end, label_name):
            return label_end

    return -1


def meet_label(state: StateInline,
               pos: int, pos_max: int,
               label_name: str | set | None = None,
               start_marker: int = 0x28,  # /* ( */
               end_marker: int = 0x29):  # /* ) */
    """
    search for the first label from the given position,
    return the start and the end position (inclusive) of it,
    or -1, -1 if there's no label
    :param state: StateInline
    :param pos: position where we begin searching
    :param pos_max: max position where we will search
    :param label_name: specify label name
    :param start_marker: start marker of a label
    :param end_marker: end marker of a label
    :return: the end position (inclusive) of it, or -1 if it's not a valid label
    """

    label_start = pos
    while label_start < pos_max:
        while label_start < pos_max and state.srcCharCode[label_start] != start_marker:
            label_start += 1

        if label_start < pos_max:
            label_end = get_label(state,
                                  label_start, min(pos_max, label_start + get_max_label_length(label_name)),
                                  None,
                                  start_marker, end_marker)
            if label_end != -1:
                if not check_label(state, label_start, label_end, label_name):
                    label_start = label_end
                    continue
                return label_start, label_end
            else:
                break
    return -1, -1
