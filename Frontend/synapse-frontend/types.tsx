interface ResultType {
  company_claim_summary: string;
  object_property: string;
  judgment: string;
  greenwashing_status: string;
  reason_for_judgement: string;
  summary_support_evidence: string;
  summary_counter_evidence: string;
  retrieved_documents:{
    company_reports: EvidenceItem[];
    counterfactual_sources: EvidenceItem[];
    supportive_sources: EvidenceItem[];
  }
}

interface AnalysisResultsProps {
  companyName: string;
  query: string;
  supportingEvidence: EvidenceItem[];
  refutingEvidence: EvidenceItem[];
  companyClaimSummary: EvidenceItem[];
}

interface EvidenceItem {
  id: number;
  title: string;
  company: string;
  article: string;
  url: string;
}