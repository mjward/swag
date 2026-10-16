"""Count writing habits in a file of collected messages.

Input lines look like "DATE | WHERE | text". WHERE starts with the kind of
place: DM, CHANNEL or EMAIL, optionally followed by a name in brackets. Prints a
markdown report for the voice profile's stats.md.

Usage: python3 -I voice_stats.py [--words yep,tho,reckon] raw/chat-*.txt > stats.md

--words lists the user's own slang and stock words (from the Collector
reports). Each gets a "Words in context" entry: where and when they use it, and
example messages.
"""

import collections
import re
import statistics
import sys

STOPWORDS = set(
    """a about above after again all am an and any are as at be because been
    before being below between both but by can could did do does doing down
    during each few for from further had has have having he her here hers him
    his how i if in into is it its itself just me more most my no nor not now
    of off on once only or other our ours out over own same she should so some
    such than that the their them then there these they this those through to
    too under until up very was we were what when where which while who whom
    why will with would you your yours i'm i've i'll i'd it's that's don't
    can't won't we'll we're we've you're they're there's let's""".split()
)
INFORMAL_MARKERS = [
    "yeah", "yep", "yes", "yup", "nah", "nope", "mate", "dude", "folks",
    "team", "tho", "though", "gonna", "wanna", "reckon", "keen",
    "cheers", "thanks", "thx", "ta", "haha", "lol", "lmao", "please", "pls",
    "fyi", "imo", "tbh", "iirc", "afaict", "btw", "atm", "def",
]
CONTRACTION_STEMS = ["don", "can", "won", "didn", "doesn", "isn", "wasn", "i", "that"]
DROPPED = re.compile(r"\b(dont|cant|wont|didnt|doesnt|isnt|wasnt|im|ive|thats)\b")
KEPT = re.compile(r"\b(?:%s)['’](?:t|m|ve|ll|s)\b" % "|".join(CONTRACTION_STEMS))
SHORTCODE = re.compile(r":[a-z0-9_+-]+:")
UNICODE_EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")
REDACTED = re.compile(r"\[[^\]]*omitted\]")


def load(paths):
    messages = []
    for path in paths:
        with open(path, encoding="utf-8", errors="ignore") as handle:
            for line in handle:
                parts = line.rstrip("\n").split(" | ", 2)
                if len(parts) == 3 and not REDACTED.search(parts[2]):
                    messages.append((parts[1].upper(), parts[2].replace("\\n", " "), parts[0]))
    return messages


def share(predicate, texts):
    return f"{100 * sum(map(predicate, texts)) / len(texts):.0f}%"


def median_words(texts):
    return statistics.median(len(t.split()) for t in texts) if texts else 0


def word_in_context(word, messages):
    pattern = re.compile(r"(?<![a-z'])" + re.escape(word.lower()) + r"(?![a-z'])")
    uses = [(where, text) for where, text, _ in messages if pattern.search(text.lower())]
    if not uses:
        print(f"### {word} (0)\n")
        return
    places = collections.Counter(re.split(r"[\s(]", where, maxsplit=1)[0] for where, _ in uses)
    channels = collections.Counter(
        where.split("(", 1)[1].rstrip(")") for where, _ in uses if where.startswith("CHANNEL(")
    )
    years = collections.Counter(date[:4] for _, text, date in messages if pattern.search(text.lower()))
    print(f"### {word} ({len(uses)})\n")
    print("- Where: " + ", ".join(f"{kind} {n}" for kind, n in places.most_common()))
    if channels:
        print("- Top channels: " + ", ".join(f"{name} {n}" for name, n in channels.most_common(4)))
    print("- By year: " + ", ".join(f"{year} {n}" for year, n in sorted(years.items())))
    at_end = sum(text.lower().rstrip(" ?!.").endswith(word.lower()) for _, text in uses)
    at_start = sum(text.lower().startswith(word.lower()) for _, text in uses)
    print(f"- Opens the message {at_start} times, ends it {at_end} times")
    for _, text in sorted(uses, key=lambda use: len(use[1]))[len(uses) // 4:][:4]:
        print(f"- {text[:140]}")
    print()


def report(messages, context_words=()):
    texts = [text for _, text, _ in messages]
    if not texts:
        sys.exit("No messages found. Check the file paths and the DATE | KIND | text format.")
    lowered = " ".join(texts).lower()
    words = re.findall(r"[a-z][a-z'’]*", lowered)
    by_kind = collections.defaultdict(list)
    for where, text, _ in messages:
        by_kind[re.split(r"[\s(]", where, maxsplit=1)[0]].append(text)

    print(f"# Writing habits\n\n{len(texts)} messages, {len(words)} words.\n")
    print("## Length\n")
    print(f"- Median words per message: {median_words(texts)}")
    for kind, kind_texts in sorted(by_kind.items()):
        print(f"- {kind}: {median_words(kind_texts)} ({len(kind_texts)} messages)")
    print()

    print("## Mechanics\n")
    print(f"- No full stop, ! or ? at the end: {share(lambda t: not t.rstrip().endswith(('.', '!', '?')), texts)}")
    print(f"- Starts lowercase: {share(lambda t: t[:1].islower(), texts)}")
    print(f"- Has .. or ...: {share(lambda t: '..' in t or '…' in t, texts)}")
    print(f"- Has an emoji shortcode: {share(lambda t: bool(SHORTCODE.search(t)), texts)}")
    print(f"- Has a Unicode emoji: {share(lambda t: bool(UNICODE_EMOJI.search(t)), texts)}")
    print(f"- Has an em dash: {sum('—' in t for t in texts)} messages (check these for AI drafting)")
    print(f"- Has a spaced hyphen ' - ': {sum(' - ' in t for t in texts)} messages")
    print(f"- Has a semicolon: {sum(';' in t for t in texts)} messages")
    dropped, kept = len(DROPPED.findall(lowered)), len(KEPT.findall(lowered))
    if dropped + kept:
        print(f"- Contractions without the apostrophe: {100 * dropped / (dropped + kept):.0f}% ({dropped} of {dropped + kept})")
    print()

    counts = collections.Counter(words)
    print("## Informal markers (count)\n")
    for marker in INFORMAL_MARKERS:
        if counts[marker]:
            print(f"- {marker}: {counts[marker]}")
    print("\n## Most used emoji\n")
    emoji = collections.Counter(SHORTCODE.findall(lowered) + UNICODE_EMOJI.findall(lowered))
    for code, n in emoji.most_common(25):
        print(f"- {code} {n}")
    print("\n## Emoji in context\n")
    print("Where each of the top emoji appears, and up to three messages that use it.\n")
    for code, n in emoji.most_common(15):
        places = collections.Counter(
            re.split(r"[\s(]", where, maxsplit=1)[0]
            for where, text, _ in messages if code in text.lower()
        )
        where_text = ", ".join(f"{kind} {count}" for kind, count in places.most_common())
        uses = [text for _, text, _ in messages if code in text.lower()]
        alone = sum(not SHORTCODE.sub("", UNICODE_EMOJI.sub("", t)).strip() for t in uses)
        print(f"### {code} ({n}: {where_text}; {alone} on its own as the whole reply)\n")
        with_words = [t for t in uses if len(SHORTCODE.sub("", t).split()) >= 3]
        for text in sorted(with_words, key=len)[:4]:
            print(f"- {text[:140]}")
        print()
    if context_words:
        print("\n## Words in context\n")
        for word in context_words:
            word_in_context(word, messages)
    print("\n## Most used words, stopwords removed\n")
    common = [(w, n) for w, n in counts.most_common(400) if w not in STOPWORDS and len(w) > 1]
    print(", ".join(f"{w} {n}" for w, n in common[:80]))
    print("\n## Messages with an em dash (check each for AI drafting)\n")
    for text in texts:
        if "—" in text:
            print(f"- {text[:120]}")


if __name__ == "__main__":
    args = sys.argv[1:]
    words = []
    if args[:1] == ["--words"] and len(args) > 1:
        words = [w.strip() for w in args[1].split(",") if w.strip()]
        args = args[2:]
    if not args:
        sys.exit("usage: voice_stats.py [--words a,b,c] FILE [FILE ...]")
    report(load(args), words)
