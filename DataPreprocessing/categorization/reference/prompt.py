from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an ESG (Environmental, Social, Governance) expert."),
    ("human", """Categorize the following topics into the ESG taxonomy structure provided.

ESG Taxonomy: {taxonomy}

Topics to categorize: {topics}

Instructions:
1. Assign each topic to the most appropriate Pillar (Environmental, Social, or Governance)
2. Within that pillar, assign it to a Category
3. Within that category, assign it to a Sub-category (or suggest a new one if none fit well)
4. If a topic could fit multiple categories, choose the primary/best fit
5. For ambiguous topics, use your best judgment based on ESG standards   

Return ONLY a JSON object with this structure (no markdown, no extra text):
{{
"topic_name": {{
    "pillar": "Environmental/Social/Governance",
    "category": "category_name",
    "subcategory": "subcategory_name",
    "confidence": "high/medium/low",
    "reasoning": "brief explanation"
    }},
...
}}""")
])