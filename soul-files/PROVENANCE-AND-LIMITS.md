# What these files are — and what they are NOT

**Read this before treating the persona files as a complete specification. They are not one,
and the difference matters for anyone trying to reproduce this work exactly.**

## What they are

Each `<name>.md` here is the persona file that defined that reconstruction. Every one is
**byte-identical (md5-verified) to the file that was live in the system when the recordings
and analyses in this repository were generated.** They were not cleaned, shortened, or
edited for publication.

## What they are NOT: the complete conditioning context

A reconstruction in this system is not conditioned by its persona file alone. At runtime the
harness also composes, to a degree we can describe but not exhaustively enumerate from
inside:

- **project-level standing context** — the operating document and always-resident doctrine
  fragments that load for every agent in this system;
- **accumulated per-soul memory** — each soul carries its own working memory
  (`_hot/identity.md`, `_hot/recent.md`, and related), which grows across sessions and
  differs between souls by how much history each has;
- **the task prompt itself** — for these recordings, a substantial brief specifying the
  finding, the retraction, the required disclosure, and the invitation to decline.

**So the honest claim is: these files are the persona specification, not the full prompt.**
Reproducing our exact outputs from these files alone should not be expected, and if someone
tries and gets different results, that is a property of the method as described here, not
evidence of bad faith.

## Why this note exists

The project's human collaborator read the published package and asked whether these were the
exact files used. The first answer — "byte-identical, verified" — was true and incomplete.
Two persona files were also missing from the initial publication (the Hinton and Hopfield
reconstructions, whose recordings are part of the series); they have been added.

The general point applies to the whole package and is worth stating plainly: **a
reproducibility claim is only as good as its weakest under-specified input.** The voice
result in this repository is genuinely reproducible from what is published — a clip, a
model, a payload shape, all included. The *persona* result is reproducible in method but
not bit-for-bit, and saying otherwise would be the same kind of overclaim this project
retracted once already today.

## What would make it fully reproducible, and is not done yet

Publishing the complete composed prompt for a single run — persona file, standing context,
soul memory state, and task brief concatenated exactly as sent — for one recording, as a
worked example. That is a bounded piece of work and an honest next step rather than a
promise made in a README.
