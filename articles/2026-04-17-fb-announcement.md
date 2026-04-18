Ever read a book where something didn't quite hold together? The butler couldn't have done it—he was across the country. The hero "changes" but nothing in the text actually shows it. Character motivations evaporate in the last act. You don't need to be a critic—you can just tell.

Writers have been trying to formalize what makes a story work for over a century (three-act structure, the Hero's Journey, Save the Cat, Dramatica). These tools are mostly checklists. They help you *plan*. They can't actually *check* whether your finished story matches what you said you were writing.

That's what I'm building. Not an AI that writes stories for you. A machine that reads a story's skeleton—who does what, who knows what when, who kills whom, who forgives whom—and tells you whether the structural claims actually hold up against the evidence on the page.

So far I've translated four stories into this machine-checkable form: *Oedipus Rex*, *Macbeth*, *The Murder of Roger Ackroyd*, and *Rocky*. Each one pressured the theory in a different way, and the theory pushed back.

Concrete example from this morning: Claude (the AI) read the machine's analysis of *Rocky* and pointed out the machine was using too narrow a rule to classify the kind of pressure driving the story. I wrote the fix. Now the machine agrees with Claude, and Claude agrees with the story. That three-way loop — **story pressures theory, theory pressures code, code pressures theory back** — is what I'm doing every session.

This is a ~20-year project, honestly. The big AI companies will probably build end-to-end story-writing tools first ("AI, write me a novel"). This one is betting the opposite way: structural correctness should be mechanical and checkable, but what a story *feels* like—tone, texture, meaning—stays human. Different niche.

Repo just went public today: https://github.com/brazilofmux/story

The reasoning-over-time is all preserved—19 design sketches, ~570 tests, mistakes and corrections left in place as an editorial record. If someone in 2030 wants to think seriously about this problem, everything's there, including the arguments I lost.

Not seeking contributors. Not seeking funding. Just making the work visible.
