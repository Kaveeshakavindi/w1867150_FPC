import pandas as pd
from sklearn.metrics import cohen_kappa_score

# paths
gpt_file = "gpt/pairwise_evaluation_results_baseline.csv"
claude_file = "claude/pairwise_evaluation_results_baseline.csv"

gpt = pd.read_csv(gpt_file)
claude = pd.read_csv(claude_file)

gpt_labels = gpt["winner"].astype(str).str.strip().iloc[:350]
claude_labels = claude["winner"].astype(str).str.strip().iloc[:350]

AA = 0
BB = 0
AB = 0
BA = 0

for g, c in zip(gpt_labels, claude_labels):

    if g == "A" and c == "A":
        AA += 1
    elif g == "B" and c == "B":
        BB += 1
    elif g == "A" and c == "B":
        AB += 1
    elif g == "B" and c == "A":
        BA += 1

total = len(gpt_labels)

agreement = AA + BB
disagreement = AB + BA

print("\n--- Agreement Table ---")
print(f"GPT A  | Claude A : {AA}")
print(f"GPT B  | Claude B : {BB}")
print(f"GPT A  | Claude B : {AB}")
print(f"GPT B  | Claude A : {BA}")

print("\n--- Agreement Summary ---")
print("Total scenarios:", total)
print("Agreement:", agreement)
print("Disagreement:", disagreement)
print("Agreement rate:", round(agreement / total, 3))

# Cohen's kappa
kappa = cohen_kappa_score(gpt_labels, claude_labels)

print("\n--- Cohen's Kappa ---")
print("Kappa:", round(kappa, 3))