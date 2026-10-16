"""Show what the user changed between a draft and the message they sent.

Usage: python3 -I draft_diff.py DRAFT_FILE SENT_FILE

Prints the words removed and added, then a similarity score, so the agent can
turn each change into a lesson for corrections.md. Similarity under 0.3 usually
means the user wrote their own reply rather than editing the draft.
"""

import difflib
import re
import sys


def words(path):
    with open(path, encoding="utf-8") as handle:
        return re.findall(r"\S+", handle.read())


def main(draft_path, sent_path):
    draft, sent = words(draft_path), words(sent_path)
    matcher = difflib.SequenceMatcher(a=draft, b=sent, autojunk=False)
    print(f"Similarity: {matcher.ratio():.2f}\n")
    for tag, a1, a2, b1, b2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        removed, added = " ".join(draft[a1:a2]), " ".join(sent[b1:b2])
        if tag == "replace":
            print(f"- changed: \"{removed}\" => \"{added}\"")
        elif tag == "delete":
            print(f"- cut: \"{removed}\"")
        else:
            print(f"- added: \"{added}\"")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: draft_diff.py DRAFT_FILE SENT_FILE")
    main(sys.argv[1], sys.argv[2])
