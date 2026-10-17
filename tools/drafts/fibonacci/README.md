# Fibonacci spiral drafts (not published)

Concept drafts for showing Recursive Emergence as a Fibonacci spiral. Kept for later; the site uses the ring map (`tools/make_continuum.py`).

- `fib_sketch.py` → `sketch.svg` / `sketch.png`: the nine layers as squares 1, 1, 2, 3, 5, 8, 13, 21, 34. Hard to read, because the inner layers come out 1/34 the size of the outer one and need long callouts.
- `emblem.py` → `emblem.svg`, shown with its caption in `emblem.html` / `emblem.png`: a label-free emblem of the law (only the numbers 5–34, with the words in the caption). Cleaner, but still not as easy to read as the rings.

Why the spiral fits RE as a concept: the sequence starts 0, 1; each term is the sum of the two before it, with every square kept; ratios converge on φ from any positive start (always approaching, never arriving); removing the largest square from a golden rectangle always leaves a smaller golden rectangle (a remainder that never vanishes); and the spiral never closes. Caveat: RE's layers are not literally Fibonacci-sized, so present it as an emblem, not a model.

Regenerate: `python3 emblem.py emblem.svg`, then screenshot `emblem.html` with headless Chrome.
