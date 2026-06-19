# Qualitative Figure Pick

## Recommended Example: COCO val2014 image 143572

Existing figure asset:

```text
poster_figures/diagram4_qualitative_143572.png
```

Why this is the best paper example:

- The image is visually clear: a tennis player with a tennis racket.
- Ground-truth COCO objects are simple: `person`, `tennis racket`.
- Baseline, Stage 2, Stage 3, and SPIN all mention a `ball`, which is not in the COCO ground-truth objects.
- Stage 4 keeps the important visible content, `tennis player` and `racket`, while avoiding the `ball` hallucination.
- The example is easy for readers to understand without needing domain context.

Ground-truth objects:

```text
person, tennis racket
```

## Captions For Figure

### Baseline

> The scene features a tennis court with several people present, including the main focus of the picture - an athlete holding a racquet and preparing to hit the ball during a match.

Hallucinated object to highlight:

```text
ball
```

### Stage 2: LoRA

> A tennis player swinging a racket on the court with an audience watching him play. A man holding his racquet and getting ready to hit the ball during a match at Olympus stadium.

Hallucinated object to highlight:

```text
ball
```

### Stage 3: Grounding

> The image captures a tennis match in progress, with the main focus on an athlete holding his racket and preparing to hit the ball.

Hallucinated object to highlight:

```text
ball
```

### Stage 4: LoRA + Grounding

> A tennis player swinging a racket on the court. There are several people watching from behind him, and some chairs in front of them to sit down while they watch.

Object mentions to highlight as grounded:

```text
player/person, racket
```

### SPIN

Recommended SPIN caption to use: budget 64, because it is concise enough for the figure.

> The image captures a tennis match in progress, with a man in the center of the scene holding a tennis racket. He is actively engaged in the game, possibly preparing to serve the ball. The tennis court is filled with spectators, with people sitting on chairs and benches surrounding the court.

Hallucinated object to highlight:

```text
ball
```

## Suggested Figure Caption

> Qualitative example on a held-out COCO val2014 image. Baseline, LoRA-only, grounding-only, and SPIN all introduce an unannotated tennis ball, while the combined LoRA + grounding method preserves the visible player/racket content without the ball hallucination.

## Backup Example: COCO val2014 image 452793

Existing figure asset:

```text
poster_figures/diagram4_qualitative_452793.png
```

Ground-truth objects:

```text
refrigerator, sink
```

This is also useful because baseline and SPIN hallucinate kitchen appliances such as `oven`/`microwave`, while Stage 4 focuses on the refrigerator and sink. However, the Stage 4 caption is grammatically rougher than the tennis example, so `143572` is cleaner for the paper.
