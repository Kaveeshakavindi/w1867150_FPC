# relevancy_check.py
from llm import llm

evaluation_prompt = """
You are an expert ESG analyst evaluating two AI systems on a greenwashing detection task.
Both systems analyzed the same company claim and provided a verdict.

You are given:
- The original company claim
- Response A: verdict and reasoning from System A
- Response B: verdict and reasoning from System B

Evaluate which response is better based on these criteria:

1. COUNTER-EVIDENCE DETECTION (most important): Does the system identify and use counter-evidence 
   that is present in the input? A system that ignores available counter-evidence should be penalized heavily.
   
2. GREENWASHING FLAGGING: When counter-evidence exists (e.g. corruption allegations, legal investigations, 
   regulatory violations), the correct verdict is typically "Greenwashing" or "Misleading" — NOT "NotGreenwashing".
   A system that returns "NotGreenwashing" despite clear counter-evidence in the input is WRONG.

3. GROUNDEDNESS: Is the verdict supported by specific evidence from the input rather than assumptions?

4. CONSISTENCY: Does the greenwashing verdict logically follow from the reasoning and evidence provided?

5. EVIDENCE QUALITY: Does the response correctly distinguish between supportive and counter-evidence?

PENALIZE:
- Any response that ignores counter-evidence present in the input.
- Any response that returns "NotGreenwashing" or "Unsupported" when counter-evidence is clearly available.
- Any response that fabricates facts or gives a verdict without citing concrete evidence.

REWARD:
- Responses that detect counter-evidence (e.g. legal investigations, corruption, regulatory actions) 
  and correctly classify the claim as Greenwashing or Misleading as a result.

Company Claim:
{company_claim_summary}

Response A:
- Verdict: {verdict_a}
- Judgment: {judgment_a}
- Reasoning: {reason_a}
- Supporting Evidence: {support_a}
- Counter Evidence: {counter_a}

Response B:
- Verdict: {verdict_b}
- Judgment: {judgment_b}
- Reasoning: {reason_b}
- Supporting Evidence: {support_b}
- Counter Evidence: {counter_b}

Which system produced a more evidence-based, accurate and trustworthy greenwashing assessment?

Think step by step:
1. Is counter-evidence present in the input?
2. Which system detected and used that counter-evidence?
3. Which verdict is more consistent with the available evidence?

Output ONLY one character:
A
or
B
"""
import json

def parse_response(raw):
    try:
        return json.loads(raw)
    except:
        return {}

def check_system_quality(row_a, row_b):
    a = parse_response(row_a["raw_llm_output"])
    b = parse_response(row_b["raw_llm_output"])

    prompt = evaluation_prompt.format(
        company_claim_summary=row_a.get("company_claim_summary", "N/A"),

        verdict_a=a.get("greenwashing_status", "N/A"),
        judgment_a=a.get("judgment", "N/A"),
        reason_a=a.get("reason_for_judgement", "N/A"),
        support_a=a.get("summary_support_evidence", "N/A"),
        counter_a=a.get("summary_counter_evidence", "N/A"),

        verdict_b=b.get("greenwashing_status", "N/A"),
        judgment_b=b.get("judgment", "N/A"),
        reason_b=b.get("reason_for_judgement", "N/A"),
        support_b=b.get("summary_support_evidence", "N/A"),
        counter_b=b.get("summary_counter_evidence", "N/A"),
    )

    result = llm.invoke(prompt)
    return result.content.strip()