import pandas as pd
import json
import ast

# Paths
csv_path = "../Dataset/processed/semantic_extraction/esg_extraction_results.csv"
taxonomy_path = "output/esg_categorized_topics.json"
output_path = "../Dataset/processed/semantic_extraction/esg_final_enriched.csv"

# Step 1: Load CSV
df = pd.read_csv(csv_path)

# Step 2: Load topic classification data
# The txt file likely contains a JSON-like dict string (not perfect JSON)
with open(taxonomy_path, 'r', encoding='utf-8') as f:
    content = f.read().strip()

# Fix possible formatting issues
try:
    topic_mapping = json.loads(content)
except json.JSONDecodeError:
    topic_mapping = ast.literal_eval(content)  # fallback if JSON not perfect

# Step 3: Create mapping DataFrame
taxonomy_df = pd.DataFrame.from_dict(topic_mapping, orient='index').reset_index()
taxonomy_df.rename(columns={'index': 'esg_topic'}, inplace=True)

# Step 4: Merge both datasets
merged = pd.merge(df, taxonomy_df[['esg_topic', 'pillar', 'category', 'subcategory']], on='esg_topic', how='left')

# Step 5: Select only required columns
final_df = merged[['record_index', 'company', 'date', 'esg_topic', 'sentence', 'pillar', 'category', 'subcategory', 'title', 'url']]

# Step 6: Save the result
final_df.to_csv(output_path, index=False, encoding='utf-8')

print(f"Final enriched CSV saved to: {output_path}")
print(final_df.head())
