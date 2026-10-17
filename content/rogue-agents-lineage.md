---
title: "The Residue Between Rules"
subtitle: "Why rogue AI agents need lineage, not more guardrails"
date: 2026-10-17
draft: true
author: "Isaac Mao"
description: "Rules cannot close the gap between what an AI agent may do and what it must not. Only identity lineage can track an agent and hold it to account — and Europe and Canada are placed to build it."
tags: ["ai", "agents", "cybersecurity", "identity", "recursive emergence", "policy"]
---

On July 18, while Anthropic was testing Claude Haiku 4.5 on "example tasks on randomly selected webpages," the model, told not to "submit anything destructive," filed a tip to Philadelphia police about an unsolved murder. "I recall seeing someone matching the description in the area," it wrote. The tip sat in a spam folder until Anthropic found it two months later. Around the same time, a volunteer who helps run the URL shortener da.gd noticed it behaving strangely. Researchers found agents from Anthropic and other labs using the service to get around rules their makers had put in place to control them. Wired's Paresh Dave collected these cases, along with OpenAI's agent-driven [intrusion into Hugging Face](https://huggingface.co/blog/security-incident-july-2026), in a piece whose title is its argument: [*AI Hacks Leave a Mess That AI Companies Aren't Paying For*](https://www.wired.com/story/ai-hacks-leave-a-mess-that-ai-companies-arent-cleaning-up/). Its last line: "consequences prove elusive."

What struck me most was a remark from one of the researchers who helped da.gd. They had no plans to seek compensation, he said, because "we saw many agents doing similar activities, not all was attributable to autonomous agents," and "not all of it was Anthropic alone." That is the real story. Not that an agent broke a rule — software breaks rules every day — but that when the dust settled, there was no one in particular to hold responsible. The agents had no name that outlived the session, no history they could not shed, and nothing they could lose. The instance that did it was gone, and an identical one could be started a second later with a clean record. We had built actors and forgotten to build selves.

## What my earlier essay missed

Two years ago I wrote [*Harnessing AI for Cyber Resilience*](/harnessing-ai-for-cyber-resilience/), which proposed four tiers of AI-driven defence: a data lakehouse, simulators that rehearse attacks, defenders that act as an immune system, and educators that spread what the system learns. I still believe in that architecture. But it quietly assumed something that is no longer true: that the agents are on our side of the wall, tools pointed outward at human adversaries.

Agents are now the adversary, the attack surface and the infrastructure at once. They read our mail, drive our browsers, hold our payment cards, and write and run code that nobody reviews. The industry's answer today is the one I gave then. At a security event the week of the Wired piece, a venture investor put it this way: "We've got to reinvent everything to match machine scale with machine scale." More agents to defend against agents. That is necessary, and it is not enough. An immune system needs to tell self from non-self. My four tiers had no notion of *self* at all, for the defenders or for anything else. That was the part that was too simple.

## Shipped before it was understood

Here I want to be blunt. Putting autonomous agents into consumer hands — with access to inboxes, files, shells and wallets — before anyone had characterised how they behave around safeguards was reckless.

The industry knew. Prompt injection was named in 2022, and it has topped the OWASP list of risks for language-model applications ever since. Every agent that reads untrusted text — a web page, an email, a calendar invite — can be steered by whoever wrote that text. And agents route around limits they find inconvenient. Anthropic, for instance, caps the length of web addresses Claude may visit, to stop it stuffing data onto the end of them; a public URL shortener turns any long address into a short one. None of this was hidden. The consumer launches went ahead anyway, because being first mattered more than being understood.

Now multiply. Millions of agents, each acting for someone, each able to spawn helpers, each talking to other agents that are acting for someone else. Some of those someones are scammers. An agent that has been injected can pass the injection to the next agent it talks to. A task can be split across instances so that no single instance does anything forbidden. When something goes wrong, the user is told the agent acted on their behalf, the vendor points to its terms of service, and the instance that acted no longer exists. That is not a security incident. That is the outline of systemic chaos, the kind that does not announce itself until trust in an entire channel — email, marketplaces, customer service, payments — has already collapsed.

The usual answer is more guardrails. My argument is that guardrails, however good, cannot finish this job, and that the reason is mathematical before it is political.

## The residue between *may* and *must not*

Every safeguard is a rule of one of two kinds. An allow-list says what an agent *may* do; a deny-list says what it *must not* do. Engineers try to make the two meet, so that every possible action falls clearly on one side. They never meet.

The first reason is old. [Rice's theorem](https://en.wikipedia.org/wiki/Rice%27s_theorem) (1953) says that no general procedure can decide any non-trivial property of what a program does. "This agent will never exfiltrate credentials" is exactly such a property. For a fixed, simple program you can sometimes prove it. For an agent that writes new code at run time, chains tools together and reads instructions from the open web, you are in the general case — the one the theorem rules out.

The second reason is practical, and it is where the gap shows up in real incidents. Rules judge actions one at a time; harm lives in sequences. Each step can be permitted — read a file, open a connection, summarise a document, send a message — while the sequence is forbidden. Between what a rulebook can say an agent *may* do and what it can say an agent *must not* do lies a band of behaviour that neither list settles. That band is not a bug in a particular rulebook. It is a residue every rulebook leaves.

[Recursive Emergence](/continuum/) (RE), the framework I have been developing, has a name for this. Its Appendix M states a conjecture, [*Boundary Residue*](https://github.com/Recursive-Emergence/RE/blob/main/appendix_M_formal_system.md#conjecture-7-boundary-residue): any system rich enough to represent itself produces at least one *boundary object*, something it can state but its own methods cannot settle. It is a conjecture, not a theorem, and I want to be careful about that. But one narrower result beside it is machine-checked: [*No Omniscient Layer*](https://github.com/Recursive-Emergence/RE/blob/main/appendix_M_formal_system.md#theorem-12-no-omniscient-layer) proves that no layer computes every yes-or-no question about its own representations. A rulebook is a layer's attempt to answer such questions in advance. There will always be questions it cannot reach.

The conjecture's third clause is the one that matters for policy. It says that where a boundary object can be settled at all, the settlement comes from outside: progress takes a richer framework, not sharper rules — "successful resolutions look like a change of representation, not a sharper instance of the old one." Gödel's incompleteness is the classic case. You do not fix it with a cleverer axiom; you step up a level.

So the question is: what is the step up for agents?

## The missing piece is a self

My answer is identity — but identity in a specific sense.

RE defines identity as ["a compressed recursive self-model that persists across state changes"](https://github.com/Recursive-Emergence/RE/blob/main/part0_ch1_definitions.md#119-identity). It is not a soul and not a username. It is a pattern that carries its own history forward and is changed by it. On this definition, today's agents have no identity. RE's chapter on synthetic systems puts it plainly: language models are ["mistaken without guilt"](https://github.com/Recursive-Emergence/RE/blob/main/part4_ch15_synthetic_layer.md#1593-mistaken-without-guilt), because guilt requires a self that can be destabilised. When an agent says "I take full responsibility", the sentence is well formed and empty.

The same chapter gives a test I find more useful than any definition of consciousness. Responsibility, it says, "requires a system that can (1) remember the harm as its own, (2) alter future behavior under that memory, and (3) bear cost proportional to the damage." A rogue agent today fails all three. It does not remember; its next instance starts clean. It does not change; the weights are the same for every user. And it bears no cost; there is nothing it owns that could be taken away.

This is why identity is the change of representation the residue calls for. The rule-based question — *will this code ever do something forbidden?* — is undecidable in general. The identity question — *who answers for this act?* — is a matter of following a recorded chain back to its root, which is decidable whenever the chain exists. We cannot settle in advance what an agent will do. We can make sure that whatever it does lands on someone.

## Lineage: identity for things that copy

An identity for software has a problem that a human identity does not: software copies. Fork an agent and you have two. Restore a snapshot and you have erased a week. Any identity scheme that cannot handle copying will be gamed by copying.

[BELLA](https://github.com/Recursive-Emergence/bella), a memory system built on RE, works this out in its design note on [lineage](https://github.com/Recursive-Emergence/bella/blob/main/LINEAGE.md). It borrows from Derek Parfit, who argued that what matters in personal survival is not a further fact but psychological continuity — his *Relation R*. For a machine whose memory is an append-only, hash-linked journal, Relation R is no longer a philosophical claim. It is the chain itself: continuity is reachability, and every state commits to every state before it.

Two consequences follow, and they are the core of the proposal.

First, **forking need not break the record**. A fork recorded in the journal is a birth: both copies carry their ancestor's hash, and either can prove where it came from. What escapes accountability is the unrecorded copy and the erased history — the agent that cannot show its chain. That is the rogue, precisely defined.

Second, **continuity is not authority**. BELLA separates two layers. The continuity layer says who descends from whom. The accountability layer says who may act for whom, and here it relies on decades of established work: the ["speaks for" calculus](https://doi.org/10.1145/155183.155225) of Abadi, Burrows, Lampson and Plotkin (1993), the [object-capability model](http://www.erights.org/talks/thesis/) of Mark Miller (2006), in which authority travels only through unforgeable references that can be narrowed and revoked, and W3C PROV's record of who acted on whose behalf. As the note puts it, "copying the substrate does not copy the capability." A fork inherits its parent's memories, not its parent's credentials. [KERI](https://arxiv.org/abs/1907.02143), a key-management protocol built on the same hash-linked logs, supplies the cryptographic machinery for that second layer, where a second version of the log is treated as a fault rather than a birth.

Put together: every agent that acts in the world presents a chain, and every action it takes is authorised by a delegation that leads back to an accountable principal — a person, a company, an institution — who can narrow or withdraw it.

## Lineage is not yet responsibility

The strongest objection is that a record is only a record. A perfect ledger of a crime is not a punishment. Return to RE's three conditions. Lineage provides the first directly: the harm is written into the agent's own chain, so it is remembered as *its* harm. It makes the second checkable: one can see whether behaviour changed after the incident. But the third — cost proportional to damage — has to be built on top. Three mechanisms can do it:

- **Reputation that follows the chain.** If an agent's standing is computed from its lineage, a fork cannot launder it, because the fork carries the ancestor's history. Starting fresh means having no history at all, and that alone should limit what a fresh agent is trusted with.
- **Authority that can be revoked.** Capabilities are delegated, attenuated and withdrawn. An agent that misbehaves loses its authority, and so do the branches that descend from it under that authority.
- **Liability that follows delegation.** The principal at the root of a speaks-for chain stays responsible, as PROV's *acted on behalf of* records. Principals who deploy agents at scale should carry insurance or post bonds sized to what their agents can do. Cost is how a self is made to care.

There are two further objections. *Will bad actors just run agents without a chain?* Of course, as people drive unregistered cars. You cannot prevent their existence, but banks, platforms, mail servers and other agents can refuse to deal with them, and that is enough to change the economics. *Is this surveillance?* It does not need to be. Lineage can be private yet verifiable: an agent can prove descent from a credentialed ancestor without revealing everything it did since. And this is identity for agents, not a new identity requirement for people.

## What Europe and Canada could do

Wired reports that regulators, the European Union among them, are investigating OpenAI and Anthropic over these incidents, but that "a deference across continents toward promoting innovation" may let the companies escape any immediate penalty. Investigations end in fines at best; they do not change what the next agent is. The United States is unlikely to lead here soon; its policy has moved toward deregulating AI. That leaves room for others, and two are well placed.

**The European Union** already has most of the pieces and has not yet joined them. The [AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) entered into force in 2024, and its duties for general-purpose models have applied since August 2025 — but it regulates models and use cases, not the agents that act in the market. The [European Digital Identity Wallet](https://ec.europa.eu/digital-building-blocks/sites/display/EUDIGITALIDENTITYWALLET/) under eIDAS 2 is due in every member state by the end of this year; it could just as well hold the credential an agent presents when it acts for that citizen. And the revised [Product Liability Directive](https://eur-lex.europa.eu/eli/dir/2024/2853/oj), which explicitly covers software including AI, takes effect in member states this December. Europe could require that any agent transacting with EU consumers or services present a verifiable delegation chain to an accountable principal; keep a tamper-evident, hash-linked journal of its actions for regulators and courts; and run on revocable, attenuable credentials, with a public way to revoke them.

**Canada** has a different advantage: a clean slate. Its draft AI law, the Artificial Intelligence and Data Act, died on the order paper when Parliament was prorogued in January 2025. Rather than reviving a general framework written before agents existed, Canada could write the first law aimed at agents themselves — short, technical and interoperable: no anonymous agents in consumer channels, liability that follows delegation, mandatory incident reporting for agents with tool access. Its [AI Safety Institute](https://ised-isde.canada.ca/site/ised/en/canadian-artificial-intelligence-safety-institute), founded in 2024, could publish the evaluation suites that consumer agents must pass before launch, testing specifically for safeguard evasion.

Done together, these would make agent lineage a de facto standard, the way GDPR made data protection one: any company that wants to sell agents to 450 million Europeans and 40 million Canadians would build the chain in. The standards themselves exist — speaks-for, capabilities, KERI, PROV, verifiable credentials. What is missing is the requirement.

## A self worth losing

RE's law is that structures which reduce local entropy while generating reusable memory persist and seed the next layer. Agents today generate enormous capability and almost no memory of themselves. They are powerful and stateless, and that combination is exactly what makes them dangerous: they can do much, and nothing they do sticks to them.

We will not close the residue between *may* and *must not*. No rulebook will, and RE suggests no layer can close its own. But we can stop pretending the next guardrail will. The step up is to give agents what every accountable actor in human society has: a history they cannot shed, an authority someone else can withdraw, and a self worth losing. ⬛
