# Setup: learn how the user writes

Study what the user has written, in the places they choose, then write their
voice profile. A refresh is the same process limited to the time since the last
run (see `setup-log.md` in the profile), merged into the existing profile.

Setup reads private messages. Read only: never post, send, edit, comment or
react anywhere. Run it only in a session on the user's own computer, never in a
cloud or remote VM, and never write the profile inside a repo.

Paths to `scripts/` and `references/` are relative to this skill's folder.

## What it needs

- At least one source the user can read through a connected tool, or files
  they point you at. See [sources.md](sources.md) for each source.
- A shell with Python 3, for `scripts/voice_stats.py`.
- Subagents, to study slices in parallel. Without them, do the slices one after
  another yourself.

### Subagent settings

Each spawn below names a role. Use that role's settings for the tool you're
running in. If a listed type isn't available, use the closest type that meets
the Needs column.

| Role | Needs | Claude Code | Cursor |
| --- | --- | --- | --- |
| Collector | Reads one source, writes only to the profile's `raw/` folder | `subagent_type: general-purpose`, told it may write only to `raw/` | `subagent_type: generalPurpose`, told it may write only to `raw/` |
| Tester | Reads the profile, drafts text, never writes or sends | `subagent_type: general-purpose`, told not to edit or send | `subagent_type: generalPurpose`, `readonly: true` |

Leave `model` unset for every subagent so each one runs on the session's
model. Run Collectors in the background where the tool allows it.

## Step 1. Agree the sources and scope

1. Work out which sources you can read. Check the tools you have against the
   table in [sources.md](sources.md). Don't call a tool just to test it.
2. Ask the user which to scan, as a multiple-choice question (or a numbered
   list they answer by number, if the tool has no such prompt), listing only
   the sources you can read, plus "files I'll point you at". Give
   each a one-line note on what it adds: chat shows their quick voice, email
   their voice with outsiders, docs their long-form voice. Recommend at least
   one chat source and one long-form source, because people write differently
   in each.
3. In the same message, ask:
   - their name as it should appear in the profile
   - roughly when they started using AI to help write, so later text gets
     stricter checks ("not sure" means check everything)
   - anything to leave out (a channel, a mailbox folder, a period, a topic)
4. For each chosen source, find their identity there (user ID, email address
   or account) and the date of their oldest message or doc you can reach.

## Step 2. Collect chat and email

For each chosen chat or email source, split the time from the oldest message
to today into slices: up to six for the busiest source, fewer for the others.
Keep the total number of Collectors across all sources to about ten. Spawn them
all at once with this brief, adding that source's notes from
[sources.md](sources.md):

> Collect messages written by [name] ([identity in this source]) in [source]
> between [start] and [end], for a study of how they write. Read only: never
> post, send, edit or react.
>
> [Source notes: how to find only their messages, page through them and tell
> the kinds of place apart.]
>
> Aim for about 400 messages, spread across every month in the slice rather
> than only the first pages, and balanced across the kinds of place (for chat,
> about half direct messages and half channels). Also read three or four
> conversations in full, to see how they open and close a reply.
>
> Append each message to `[profile]/raw/[chat or email]-[source]-[n].txt`, one
> per line, as `DATE | KIND | text`. KIND is `DM` for direct and group chats
> (no names), `CHANNEL(channel name)` for channels and spaces, and
> `EMAIL(internal)` or `EMAIL(external)` for email. Never put a person's name
> in KIND.
> Write newlines inside a message as `\n`. Copy the text exactly, typos
> included. For email, keep only the text they wrote: cut quoted replies,
> forwarded text and signatures.
>
> Leave out, and do not save (skip the whole message):
> - any message with a footer saying an assistant sent or wrote it ("Sent
>   using ...", "Drafted with ..."), and any message that reads as AI-written
>   (em dashes, tidy paragraphs, words like delve, robust, seamless,
>   leverage). List these at the end of your report with the date and first
>   few words.
> - automated messages, calendar replies, slash commands, bare links and
>   pasted logs or code
> - anything about health, HR, pay, family or someone else's private matters,
>   and any credential, account number or personal detail.
>
> Then report on how they write, quoting their own words: openers and
> greetings; closers and sign-offs; signature words, slang and swearing with
> rough counts; capitals, punctuation, apostrophes, ellipses, dashes, typos,
> message length and whether they split thoughts into bursts; emoji and
> laughter; how their tone changes with peers, seniors, outsiders and people
> asking for help; how they explain things and decide; what they never or
> rarely do; and 10 to 15 short example messages across situations. Under
> 1,500 words, plus your message counts by kind of place.

### Reactions

Emoji reactions say as much as emoji in messages: "seen it", "approved",
"thanks". Where the source can find messages the user reacted to (in Slack, the
`hasmy::emoji:` filter), spawn one more Collector for the last six months:

> For each emoji in [the top 15 from the messages collected so far, plus
> common reactions: +1, thumbsup, white_check_mark, eyes, joy, heart, clap,
> raised_hands, fire, tada, 100], search messages [name] reacted to with it,
> up to 100 per emoji. Read only. Record the count and, for each message, a
> category: thanks or work reported done, request or review, question,
> announcement, joke, bad news, praise of someone, other. Save
> `EMOJI | DATE | DM or CHANNEL | category` lines (no text, no names) to
> `[profile]/raw/reactions-[source].txt`. Return a table: emoji, count, what
> they use it for.

Skip this where the source has no such search.

### Terms of address

People often address some people differently from others: "mate" to some,
a first name to the rest. Find the user's terms of address and nicknames from
the Collector reports (for example mate, dude, love, hun, bro, fellas), then
spawn one Collector:

> For each term in [terms], search messages [name] wrote containing it, with
> enough context to see who it was addressed to: the other person in a 1:1
> chat, or the person mentioned or replied to in a channel. Skip uses that
> don't address anyone ("my mate from school") and record "unclear" where you
> can't tell. Note any nickname they use for a person. Never guess or record
> anyone's gender. Write `[profile]/people.md` as profile-format.md describes.

Tell the user this file holds colleagues' names and stays in the profile.

## Step 3. Collect long-form writing

For each chosen docs source, split the docs into up to three periods, with the
last one starting at the date the user gave for AI help. Spawn one Collector
per period, adding that source's notes from [sources.md](sources.md):

> Study documents that [name] ([identity]) owns and wrote themselves in
> [source], created between [start] and [end]. Read only: never edit, comment
> or share.
>
> [Source notes: how to find docs they own and read them.]
>
> Search with several queries (by owner, by date, and by words like proposal,
> RFC, plan, analysis, incident, design, strategy, options). Read up to 15
> that qualify.
>
> Leave out: meeting notes of any kind (agendas, minutes, 1:1s, retros,
> standups, workshops, AI meeting notes), templates they barely filled in, docs
> mostly written by others, HR, performance or personal docs, and docs or
> sections that read as AI-drafted (em dashes, "It is not X. It is Y.", words
> like underscores, fosters, delve, robust, seamless, closing summaries). [Last
> period only:] Be strict: this period is after they started using AI to
> write, so keep a doc only if it reads as their own hand. A handful is fine.
>
> Save a few verbatim paragraphs from each doc you keep, under its title and
> date, to `[profile]/raw/docs-[source]-[n].txt`.
>
> Report on their long-form voice with short verbatim quotes: structure and
> openings; sentences, punctuation and spelling; signature words and how they
> differ from chat; how they argue, decide, hedge and ask for input; tone with
> different audiences; what they never do; and 5 to 8 excerpts. Under 1,200
> words. Then list each doc you kept, kept in part or left out, with a one-line
> reason.

For files the user points you at, read them yourself or with one Collector,
using the brief that fits (chat export or documents).

## Step 4. Check the collection

When the Collectors report back:

1. Run `python3 -I scripts/voice_stats.py --words [slang and stock phrases
   the Collector reports named] [profile]/raw/chat-*.txt
   [profile]/raw/email-*.txt` (whichever exist) and save the output as
   `[profile]/stats.md`.
2. Read the em dash messages listed at the end of `stats.md`, and search the
   raw files for assistant footers ("Sent using", "Drafted with"). Remove any
   that are AI-written, then rerun the script.
3. Use the "Words in context" section to say where each word belongs: DMs
   or channels, the start or end of a message, and whether use is rising or
   falling.
4. Check the Collectors' claims against `stats.md`. Where a report says
   "always" or "usually", use the counted rate instead.

## Step 5. Write the profile

Write `voice.md`, `chat-examples.md`, `docs-examples.md` and `setup-log.md` as
[profile-format.md](profile-format.md) describes, skipping any file with no
source behind it. Merge the reports: keep what several slices agree on, note
where the voice differs between sources (chat with the team against email to
outsiders), and note where it changed over time. When slices conflict, favour
the most recent unless it reads as AI-assisted.

On a refresh, merge into the existing files rather than replacing them. Fold
in any `corrections.md` lessons seen three or more times, as
[learning.md](learning.md) describes, and leave the rest of the file alone.

## Step 6. Test it

Spawn a Tester. Give it the path to this skill's `SKILL.md` and the profile
folder, tell it to follow only the Drafting section, and ask for three drafts built from the user's own work: a reply to someone
asking for help, a short pushback to a peer, and an email to an outsider or a
long announcement to a team. Never ask for a technical document, PR
or code. Ask it to list anything in the profile that was unclear or
contradictory.

Fix the gaps it finds, then show the user the three drafts. Ask what they would
change, and record their answers in `corrections.md`.

## Step 7. Tidy up

Ask the user whether to keep `raw/` for a later refresh. If not, delete it.
Tell them where the profile lives and that it is theirs to edit.
