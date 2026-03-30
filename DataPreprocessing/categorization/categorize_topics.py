from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import json, re
import matplotlib.pyplot as plt
from reference.taxonomy_ref import taxonomy
from reference.prompt import prompt

# model initialization
model = "gemini-2.5-flash-lite"

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key

try:
    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    print(f"Connected to Gemini API")
    print(f"Using model: {model}")
except Exception as e:
    print(f"Error initializing Gemini: {e}")
    raise



# load extracted topics
with open("reference/extracted-esg-topics.txt", "r", encoding="utf-8") as f:
    topics = [line.strip() for line in f if line.strip()]

chain = prompt | llm

response = chain.invoke({
    "taxonomy": taxonomy,
    "topics": topics
})

print(response.content)

log_file_path = "esg_categorized_topics.txt"

with open(log_file_path, "a", encoding="utf-8") as f:
    f.write("=== New ESG Categorization ===\n")
    f.write(response.content)
    f.write("\n\n")  

raw = response.content.strip()
cleaned = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
data = json.loads(cleaned)
df = pd.DataFrame([
    {
        "Topic": topic,
        "Pillar": info["pillar"],
        "Confidence": info["confidence"]
    }
      for topic, info in data.items()
])

print(df.head())

# Count topics per Pillar
plt.figure(figsize=(4, 5))
bar_plot = df['Pillar'].value_counts().plot(kind='bar')
plt.title("Number of Topics per ESG Pillar")
plt.xlabel("Pillar")
plt.ylabel("Topic Count")
plt.tight_layout()
# Add number labels on each bar
for i, value in enumerate(df['Pillar'].value_counts()):
    plt.text(i, value + 0.1, str(value), ha='center', va='bottom', fontsize=10)
plt.show()

# Confidence distribution per pillar
plt.figure(figsize=(6,4))
pd.crosstab(df['Pillar'], df['Confidence']).plot(kind='bar', stacked=True)
plt.title("Confidence Levels per ESG Pillar")
plt.xlabel("Pillar")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
