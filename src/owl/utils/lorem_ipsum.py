import random

SENTENCES = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    "Curabitur pretium tincidunt lacus.",
    "Nulla gravida orci a odio.",
    "Nullam varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin mauris.",
    "Integer in mauris eu nibh euismod gravida.",
    "Duis ac tellus et risus vulputate vehicula.",
    "Donec lobortis risus a elit.",
    "Etiam tempor.",
    "Ut ullamcorper, ligula ut dictum pharetra, nisi nunc fringilla magna, in commodo elit erat nec turpis.",
    "Praesent elementum hendrerit tortor.",
    "Sed semper lorem at felis.",
    "Vestibulum volutpat, lacus a ultrices sagittis, mi neque euismod dui, eu pulvinar nunc sapien ornare nisl.",
    "Phasellus pede arcu, dapibus eu, fermentum et, dapibus sed, urna.",
    "Morbi interdum mollis sapien.",
    "Sed ac risus.",
    "Phasellus lacinia, magna a ullamcorper laoreet, lectus arcu pulvinar risus, vitae facilisis libero dolor a purus.",
    "Sed vel lacus.",
    "Mauris nibh felis, adipiscing varius, adipiscing in, lacinia vel, tellus.",
    "Suspendisse ac urna.",
    "Etiam pellentesque mauris ut lectus.",
    "Nunc tellus ante, mattis eget, gravida vitae, ultricies ac, leo.",
    "Integer leo pede, ornare a, lacinia eu, vulputate vel, luctus eu.",
    "Vivamus lacinia, enim vitae ultricies aliquam, nisi est tincidunt velit, id congue risus eros in sapien.",
    "Cras eu libero.",
    "Fusce dui leo, imperdiet in, aliquam sit amet, feugiat eu, orci.",
    "Aenean vel massa quis mauris vehicula lacinia.",
    "Quisque tincidunt scelerisque libero.",
    "Maecenas libero.",
    "Nam condimentum, sapien in viverra convallis, sem est commodo dolor, quis pulvinar quam ipsum sit amet dui.",
    "Proin eget tortor risus.",
    "Pellentesque in ipsum id orci porta dapibus.",
    "Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus.",
    "Curabitur non nulla sit amet nisl tempus convallis quis ac lectus.",
    "Nulla porttitor accumsan tincidunt.",
    "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae.",
    "Donec velit neque, auctor sit amet aliquam vel, ullamcorper sit amet ligula.",
]


def lorem_ipsum(sentences=None, words=None):
    """Generate lorem ipsum text.

    Args:
        sentences: Number of sentences to generate.
        words: Target number of words (text is built from whole sentences).

    Returns:
        A string of lorem ipsum text.
    """
    if sentences is not None and words is not None:
        raise ValueError("Specify either 'sentences' or 'words', not both.")

    # Always start with the classic opening sentences in order
    pool = list(SENTENCES)

    if words is not None:
        result = []
        count = 0
        # Use first few sentences in order, then shuffle the rest
        ordered = pool[:5]
        rest = pool[5:]
        random.shuffle(rest)
        available = ordered + rest

        for s in available:
            s_words = len(s.split())
            if count + s_words > words and count > 0:
                continue
            result.append(s)
            count += s_words
            if count >= words:
                break

        # If we still need more words, cycle through shuffled sentences
        while count < words:
            random.shuffle(rest)
            for s in rest:
                s_words = len(s.split())
                if count + s_words > words and count > 0:
                    continue
                result.append(s)
                count += s_words
                if count >= words:
                    break

        return " ".join(result)

    num = sentences if sentences is not None else 10
    # First 5 sentences stay in classic order, rest are shuffled
    if num <= 5:
        return " ".join(pool[:num])
    ordered = pool[:5]
    rest = pool[5:]
    random.shuffle(rest)
    return " ".join(ordered + rest[: num - 5])
