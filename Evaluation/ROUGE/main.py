"""
Compute ROUGE scores from generated test_set.csv and save results to CSV.
Prediction = concatenation of LLM output fields:
    company_claim_summary + summary_counter_evidence + summary_support_evidence + reason_for_judgement
Reference = rouge_reference column (all retrieved Article sentences in order)
"""

import csv
from evaluate import load

rouge = load("rouge")
TEST_SET_PATH = "../../Backend/test_set_baseline.csv"


def build_prediction_from_row(row: dict) -> str:
    """Concatenate LLM output fields into one prediction string."""
    fields = [
        
        row.get("company_claim_summary", ""),
        row.get("summary_support_evidence", ""),
         row.get("summary_counter_evidence", ""),
        row.get("reason_for_judgement", ""),
    ]
    return " ".join(f for f in fields if f and f.strip())


def compute_rouge_from_csv(path: str = TEST_SET_PATH):
    predictions = []
    references = []
    row_labels = []
    raw_rows = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pred = build_prediction_from_row(row)
            ref = row.get("rouge_reference", "").strip()
            if pred and ref:
                predictions.append(pred)
                references.append(ref)
                row_labels.append(f"{row.get('company','?')} | {row.get('query','?')}")
                raw_rows.append(row)

    if not predictions:
        print("No valid rows found.")
        return

    # ── Per-row scores ──────────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print(f"{'Per-Row ROUGE Scores':^65}")
    print(f"{'='*65}")
    print(f"{'Row':<35} {'R1':>7} {'R2':>7} {'RL':>7} {'RLsum':>7}")
    print(f"{'-'*65}")

    per_row_results = []
    for i, (label, pred, ref, row) in enumerate(zip(row_labels, predictions, references, raw_rows)):
        r = rouge.compute(predictions=[pred], references=[ref])
        company = row.get("company", "?")
        query = row.get("query", "?")
        judgment = row.get("judgment", "?")
        greenwashing_status = row.get("greenwashing_status", "?")
        timestamp = row.get("timestamp", "?")

        per_row_results.append({
            "row":                i + 1,
            "company":            company,
            "query":              query,
            "judgment":           judgment,
            "greenwashing_status": greenwashing_status,
            "rouge1":             round(float(r["rouge1"]), 4),
            "rouge2":             round(float(r["rouge2"]), 4),
            "rougeL":             round(float(r["rougeL"]), 4),
            "rougeLsum":          round(float(r["rougeLsum"]), 4),
            "timestamp":          timestamp,
        })

        print(
            f"{label:<35} "
            f"{float(r['rouge1']):>7.4f} "
            f"{float(r['rouge2']):>7.4f} "
            f"{float(r['rougeL']):>7.4f} "
            f"{float(r['rougeLsum']):>7.4f}"
        )

    # ── Aggregate scores ────────────────────────────────────────────────────
    overall = rouge.compute(predictions=predictions, references=references)
    print(f"\n{'='*65}")
    print(f"{'Aggregate ROUGE across all rows':^65}")
    print(f"{'='*65}")
    for k, v in overall.items():
        print(f"  {k:<12}: {float(v):.4f}")
    print(f"\nTotal rows evaluated: {len(predictions)}")

    # ── Save to CSV ─────────────────────────────────────────────────────────
    output_path = path.replace(".csv", "_rouge_scores.csv")
    fieldnames = ["row", "company", "query", "judgment", "greenwashing_status",
                  "rouge1", "rouge2", "rougeL", "rougeLsum", "timestamp"]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for result in per_row_results:
            writer.writerow(result)

        # Aggregate summary row
        writer.writerow({
            "row":                "AGGREGATE",
            "company":            "ALL",
            "query":              "ALL",
            "judgment":           "-",
            "greenwashing_status": "-",
            "rouge1":             round(float(overall["rouge1"]), 4),
            "rouge2":             round(float(overall["rouge2"]), 4),
            "rougeL":             round(float(overall["rougeL"]), 4),
            "rougeLsum":          round(float(overall["rougeLsum"]), 4),
            "timestamp":          "-",
        })

    print(f"\nResults saved to: {output_path}")
    return overall


if __name__ == "__main__":
    compute_rouge_from_csv()