"use client";

import { useState } from "react";
import { form_dropdowns, stages } from "../../data";
import Evidence from "../../components/Evidence";
import BreadCrumb from "@/components/BreadCrumb";
import Chip from "@/components/Chip";
import { Button, Select, Space } from 'antd';
import Ready from "@/components/Ready";

import { Form } from "antd";
import LoadingAnalysis from "@/components/LoadingAnalysis";

const page = () => {
    const [selectedCompany, setSelectedCompany] = useState("");
    const [selectedQuery, setSelectedQuery] = useState("");
    const [useOntology, setUseOntology] = useState(false);
    const [useCounterfactual, setUseCounterfactual] = useState(false);
    const [result, setResult] = useState<ResultType | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [currentStatus, setCurrentStatus] = useState("");
    const [progress, setProgress] = useState(0);

    const handleSubmit = async () => {
        try {
            setLoading(true);
            setError(null);
            setResult(null);

            setProgress(0)
            setCurrentStatus("Initializing analysis");
            
            const response = await fetch(
                "http://127.0.0.1:8000/evaluate_claim",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        company: selectedCompany,
                        query: selectedQuery,
                        useOntology,
                        useCounterfactual,
                    }),
                }
            );
            setProgress(80);
            setCurrentStatus("Generating explanation");
            
            if (!response.ok) {
                throw new Error("Failed to fetch evaluation");
            }

            const data = await response.json();

            setResult(data.result);

        } catch (err: any) {
            setError(err.message || "Something went wrong");
        } finally {
            setLoading(false);
            setProgress(100);
        }
    };

    const statusColor =
        result?.greenwashing_status === "Greenwashing"
            ? "text-red-600"
            : "text-green-600";
    return (
        <div className="min-h-screen bg-gray-100 p-6">
            <BreadCrumb prev="Home" current="Analyze Claim" />
            <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-6  ">
                {/* LEFT FORM */}
                <div className="bg-white rounded-2xl p-6 space-y-8 h-[80vh] " >
                    <h2 className="text-xl font-semibold text-gray-800">
                        Greenwashing Checker
                    </h2>
                    <p className="text-sm text-gray-400">
                        Please select a company and provide your query to check for potential greenwashing.
                    </p>

                    <Form >

                        {/* Company Dropdown */}

                        {form_dropdowns.length > 0 && form_dropdowns.map((dropdown) => (
                            <Form.Item label={dropdown.label} key={dropdown.placeholder}>
                                <Select
                                    key={dropdown.placeholder}
                                    placeholder={dropdown.placeholder}
                                    onChange={(value) => {
                                        if (dropdown.placeholder === "Select Company") {
                                            setSelectedCompany(value);
                                        } else if (dropdown.placeholder === "Select Query") {
                                            setSelectedQuery(value);
                                        }
                                    }}
                                    className="w-full border text-black rounded-xl px-3 py-4"
                                    options={dropdown.options.map((option) => ({
                                        label: option,
                                        value: option,
                                    }))}
                                />
                            </Form.Item>
                        ))}
                        <div className="w-full flex gap-4 justify-end">
                            <Form.Item>
                                <Button type="default"
                                    onClick={() => {
                                        setResult(null);
                                    }}
                                >
                                    Cancel
                                </Button>
                            </Form.Item>
                            <Form.Item>
                                <Button type="primary"
                                    onClick={handleSubmit}
                                    color="lime" variant="solid"
                                >
                                    {loading ? "Checking..." : "Check Greenwashing"}
                                </Button>
                            </Form.Item>
                        </div>
                        {error && (
                            <p className="text-red-500 text-sm">{error}</p>
                        )}
                    </Form>
                </div>

                {/* RIGHT RESULT PANEL */}
                <div className="overflow-scroll h-screen space-y-4">
                    <div className="bg-white rounded-2xl p-6 ">
                        <h2 className="text-xl font-semibold mb-4 text-gray-800">
                            Analysis Result
                        </h2>

                        {!loading && !result && (
                            <Ready />
                        )}

                        {loading && (
                            <LoadingAnalysis currentStatus={currentStatus} progress={progress} />
                        )}

                        {result && (
                            <div className="space-y-4">
                                <Chip label={result?.greenwashing_status || "No Result"} />

                                <div>
                                    <p className="text-sm text-gray-500">Claim Summary</p>
                                    <p className="text-gray-800">
                                        {result.company_claim_summary}
                                    </p>
                                </div>

                                <div>
                                    <p className="text-sm text-gray-500">Reason</p>
                                    <p className="text-gray-800">
                                        {result.reason_for_judgement[2]}
                                    </p>
                                </div>

                            </div>
                        )}
                    </div>
                    {result && (
                        <Evidence
                            companyName={selectedCompany}
                            query={selectedQuery}
                            supportingEvidence={result?.retrieved_documents.supportive_sources || []}
                            refutingEvidence={result?.retrieved_documents.counterfactual_sources || []}
                            companyClaimSummary={result?.retrieved_documents.company_reports || []}
                        />
                    )}
                </div>

            </div>

        </div>
    )
}

export default page