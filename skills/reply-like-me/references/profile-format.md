# Voice profile format

The profile folder (`$REPLY_LIKE_ME_DIR`, or `~/.config/reply-like-me/`) holds
everything personal. Never commit it, paste it into a shared doc or copy it into
the skill.

| File | Holds |
| --- | --- |
| `voice.md` | The voice: rules, by-situation table and check list. Read on every draft. |
| `chat-examples.md` | 40 to 80 real chat messages, grouped by situation, plus 10 to 20 emails in their own section if email was scanned. |
| `docs-examples.md` | How they write at length, plus 10 to 15 real excerpts. Used only for long posts and announcements, never to write documents. Optional. |
| `people.md` | Which terms of address and nicknames the user has used with each person and group, with counts. Holds names, so it is the most private file. |
| `stats.md` | Output of `scripts/voice_stats.py`. Evidence for the numbers in `voice.md`. |
| `corrections.md` | Rules learnt from edits the user made to drafts. Wins over everything else. |
| `setup-log.md` | When setup ran, which sources it read, and what it left out, with reasons. |
| `drafts/` | Every draft handed over, with where it was going and its status, until it has been compared with what was sent. See [learning.md](learning.md). Deleted after 30 days. |
| `raw/` | Collected messages and excerpts. Delete after setup unless the user wants to keep them for a refresh. |

## voice.md

Keep it under about 2,000 words, tables included. Every claim should come from the user's own
text: a count from `stats.md` or a quote. Use these sections:

1. **Owner.** Name, the setup date, and where the evidence came from ("3,200
   Slack messages, Oct 2023 to Oct 2026; 46 Google Docs"). If sources differ
   (team chat against email to outsiders), say how.
2. **Rules still in force.** General writing rules that still apply to text sent
   as them (for example "no em dashes"), and which ones their voice overrides.
3. **The voice in brief.** Length, greetings, sign-offs, the words they use and
   the ones they avoid (for example "yep, never yes"), phrases they reach for,
   mechanics (full stops, capitals, apostrophes, ellipses, dashes, spelling),
   emoji and laughter, swearing and where it is allowed. Give slang as a
   table: word, count, where it goes (DMs or channels, start or end of a
   message) and what it does, from "Words in context" in `stats.md`.
   Give emoji as a table: emoji, how often, and what it means when they use it
   in a message and as a reaction, from the "Emoji in context" section of
   `stats.md` and the reactions Collector.
4. **By situation.** A table: quick ask, helping someone, asking, delegating,
   bad news, pushing back, deciding, explaining, thanks, late reply, senior or
   outside people, moving to a call. One line each, with a quote where you have
   one.
5. **Docs in brief.** How their long-form voice differs from chat. Point to
   `docs-examples.md`.
6. **Check before you hand it over.** Four to six checks specific to them.

Give rates as numbers ("about 8 in 10 messages have no full stop at the end"),
not as "often". A model copies a rate better than an adverb.

## Examples files

- Copy messages exactly, typos included.
- Replace other people's names with `<name>`. Keep public channel names.
- Leave out anything about health, HR, pay, family or someone else's private
  matters, and any credential, account number or personal detail.
- Join messages sent in a quick burst with ` / `.
- Group by situation, using the same headings as the table in `voice.md`.
- Leave out anything that reads as AI-written (see setup step 4).

## people.md

A table of person, handle, terms used with them (with counts), nickname and
last used, sorted by count, then a table of groups and channels. Record only
what the user wrote to each person. Never record or infer anyone's gender.
Drafting uses a term only with people listed for it 3 or more times. The user
can edit the file to add, remove or correct anyone.

## corrections.md

One line per lesson, newest first: the date, how many edits showed it, the
rule, and the change that taught it. Lessons seen three times move into
`voice.md` (see [learning.md](learning.md)).

```markdown
- 2026-03-14 (seen 2): Agreement is "Yep" or "Agree with <name>", never "That makes sense". ("That makes sense" => "Yep", #team)
```

## setup-log.md

The date setup ran, the sources chosen, the date range covered, the message counts by slice, the
docs read, and the docs and messages left out, each with a one-line reason. A
refresh reads this file to know where the last run stopped.
