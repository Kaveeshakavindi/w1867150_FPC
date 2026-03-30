from prompt import check_system_quality
import pandas as pd
import json

def extract_output(raw):

    try:
        data = json.loads(raw)

        return f"""
Judgment: {data.get('judgment')}
Greenwashing Status: {data.get('greenwashing_status')}
Reason: {data.get('reason_for_judgement')}
"""
    except:
        return raw

file_b = "../../Backend/test_set_baseline.csv" #without retrieval and ontology
file_a = "../../Backend/test_set_Synapse.csv" #with retrieval and ontology

df_a = pd.read_csv(file_a)
df_b = pd.read_csv(file_b)


wins_a = 0
wins_b = 0
results = []

for i in range(535):

    row_a = extract_output(df_a.iloc[i])
    row_b = extract_output(df_b.iloc[i])
    winner = check_system_quality(row_a, row_b).strip()
    if "A" in winner:
        verdict = "A"
        wins_a += 1
    elif "B" in winner:
        verdict = "B"
        wins_b += 1
    else:
        verdict = "Unknown"

    results.append(verdict)

    print(f"Case {i}: {verdict}")

total = wins_a + wins_b

score_a = wins_a / total if total > 0 else 0
score_b = wins_b / total if total > 0 else 0

print("\n----- FINAL RESULTS -----")
print("A wins:", wins_a)
print("B wins:", wins_b)
print("A win rate:", round(score_a, 3))
print("B win rate:", round(score_b, 3))

# save detailed results
pd.DataFrame({
    "winner": results
}).to_csv("pairwise_evaluation_results_baseline.csv", index=False)
