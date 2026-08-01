import re


def clean_filename(text, max_length=80):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s-]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        "-",
        text
    )

    text = re.sub(
        r"-+",
        "-",
        text
    )

    return text[:max_length].strip("-")
