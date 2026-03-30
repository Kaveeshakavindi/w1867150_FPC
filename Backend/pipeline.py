import json
from ontologyInfo import get_ontology_info
from retrieval import retrieve_context
from owlready2 import *
from prompt import system_prompt, guardrails, prompt_template, examples

from eval_prompts import baseline_system_prompt, baseline_prompt_template, guardrails, vanilla_system_prompt, vanilla_prompt_template,counter_system_prompt, counter_prompt_template
from eval_retrieval import vanilla_retrieve_context
from llm import chat_model
from generateTestSet import save_to_test_set, compute_rouge_for_test_set, save_to_test_set_baseline, save_to_test_vanillaRag, save_to_test_counterfactualRAG
import math

def citations(docs):
    output = []

    for d in docs:
        url = d.metadata.get("url")

        # convert NaN → None
        if isinstance(url, float) and math.isnan(url):
            url = None
        output.append({
            "title": d.metadata.get("title"),
            "company": d.metadata.get("company"),
            "date": d.metadata.get("date"),
            "year": d.metadata.get("year"),
            "article": d.metadata.get("article"),
            "url": url
        })

    return output

def evaluate_claim(query: str, company: str):
    """Evaluate a company ESG claim and auto-save to test_set.csv."""

    # ── 1. Retrieve context ──────────────────────────────────────────────────
    serialized_docs, company_docs, counterfactual_docs, supportive_docs = retrieve_context(query, company)
    # serialized_docs, docs = vanilla_retrieve_context(query, company)
    
    # Aggregate serialized docs into a single string
    if isinstance(serialized_docs, list):
        serialized_docs = "\n\n".join(serialized_docs)

    # ── 2. Load ontology ─────────────────────────────────────────────────────
    ontology_path = "ontology.owl"
    onto = get_ontology(ontology_path).load()
    ontology_info = get_ontology_info(onto)

    # ── 3. Build prompt  without RAG and ontology──────────────────────────────────────────────────────
    # final_prompt = f"""
    # System: {baseline_system_prompt}

    # Instructions:
    # {baseline_prompt_template.format(company=company, query=query)}

    #     Guardrails:
    # {guardrails}
    #     """

#     # ── 3. Build prompt ──────────────────────────────────────────────────────
    final_prompt = f"""
        System: {system_prompt}

        Documents:
    {serialized_docs}

        Examples:
    {examples}

        Instructions:
    {prompt_template.format(company=company, query=query, ontology=ontology_info)}

        Guardrails:
    {guardrails}
    """
    print(final_prompt)

    # ── 4. Call LLM ──────────────────────────────────────────────────────────
    response = chat_model.invoke(final_prompt)
    raw_output = response.content if hasattr(response, "content") else str(response)

    # ── 5. Parse JSON ────────────────────────────────────────────────────────
    result = {}
    try:
        result = json.loads(raw_output)
    except json.JSONDecodeError:
        # Strip markdown code fences if present
        for fence in ["```json", "```"]:
            if fence in raw_output:
                start = raw_output.find(fence) + len(fence)
                end = raw_output.find("```", start)
                try:
                    result = json.loads(raw_output[start:end].strip())
                    break
                except json.JSONDecodeError:
                    pass
        if not result:
            result = {"error": "Failed to parse JSON", "raw_content": raw_output}

    # Unwrap "result" key if LLM wraps output like {"result": {...}}
    if "result" in result and isinstance(result["result"], dict):
        result = result["result"]

     # ── 6. Always attach retrieved documents as citations (Synapse) ────────────────────
    company_docs = citations(company_docs)
    counterfactual_docs = citations(counterfactual_docs)
    supportive_docs = citations(supportive_docs)
    result["retrieved_documents"] = {
        "company_reports": company_docs,
        "counterfactual_sources": counterfactual_docs,
        "supportive_sources": supportive_docs
    }

# Vanilla RAG doesn't categorize documents, so we attach all retrieved docs under a single "documents" key:
    # result["retrieved_documents"] = {
    #     "documents": citations(docs)
    # }

    # ── 7. Auto-save to test set CSV ─────────────────────────────────────────
    # save_to_test_set_baseline(
    #     company=company,
    #     query=query,
    #     result=result,
    #     raw_llm_output=raw_output
    # )

    save_to_test_set(
        company=company,
        query=query,
        result=result,
        serialized_docs=serialized_docs,
        raw_llm_output=raw_output
    )
    print(result)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Run ROUGE over the full saved test set at any time:
#   from evaluate_claim import compute_rouge_for_test_set
#   compute_rouge_for_test_set()
# ─────────────────────────────────────────────────────────────────────────────
