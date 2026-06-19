#!/usr/bin/env python3
"""Bootstrap CIs and paired significance tests for CHAIR metrics.

This script is CPU-only. It reads the saved caption JSON files, computes
per-image CHAIRs/CHAIRi values, then writes a JSON summary and Markdown tables.

For paper numbers, use the spaCy scorer so the noun/proper-noun filtering
matches the project notebooks:

    python scripts/bootstrap_chair_significance.py --scorer spacy

If spaCy is not installed locally, use --scorer regex for a dependency-free
smoke test only. The regex scorer is useful for checking file plumbing but is
not the scorer used in the main notebook results.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np


COCO_OBJECTS = {
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
    "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "tv",
    "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
    "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
    "scissors", "teddy bear", "hair drier", "toothbrush",
}

COCO_SYNONYMS = {
    "person": [
        "man", "woman", "people", "boy", "girl", "child", "guy", "lady",
        "kid", "baby", "player", "rider", "skier", "surfer", "snowboarder",
    ],
    "car": ["vehicle", "automobile", "sedan", "suv"],
    "dog": ["puppy", "dogs"],
    "cat": ["kitten", "cats"],
    "tv": ["television", "monitor", "screen"],
    "couch": ["sofa"],
    "cell phone": ["phone", "cellphone", "smartphone"],
    "dining table": ["table", "desk"],
    "wine glass": ["glass"],
    "bicycle": ["bike"],
    "motorcycle": ["motorbike"],
    "airplane": ["plane", "jet"],
    "potted plant": ["plant"],
    "laptop": ["computer"],
    "refrigerator": ["fridge"],
    "truck": ["lorry"],
    "boat": ["ship", "sailboat"],
    "fire hydrant": ["hydrant"],
    "hot dog": ["hotdog"],
    "traffic light": ["stoplight"],
    "sports ball": ["ball", "football", "soccer ball", "basketball"],
    "baseball bat": ["bat"],
    "tennis racket": ["racket", "racquet"],
}

MULTIWORD_ALIASES = {
    "hydrant": "fire hydrant",
    "hotdog": "hot dog",
    "stoplight": "traffic light",
    "bat": "baseball bat",
    "racket": "tennis racket",
    "racquet": "tennis racket",
}

OBJECT_VOCAB = set(COCO_OBJECTS)
for _syns in COCO_SYNONYMS.values():
    OBJECT_VOCAB.update(_syns)
OBJECT_VOCAB.update(MULTIWORD_ALIASES.keys())


@dataclass
class CaptionRecord:
    img_id: int
    gt: set[str]
    caption: str


class ChairExtractor:
    def find_content_words(self, caption: str, gt_objects: Iterable[str]) -> tuple[list[str], list[str]]:
        raise NotImplementedError

    @staticmethod
    def expanded_gt(gt_objects: Iterable[str]) -> set[str]:
        gt_norm = {o.lower() for o in gt_objects}
        expanded = set(gt_norm)
        for canonical, syns in COCO_SYNONYMS.items():
            if canonical in gt_norm:
                expanded.update(syns)
        for alias, canonical in MULTIWORD_ALIASES.items():
            if canonical in gt_norm:
                expanded.add(alias)
        return expanded


class SpacyChairExtractor(ChairExtractor):
    def __init__(self) -> None:
        try:
            import spacy
        except ImportError as exc:
            raise RuntimeError("spaCy is not installed. Install spacy + en_core_web_sm, or use --scorer regex.") from exc
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError as exc:
            raise RuntimeError("spaCy model en_core_web_sm is missing. Run: python -m spacy download en_core_web_sm") from exc

    def find_content_words(self, caption: str, gt_objects: Iterable[str]) -> tuple[list[str], list[str]]:
        expanded_gt = self.expanded_gt(gt_objects)
        doc = self.nlp(caption or "")
        obj_words: list[str] = []
        hall_words: list[str] = []
        for tok in doc:
            w = tok.text.lower().strip()
            if tok.pos_ not in ("NOUN", "PROPN") or len(w) < 2:
                continue
            canonical = MULTIWORD_ALIASES.get(w, w)
            if w in OBJECT_VOCAB or canonical in OBJECT_VOCAB:
                obj_words.append(w)
                if w not in expanded_gt and canonical not in expanded_gt:
                    hall_words.append(w)
        return obj_words, hall_words


class RegexChairExtractor(ChairExtractor):
    TOKEN_RE = re.compile(r"[a-z][a-z-]*", re.IGNORECASE)

    def find_content_words(self, caption: str, gt_objects: Iterable[str]) -> tuple[list[str], list[str]]:
        expanded_gt = self.expanded_gt(gt_objects)
        obj_words: list[str] = []
        hall_words: list[str] = []
        for match in self.TOKEN_RE.finditer(caption or ""):
            w = match.group(0).lower()
            if len(w) < 2:
                continue
            canonical = MULTIWORD_ALIASES.get(w, w)
            if w in OBJECT_VOCAB or canonical in OBJECT_VOCAB:
                obj_words.append(w)
                if w not in expanded_gt and canonical not in expanded_gt:
                    hall_words.append(w)
        return obj_words, hall_words


def load_extractor(name: str) -> tuple[ChairExtractor, str]:
    if name == "spacy":
        return SpacyChairExtractor(), "spacy"
    if name == "regex":
        return RegexChairExtractor(), "regex"
    try:
        return SpacyChairExtractor(), "spacy"
    except RuntimeError as exc:
        print(f"WARNING: {exc}")
        print("WARNING: Falling back to --scorer regex. Use --scorer spacy for paper numbers.")
        return RegexChairExtractor(), "regex"


def per_image_chair(caption: str, gt: Iterable[str], extractor: ChairExtractor) -> dict[str, float]:
    obj_words, hall_words = extractor.find_content_words(caption, gt)
    return {
        "CHAIRs": 1.0 if hall_words else 0.0,
        "CHAIRi": len(hall_words) / max(len(obj_words), 1),
        "n_object_words": float(len(obj_words)),
        "n_hall_words": float(len(hall_words)),
        "caption_len_words": float(len((caption or "").split())),
    }


def metric_ci(values: list[float], n_boot: int, seed: int) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    if len(arr) == 0:
        return {"mean": math.nan, "ci_low": math.nan, "ci_high": math.nan, "n": 0}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(arr), size=(n_boot, len(arr)))
    boot = arr[idx].mean(axis=1)
    return {
        "mean": float(arr.mean()),
        "ci_low": float(np.percentile(boot, 2.5)),
        "ci_high": float(np.percentile(boot, 97.5)),
        "n": int(len(arr)),
    }


def paired_delta(
    reference: list[float],
    method: list[float],
    n_boot: int,
    n_perm: int,
    seed: int,
) -> dict[str, float]:
    ref = np.asarray(reference, dtype=float)
    met = np.asarray(method, dtype=float)
    if len(ref) != len(met):
        raise ValueError("paired_delta requires equal-length paired arrays")
    if len(ref) == 0:
        return {"delta": math.nan, "ci_low": math.nan, "ci_high": math.nan, "p_perm": math.nan, "n": 0}

    diff = met - ref
    delta = float(diff.mean())

    rng = np.random.default_rng(seed)
    boot_idx = rng.integers(0, len(diff), size=(n_boot, len(diff)))
    boot = diff[boot_idx].mean(axis=1)
    ci_low, ci_high = np.percentile(boot, [2.5, 97.5])

    if np.allclose(diff, 0):
        p_perm = 1.0
    else:
        signs = rng.choice([-1.0, 1.0], size=(n_perm, len(diff)))
        perm = (signs * diff).mean(axis=1)
        p_perm = float((np.sum(np.abs(perm) >= abs(delta)) + 1) / (n_perm + 1))

    return {
        "delta": delta,
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
        "p_perm": p_perm,
        "n": int(len(diff)),
    }


def load_json(path: Path) -> Any:
    with path.open() as f:
        return json.load(f)


def records_from_stage4(stage4_path: Path, method: str) -> list[CaptionRecord]:
    data = load_json(stage4_path)
    records = []
    for rec in data["eval_captions"]:
        caption = rec["captions"].get(method, "")
        records.append(CaptionRecord(int(rec["img_id"]), {x.lower() for x in rec["gt"]}, caption))
    return records


def records_from_caption_file(path: Path, gt_by_id: dict[int, set[str]]) -> list[CaptionRecord]:
    rows = load_json(path)
    records = []
    for row in rows:
        img_id = int(row["img_id"])
        gt = {x.lower() for x in row.get("gt", [])} or gt_by_id.get(img_id, set())
        records.append(CaptionRecord(img_id, gt, row.get("caption", "")))
    return records


def score_records(records: list[CaptionRecord], extractor: ChairExtractor) -> dict[str, list[float]]:
    scores = {"CHAIRs": [], "CHAIRi": [], "caption_len_words": [], "n_object_words": [], "n_hall_words": []}
    for rec in records:
        row = per_image_chair(rec.caption, rec.gt, extractor)
        for key in scores:
            scores[key].append(row[key])
    return scores


def summarize_condition(records: list[CaptionRecord], extractor: ChairExtractor, n_boot: int, seed: int) -> dict[str, Any]:
    scores = score_records(records, extractor)
    return {
        "n": len(records),
        "metrics": {
            "CHAIRs": metric_ci(scores["CHAIRs"], n_boot, seed + 11),
            "CHAIRi": metric_ci(scores["CHAIRi"], n_boot, seed + 17),
        },
        "aux": {
            "avg_caption_len_words": float(np.mean(scores["caption_len_words"])) if records else math.nan,
            "avg_object_words": float(np.mean(scores["n_object_words"])) if records else math.nan,
            "avg_hallucinated_words": float(np.mean(scores["n_hall_words"])) if records else math.nan,
        },
        "per_image": scores,
    }


def align_pair(
    ref_records: list[CaptionRecord],
    method_records: list[CaptionRecord],
) -> tuple[list[CaptionRecord], list[CaptionRecord]]:
    ref_by_id = {r.img_id: r for r in ref_records}
    method_by_id = {r.img_id: r for r in method_records}
    ids = [r.img_id for r in ref_records if r.img_id in method_by_id]
    return [ref_by_id[i] for i in ids], [method_by_id[i] for i in ids]


def stage4_analysis(
    results_dir: Path,
    extractor: ChairExtractor,
    n_boot: int,
    n_perm: int,
    seed: int,
) -> dict[str, Any]:
    path = results_dir / "stage4_400img_results.json"
    methods = ["baseline", "stage2", "stage3", "stage4"]
    records = {m: records_from_stage4(path, m) for m in methods}
    summaries = {m: summarize_condition(records[m], extractor, n_boot, seed) for m in methods}

    deltas: dict[str, Any] = {}
    ref = summaries["baseline"]["per_image"]
    for method in methods:
        if method == "baseline":
            continue
        deltas[method] = {
            "vs": "baseline",
            "CHAIRs": paired_delta(ref["CHAIRs"], summaries[method]["per_image"]["CHAIRs"], n_boot, n_perm, seed + 101),
            "CHAIRi": paired_delta(ref["CHAIRi"], summaries[method]["per_image"]["CHAIRi"], n_boot, n_perm, seed + 103),
        }

    for summary in summaries.values():
        summary.pop("per_image", None)

    return {
        "source": str(path),
        "conditions": summaries,
        "paired_deltas_vs_baseline": deltas,
    }


def spin_analysis(
    results_dir: Path,
    caption_dir: Path,
    stage4_path: Path,
    extractor: ChairExtractor,
    budgets: list[int],
    n_boot: int,
    n_perm: int,
    seed: int,
) -> dict[str, Any]:
    stage4 = load_json(stage4_path)
    gt_by_id = {int(r["img_id"]): {x.lower() for x in r["gt"]} for r in stage4["eval_captions"]}
    out: dict[str, Any] = {}

    for budget in budgets:
        base_path = caption_dir / f"baseline_captions_budget{budget}.json"
        spin_path = caption_dir / f"spin_captions_budget{budget}.json"
        if not base_path.exists() or not spin_path.exists():
            out[f"budget_{budget}"] = {
                "status": "missing",
                "required_files": [str(base_path), str(spin_path)],
            }
            continue

        base_records = records_from_caption_file(base_path, gt_by_id)
        spin_records = records_from_caption_file(spin_path, gt_by_id)
        base_aligned, spin_aligned = align_pair(base_records, spin_records)

        summaries = {
            "baseline": summarize_condition(base_aligned, extractor, n_boot, seed + budget),
            "spin": summarize_condition(spin_aligned, extractor, n_boot, seed + budget + 1),
        }
        deltas = {
            "spin": {
                "vs": "baseline",
                "CHAIRs": paired_delta(
                    summaries["baseline"]["per_image"]["CHAIRs"],
                    summaries["spin"]["per_image"]["CHAIRs"],
                    n_boot,
                    n_perm,
                    seed + budget + 201,
                ),
                "CHAIRi": paired_delta(
                    summaries["baseline"]["per_image"]["CHAIRi"],
                    summaries["spin"]["per_image"]["CHAIRi"],
                    n_boot,
                    n_perm,
                    seed + budget + 203,
                ),
            }
        }
        for summary in summaries.values():
            summary.pop("per_image", None)

        out[f"budget_{budget}"] = {
            "status": "complete",
            "source_files": {"baseline": str(base_path), "spin": str(spin_path)},
            "conditions": summaries,
            "paired_deltas_vs_baseline": deltas,
        }

    return out


def fmt_ci(metric: dict[str, float]) -> str:
    return f"{metric['mean']:.4f} [{metric['ci_low']:.4f}, {metric['ci_high']:.4f}]"


def fmt_delta(delta: dict[str, float]) -> str:
    return f"{delta['delta']:+.4f} [{delta['ci_low']:+.4f}, {delta['ci_high']:+.4f}], p={delta['p_perm']:.4f}"


def markdown_report(summary: dict[str, Any]) -> str:
    lines = [
        "# CHAIR Bootstrap and Paired Significance",
        "",
        f"Scorer: `{summary['scorer']}`",
        f"Bootstrap resamples: `{summary['n_boot']}`",
        f"Permutation resamples: `{summary['n_perm']}`",
        "",
        "Negative paired deltas mean the method has lower hallucination than the reference.",
        "",
    ]
    if summary["scorer"] != "spacy":
        lines += [
            "**Warning:** this was run with the dependency-free regex scorer. Use `--scorer spacy` for paper numbers that match the project notebooks.",
            "",
        ]
    lines += [
        "## Stage 4 Main Comparison",
        "",
        "| Method | n | CHAIRs 95% CI | CHAIRi 95% CI | Avg Len |",
        "|---|---:|---:|---:|---:|",
    ]

    for method, result in summary["stage4"]["conditions"].items():
        lines.append(
            f"| {method} | {result['n']} | {fmt_ci(result['metrics']['CHAIRs'])} | "
            f"{fmt_ci(result['metrics']['CHAIRi'])} | {result['aux']['avg_caption_len_words']:.1f} |"
        )

    lines += [
        "",
        "### Paired Deltas vs Baseline",
        "",
        "| Method | Delta CHAIRs | Delta CHAIRi |",
        "|---|---:|---:|",
    ]
    for method, result in summary["stage4"]["paired_deltas_vs_baseline"].items():
        lines.append(f"| {method} | {fmt_delta(result['CHAIRs'])} | {fmt_delta(result['CHAIRi'])} |")

    lines += ["", "## SPIN Budgets", ""]
    for budget, block in summary["spin"].items():
        lines.append(f"### {budget}")
        lines.append("")
        if block["status"] != "complete":
            lines.append("Missing caption files:")
            for file_path in block["required_files"]:
                lines.append(f"- `{file_path}`")
            lines.append("")
            continue

        lines += [
            "| Method | n | CHAIRs 95% CI | CHAIRi 95% CI | Avg Len |",
            "|---|---:|---:|---:|---:|",
        ]
        for method, result in block["conditions"].items():
            lines.append(
                f"| {method} | {result['n']} | {fmt_ci(result['metrics']['CHAIRs'])} | "
                f"{fmt_ci(result['metrics']['CHAIRi'])} | {result['aux']['avg_caption_len_words']:.1f} |"
            )
        lines += [
            "",
            "| Method | Delta CHAIRs | Delta CHAIRi |",
            "|---|---:|---:|",
        ]
        for method, result in block["paired_deltas_vs_baseline"].items():
            lines.append(f"| {method} | {fmt_delta(result['CHAIRs'])} | {fmt_delta(result['CHAIRi'])} |")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--caption-dir", type=Path, default=Path("results"))
    parser.add_argument("--out-json", type=Path, default=Path("results/bootstrap_chair_significance.json"))
    parser.add_argument("--out-md", type=Path, default=Path("results/bootstrap_chair_significance.md"))
    parser.add_argument("--budgets", type=int, nargs="+", default=[64, 128])
    parser.add_argument("--n-boot", type=int, default=5000)
    parser.add_argument("--n-perm", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--scorer", choices=["auto", "spacy", "regex"], default="spacy")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    extractor, scorer_name = load_extractor(args.scorer)

    stage4_path = args.results_dir / "stage4_400img_results.json"
    if not stage4_path.exists():
        raise FileNotFoundError(f"Missing required file: {stage4_path}")

    summary = {
        "scorer": scorer_name,
        "n_boot": args.n_boot,
        "n_perm": args.n_perm,
        "seed": args.seed,
        "stage4": stage4_analysis(args.results_dir, extractor, args.n_boot, args.n_perm, args.seed),
        "spin": spin_analysis(
            args.results_dir,
            args.caption_dir,
            stage4_path,
            extractor,
            args.budgets,
            args.n_boot,
            args.n_perm,
            args.seed,
        ),
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(summary, indent=2) + "\n")
    args.out_md.write_text(markdown_report(summary))

    print(f"Wrote {args.out_json}")
    print(f"Wrote {args.out_md}")
    print(f"Scorer: {scorer_name}")
    missing = [name for name, block in summary["spin"].items() if block["status"] != "complete"]
    if missing:
        print("SPIN budgets not yet scored because caption files are missing:", ", ".join(missing))


if __name__ == "__main__":
    main()
