# Learning from edits

The profile improves each time the user changes a draft before sending it. The
skill logs each draft, later finds what the user actually sent, and turns the
differences into lessons.

All of this stays in the profile folder. Never send a draft, a diff or a lesson
anywhere.

## 1. Log every draft

Each time you hand over a draft, save it to `[profile]/drafts/` as
`YYYY-MM-DD-HHMM-[short-slug].md`:

```markdown
---
created: 2026-10-08T15:02:00+11:00
where: slack
place: "#team-helpline"
thread: "1791431246.004069"
to: "<person's handle, or the channel>"
status: open
---

<the draft text exactly as you handed it over>
```

Record the place and thread whenever you know them: without them the draft
can't be matched later. If the user edits the draft in the conversation before
sending it, save their version as `sent` straight away and go to step 3.

## 2. Find what was sent

At the start of each drafting run, and whenever the user asks to "learn from my
edits", check every draft with `status: open`:

1. Search the place for messages from the user after `created`, in the same
   thread if there is one. Take the first message in the next 24 hours that
   answers the same thing. Read only.
2. If it was sent by an assistant (a "Sent using ..." footer), mark the draft
   `status: sent-by-assistant`. There is nothing to learn.
3. If you find nothing after 3 days, mark it `status: unsent` and move on. An
   unsent draft may itself be a lesson: if the user often drops drafts of one
   kind, note that.

## 3. Compare and learn

Save the sent text next to the draft, then run:

```
python3 -I scripts/draft_diff.py [draft file] [sent file]
```

- **Similarity 0.95 or more:** the draft worked. Mark it `status: kept`. Add
  nothing.
- **Similarity under 0.3:** the user wrote their own reply. Compare the two as
  wholes (length, tone, what they chose to say) and write at most one lesson.
- **Anything between:** read each change and ask what it says about the voice,
  not about this one message. Changed facts, names or dates aren't voice
  lessons: skip them.

Write each lesson as a rule another draft could follow, with the evidence:

```markdown
- 2026-03-02 (seen 1): Drops "Thanks" before "nice catch" with peers. ("Thanks Sam, nice catch" => "Nice catch Sam", #team-helpline)
```

Before adding a lesson, look for one that already says the same thing. If you
find one, raise its `seen` count and add the new evidence instead of writing a
second line. If a new edit contradicts an old lesson, keep the newer one and
note the change.

Then mark the draft `status: learnt`.

## 4. Fold lessons into the voice

`corrections.md` wins over `voice.md`, so keep it short:

- A lesson `seen 3` or more is part of the voice. On the next refresh, or when
  the user asks, move it into the right section of `voice.md` and delete it
  from `corrections.md`. Update the examples file if the lesson changes one of
  them.
- Tell the user what moved, in one line each.

## 5. Tidy up

Delete drafts that are `learnt`, `kept`, `unsent` or `sent-by-assistant` and
more than 30 days old. They hold message text, so don't keep them longer than
the lessons need.
