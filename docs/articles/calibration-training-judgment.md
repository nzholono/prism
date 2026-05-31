# Calibration: Training Your Judgment

The cognitive lens in Prism isn't trying to tell you what to do. It's
trying to do something subtler — show you the gap between how confident
you feel and how often you're right.

That gap has a name: **calibration**.

## What calibration means

You are **well calibrated** if, when you say "I'm 80% sure", you're right
about 80% of the time. When you say 95%, you're right 95% of the time.
When you say 50%, it's a coin flip.

Most people — including doctors, judges, executives, professional
forecasters — are **poorly calibrated**. The most common pattern is
**overconfidence**: when people say "I'm 90% sure", they're typically right
only 70-75% of the time.

This matters because we make most decisions under uncertainty. Better
calibration means:

- You stop being surprised by predictable outcomes.
- You don't dismiss real risks ("there's no way that'll happen").
- You don't paralyze over imaginary risks.
- You can tell signal from noise about your own thinking.

## How Prism helps you calibrate

The decision journal is built around three small acts that, repeated,
train calibration:

1. **State your confidence in advance.** Numbers (0-100), not vibes. Before
   you know the outcome.
2. **State what you expect to happen.** Specific enough that you'll
   recognize whether it matched.
3. **Come back and review.** Did it work? What did the bias detectors
   flag? Were they right?

`prism-cli stats --calibration` then surfaces patterns:

- Your average confidence.
- Your average confidence when outcomes went well vs. went poorly.
- Which biases get flagged most often.
- Whether bias-flagged decisions go worse than unflagged ones.

## What good calibration data looks like

After 10–20 reviewed decisions, you'll usually see one of three patterns:

**Pattern 1: overconfident** (the most common)

> Average confidence: 78. When outcome went well: 76. When outcome went
> poorly: 84.

You were *more* confident on the decisions that went wrong. Classic
overconfidence — high certainty tracks with bad outcomes.

**Pattern 2: underconfident** (less common; more often among people who've
been criticized a lot)

> Average confidence: 52. When outcome went well: 49. When outcome went
> poorly: 57.

You're less sure of yourself when you're actually right. Trust your
judgment more, even if it feels less comfortable.

**Pattern 3: well calibrated**

> Average confidence: 65. When outcome went well: 70. When outcome went
> poorly: 55.

Higher confidence tracks with better outcomes. You can use your gut as
information — when you feel sure, you usually are.

## Why bias flags matter for calibration

The 15 bias detectors aren't trying to convince you you're wrong. They're
asking *would you make this decision the same way if you noticed this
pattern in your thinking?* Often, yes. Sometimes, no.

If you log enough decisions and review enough outcomes, you'll see
whether the bias flags **predict** worse outcomes. If they do (and they
usually will), they're calibration data — you've discovered which
patterns in your own reasoning lead you wrong.

That's worth more than most self-help advice.

## The rules of better calibration

From [Tetlock's superforecaster research](https://www.goodreads.com/book/show/23995360-superforecasting):

1. **Think in probabilities, not certainties.** "I'm 75% sure" is more
   useful than "I think so".
2. **Separate the bet from the outcome.** A good decision can have a bad
   outcome; a bad decision can have a good outcome. Judge the decision
   on what you knew at the time.
3. **Decompose.** Break a complex question into sub-questions and reason
   about each.
4. **Update slowly on new evidence — but do update.** Don't refuse to
   change your mind; also don't flip on every news cycle.
5. **Look at base rates first.** "How often does X normally happen?"
   before "What do I think will happen here?"
6. **Notice when emotions are doing the reasoning.** Fear and excitement
   both inflate confidence in the direction they pull.

## Practical setup for using Prism for calibration

**Week 1.** Log every non-trivial decision. Don't worry about quality —
build the habit.

**Week 2.** Review your week. Did any decisions resolve? Run
`prism-cli decide review <id>` for each.

**Week 4.** First calibration check: `prism-cli stats --calibration`.
You probably don't have enough data yet to see clear patterns. That's
fine. Keep going.

**Month 3.** You probably have 20+ reviewed decisions. Patterns start
showing up.

**Month 6.** Your calibration improves measurably. Not because Prism
told you anything magical — but because the practice of stating
confidence explicitly, reviewing outcomes honestly, and looking at
patterns is exactly what professional forecasters do to get better.

## Further reading

- **Philip Tetlock, *Superforecasting: The Art and Science of
  Prediction*** — the gold standard.
- **Daniel Kahneman, *Thinking, Fast and Slow*** — the source for most of
  the biases in Prism.
- **Annie Duke, *Thinking in Bets*** — applies these ideas to everyday
  decisions.
- **Julia Galef, *The Scout Mindset*** — short, practical.

---

*This article is reference material. The point is to use Prism's tools
on your own decisions — that's where the value is.*
