'use client'

import React, {useState} from 'react'
import { motion, Reorder } from 'motion/react';
import { Plus, X, GripVertical, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, LineChart, Line } from 'recharts';


interface CompanyData {
  id: string;
  name: string;
  riskScore: number;
  classification: 'Verified' | 'Insufficient Evidence' | 'Misleading';
  esgScores: {
    environmental: number;
    social: number;
    governance: number;
  };
}

const AVAILABLE_COMPANIES = [
  'Shell International',
  'BP Energy',
  'TotalEnergies',
  'Chevron Corporation',
  'Tesla Inc.',
  'Amazon Inc.',
  'Apple Inc.',
  'Microsoft Corporation',
];

const MOCK_COMPANY_DATA: Record<string, CompanyData> = {
  'Shell International': {
    id: '1',
    name: 'Shell International',
    riskScore: 78,
    classification: 'Misleading',
    esgScores: { environmental: 45, social: 62, governance: 58 },
  },
  'BP Energy': {
    id: '2',
    name: 'BP Energy',
    riskScore: 72,
    classification: 'Misleading',
    esgScores: { environmental: 48, social: 65, governance: 61 },
  },
  'Tesla Inc.': {
    id: '3',
    name: 'Tesla Inc.',
    riskScore: 35,
    classification: 'Insufficient Evidence',
    esgScores: { environmental: 82, social: 58, governance: 54 },
  },
  'Apple Inc.': {
    id: '4',
    name: 'Apple Inc.',
    riskScore: 25,
    classification: 'Verified',
    esgScores: { environmental: 88, social: 79, governance: 85 },
  },
};

const TIMELINE_DATA = [
  { month: 'Jan', shell: 76, bp: 70, tesla: 38, apple: 28 },
  { month: 'Feb', shell: 77, bp: 71, tesla: 36, apple: 26 },
  { month: 'Mar', shell: 78, bp: 72, tesla: 35, apple: 25 },
];

const page = () => {
    const [selectedCompanies, setSelectedCompanies] = useState<CompanyData[]>([
    MOCK_COMPANY_DATA['Shell International'],
  ]);
  const [showAddMenu, setShowAddMenu] = useState(false);
  const [filterRisk, setFilterRisk] = useState<string>('all');
  const [filterPillar, setFilterPillar] = useState<string>('all');

  const addCompany = (companyName: string) => {
    if (selectedCompanies.length >= 4) return;
    const companyData = MOCK_COMPANY_DATA[companyName];
    if (companyData && !selectedCompanies.find(c => c.name === companyName)) {
      setSelectedCompanies([...selectedCompanies, companyData]);
    }
    setShowAddMenu(false);
  };

  const removeCompany = (companyId: string) => {
    setSelectedCompanies(selectedCompanies.filter(c => c.id !== companyId));
  };

  const getRiskColor = (score: number) => {
    if (score < 40) return 'text-green-600';
    if (score < 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getClassificationColor = (classification: string) => {
    switch (classification) {
      case 'Verified':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'Misleading':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
    }
  };

  // Prepare data for charts
  const riskScoreData = selectedCompanies.map(company => ({
    name: company.name.split(' ')[0],
    score: company.riskScore,
  }));

  const radarData = [
    {
      pillar: 'Environmental',
      ...Object.fromEntries(selectedCompanies.map(c => [c.name.split(' ')[0], c.esgScores.environmental])),
    },
    {
      pillar: 'Social',
      ...Object.fromEntries(selectedCompanies.map(c => [c.name.split(' ')[0], c.esgScores.social])),
    },
    {
      pillar: 'Governance',
      ...Object.fromEntries(selectedCompanies.map(c => [c.name.split(' ')[0], c.esgScores.governance])),
    },
  ];

  const COLORS = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b'];
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-6">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Comparison Dashboard</h1>
          <p className="text-gray-600">
            Compare greenwashing risk and ESG performance across multiple companies
          </p>
        </div>

        {/* Company Selection */}
        <div className="mb-8">
          <div className="flex items-center gap-4 mb-4">
            <h2 className="text-xl font-semibold">Selected Companies</h2>
            {selectedCompanies.length < 4 && (
              <div className="relative">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setShowAddMenu(!showAddMenu)}
                  className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  Add Company
                </motion.button>

                {showAddMenu && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="absolute top-full left-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-10"
                  >
                    {AVAILABLE_COMPANIES.filter(
                      company => !selectedCompanies.find(c => c.name === company)
                    ).map((company, index) => (
                      <button
                        key={index}
                        onClick={() => addCompany(company)}
                        className="w-full px-4 py-2 text-left hover:bg-gray-50 transition-colors"
                      >
                        {company}
                      </button>
                    ))}
                  </motion.div>
                )}
              </div>
            )}
            <span className="text-sm text-gray-500">
              ({selectedCompanies.length}/4 companies selected)
            </span>
          </div>

          {/* Company Cards - Draggable */}
          <Reorder.Group
            axis="x"
            values={selectedCompanies}
            onReorder={setSelectedCompanies}
            className="flex gap-4 overflow-x-auto pb-4"
          >
            {selectedCompanies.map((company) => (
              <Reorder.Item
                key={company.id}
                value={company}
                className="shrink-0"
              >
                <motion.div
                  layout
                  className="w-64 bg-white rounded-xl shadow-lg p-6 cursor-move relative"
                >
                  <div className="absolute top-2 left-2 text-gray-400">
                    <GripVertical className="w-5 h-5" />
                  </div>
                  <button
                    onClick={() => removeCompany(company.id)}
                    className="absolute top-2 right-2 p-1 rounded-full hover:bg-gray-100 transition-colors"
                  >
                    <X className="w-4 h-4 text-gray-500" />
                  </button>

                  <div className="mt-6 mb-4">
                    <h3 className="font-bold text-lg mb-2">{company.name}</h3>
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold border ${getClassificationColor(company.classification)}`}>
                      {company.classification}
                    </span>
                  </div>

                  <div className="space-y-3">
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-gray-600">Risk Score</span>
                        <span className={`text-2xl font-bold ${getRiskColor(company.riskScore)}`}>
                          {company.riskScore}
                        </span>
                      </div>
                      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className={`h-full ${company.riskScore < 40 ? 'bg-green-500' : company.riskScore < 70 ? 'bg-yellow-500' : 'bg-red-500'}`}
                          style={{ width: `${company.riskScore}%` }}
                        />
                      </div>
                    </div>

                    <div className="pt-3 border-t border-gray-200">
                      <div className="text-xs text-gray-600 mb-2">ESG Scores</div>
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-xs">Environmental</span>
                          <span className="text-xs font-semibold">{company.esgScores.environmental}</span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-xs">Social</span>
                          <span className="text-xs font-semibold">{company.esgScores.social}</span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-xs">Governance</span>
                          <span className="text-xs font-semibold">{company.esgScores.governance}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              </Reorder.Item>
            ))}
          </Reorder.Group>
        </div>

        

        {/* Comparative Visualizations */}
        {selectedCompanies.length > 0 && (
          <div className="space-y-8">
            {/* Risk Scores Bar Chart */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-xl shadow-lg p-8"
            >
              <h2 className="text-2xl font-bold mb-6">Greenwashing Risk Comparison</h2>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={riskScoreData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="score" fill="#10b981" name="Risk Score" />
                </BarChart>
              </ResponsiveContainer>
            </motion.div>

           
            
          </div>
        )}

        
      </div>
    </div>
  )
}

export default page