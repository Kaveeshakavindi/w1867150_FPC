import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# Paths to your results
gpt_file = "gpt/pairwise_evaluation_results_vanillaRAG.csv"
claude_file = "claude/pairwise_evaluation_results_vanillaRAG.csv"

# Load the data
gpt = pd.read_csv(gpt_file)
claude = pd.read_csv(claude_file)

# Extract winner labels
gpt_labels = gpt["winner"].astype(str).str.strip().iloc[:350]
claude_labels = claude["winner"].astype(str).str.strip().iloc[:350]

# Confusion matrix
labels = ["A", "B"]
cm = confusion_matrix(gpt_labels, claude_labels, labels=labels)

# Create a DataFrame for easier plotting
cm_df = pd.DataFrame(cm, index=[f"GPT {l}" for l in labels], columns=[f"Claude {l}" for l in labels])

# Plot
plt.figure(figsize=(6,5))
sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues")
plt.title("GPT vs Claude Agreement Confusion Matrix")
plt.ylabel("GPT Prediction")
plt.xlabel("Claude Prediction")
plt.show()