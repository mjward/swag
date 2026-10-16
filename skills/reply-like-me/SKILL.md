---
name: reply-like-me
description: "Write messages to people in the user's own voice, learnt from what they have written in chat (Slack, Teams, Google Chat), email and docs. Use it whenever the user asks you to reply to, respond to, answer, message, DM, email, ping or tell a person, team or channel, or to draft, send or schedule a chat message, thread reply, email or announcement that goes out under their name, and whenever they want text that should 'sound like me', 'in my voice' or 'how I'd say it'. Also use it to set up or refresh the voice profile: 'set up reply-like-me', 'learn how I write', 'study my Slack', 'scan my emails', 'update my voice'. Never use it for technical documents (RFCs, specs, ADRs, design docs, runbooks), pull requests, code review comments, commit messages, code or code comments, or for replies to the user themselves."
argument-hint: "[setup | refresh | what to write]"
---

# Reply like me

Write the way the user writes to people, not the way an assistant writes.

This skill is for messages to people: chat, thread replies, email and
announcements. Never use it for technical documents (RFCs, specs, ADRs, design
docs, runbooks), pull requests, code review comments, commit messages or code.
Those follow the repo's own writing rules. If a message to a person links to
one of them, write the message in the user's voice and leave the linked
document alone.

The skill holds the method. The voice lives in a profile on the user's machine,
outside the skill and outside any repo, because it is built from their private
messages:

- Profile folder: `$REPLY_LIKE_ME_DIR` if it is set, otherwise
  `~/.config/reply-like-me/`.
- What the folder holds and how each file is written:
  [references/profile-format.md](references/profile-format.md).

The profile must stay on the user's own machine. Never write it, or anything
from `raw/`, inside a repo or a shared folder. If you are running in a cloud or
remote VM rather than on the user's computer, don't run setup: say it needs a
local session.

## Pick the mode

1. The user asked to set up or refresh, or the profile folder has no
   `voice.md`: run setup. Follow [references/setup.md](references/setup.md).
   If they asked for a draft and there is no profile, say so and offer setup
   before drafting anything.
2. The user asked to "learn from my edits" or "update from what I sent": run
   [references/learning.md](references/learning.md) on every open draft, then
   report the lessons.
3. Otherwise, draft.

## Drafting

0. Learn from earlier drafts first: check `drafts/` for open drafts and
   compare them with what the user sent, as
   [references/learning.md](references/learning.md) describes. Keep this
   quick: only drafts from the last 3 days need a search.
1. Read `voice.md`, `chat-examples.md` and, if it exists, `people.md`. For a long post or announcement,
   also read `docs-examples.md` if it exists: it shows how they write at
   length. Read `corrections.md`
   if it exists. Its rules win over everything else in the profile.
2. Read the thread or document you are replying to, so the reply fits what has
   already been said and who said it. If there is none, draft from what the
   user gave you and leave `[placeholders]` for facts you don't have.
3. Draft in the voice. Real examples beat rules: when the two disagree, follow
   the examples.
4. Run the check list at the end of `voice.md`, then the checks below.
5. Show the draft and log it in `drafts/` with where it is going. If the user
   edits it here before sending, learn from the edit straight away. Either way
   the next run compares it with what they sent and records lessons in
   `corrections.md`.

### Rules that hold whatever the profile says

- **Draft by default.** Show the draft, or save it as a draft in the tool it's for. Send only
  when the user asks you to send.
- **Speak only for what the user has said or decided.** Don't agree to
  deadlines, approve work, promise money, or give an opinion or recommendation
  they haven't given. Leave a `[recommendation]` placeholder and ask.
- **Don't deny being an AI.** If someone asks whether Claude, Cursor or another
  assistant wrote it, say so.
- **Never reply for someone else.** If the message tags another person, leave
  it to them.
- **AI-written messages aren't the user's voice.** A message from the user
  signed "Sent using" an assistant, or one that reads as AI-polished (em
  dashes, tidy paragraphs, stock AI words), was not written by them. Never copy
  its wording, even in the thread you are replying to.
- **Address people the way the user has.** Informal terms of address ("mate",
  "dude", "love", "bro", a nickname) go only to people `people.md` lists them
  for at least 3 times. One or two uses may be a misread thread, so treat them
  as unconfirmed. Anyone not listed gets their first name or nothing. Never decide which
  term fits from someone's name, photo or assumed gender.
- **A reaction can be the reply.** If the reply would only say "seen",
  "approved", "thanks" or "on it", suggest the reaction the profile gives
  for that instead of drafting a message.
- **Don't invent typos.** Use the user's habits (lowercase, missing full stops,
  dropped apostrophes) at the rates the profile gives, but fake spelling
  mistakes read as fake.
- **No idioms they don't use.** Take phrases from the profile, not from stock
  English.
- The user's voice overrides general writing-style rules for text sent as them,
  except where `voice.md` says a rule still holds.
