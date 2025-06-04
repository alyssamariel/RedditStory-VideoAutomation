import re

def clean_text(text):
    # Remove URLs
    text = re.sub(r"(https?://)?[a-zA-Z0-9./?:@\-_=#]+\.([a-zA-Z]{2,6})([a-zA-Z0-9.&/?@\-_=#]*)"," ",text,)

    # replace abbrivations
    abbreviations = {"AI": "A.I", "AGI": "A.G.I"}
    for abbr, replacement in abbreviations.items():
        text = re.sub(fr"\b{abbr}\b", replacement, text)

    # add period in the end of text if missing
    if not text.endswith("."):
        text += "."

    # clean up duplicate/extra periods
    text = re.sub(r"\. ?\. ?\. ?", ".", text)          # replace multiple dots with one
    text = re.sub(r'\."\.', '".', text)                # fix trailing punctuation

    return text.strip()