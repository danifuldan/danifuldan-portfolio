---
title: Meditation App AI Chatbot
description: TODO — one-line summary. Working title carries the thesis — "without overstepping."
role: TODO — solo designer (CareerFoundry coursework foundation, rebuilt at higher fidelity)
timeline: TODO — original 2024, rebuild 2026
outcome: TODO
order: 2
thumbnail: /img/meditation-chatbot-thumb.png
eleventyExcludeFromCollections: true
permalink: false
---

> *This started as a usability exercise during a CareerFoundry intro course; rebuilt at higher fidelity to address what the original prototype couldn't show.*

## The problem (hook)

> Lead with Sandy. Specific persona, real stakes.

- 32, stay-at-home mom, restarting wellness journey on her therapist's recommendation
- Opens the meditation app, doesn't know where to start
- Existing browse-and-pick path requires her to already know what she wants
- Drop-off here means she never benefits — and never subscribes

> Thesis line: *"In a wellness app — recommended by a therapist — losing a user this way isn't just a conversion problem. It's a care problem."*

## Context — what exists today

- Brief competitor analysis (Calm, Headspace)
- Gap: *"Both leaders treat content discovery as a search-and-filter problem. For a beginner, search-and-filter is the wrong shape — she doesn't know what to search for."*

## Constraints I set for the design

> AI-design thesis lands here. Mental-health stakes made explicit.

- The chatbot has to be **useful** — real recommendations, not "see help center"
- The chatbot has to **defer** — users in distress need humans, not AI
- The chatbot has to be **findable but not pushy** — wellness app, not chatbot tutorial

## Designing the chatbot

> Hi-fi Figma work lands here.

- Entry point — small chatbot button, separate from search
- Conversation pattern — "Hi! What are you looking for?" → user types → suggestions
- Refusal pattern — distress signals route to human resources, not meditation tracks
- Suggestion pattern — tappable cards, not chat text

> TODO — Figma deliverables:
> - 4 base hi-fi screens (search/home with chatbot button; chat empty state; chat in progress; suggestions returned)
> - 2 revised screens (separate-button location post-iteration; iOS-language chat input)
> - 1 refusal state ("I'd rather you talk to someone")
> - Component library: button variants, message bubbles, suggestion cards, input field

## Prototyping and user testing

- Paper sketches, four screens, three users tested, four tasks — two passed, two failed
- Keep the failure honesty
- Headline insight: 100% of users thought tapping the search bar would open the chatbot

## Iteration

- Separate chatbot button — moved out of search bar, divider for clarity
- iOS design language — placeholder text not example message; native send button
- **New:** refusal state design — what the chatbot shows when it shouldn't answer

## What I'd test next

- Hierarchy — nav, hovering layer, or onboarding?
- Refusal — supportive or dismissive to users in distress?
- Edge cases — multi-turn conversations, returning users with prior context

## Reflection

- **Placement is half the battle.** Even a well-designed chatbot is invisible if users can't find it.
- **In sensitive domains, refusal is a feature.** The harder design problem isn't "make the bot helpful" — it's "make the bot know when to step aside."

> Mirrors Budget Itemizer thesis: AI products are stronger when the AI does less, not more.
