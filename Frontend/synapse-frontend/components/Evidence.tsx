import React, {useState} from 'react'
import { motion } from 'motion/react';
import { CheckCircle2, XCircle, AlertTriangle, ExternalLink, ChevronDown, ChevronUp } from 'lucide-react';

const Evidence = ({ supportingEvidence, refutingEvidence }: AnalysisResultsProps)  => {
    const [activeTab, setActiveTab] = useState<'supporting' | 'refuting'>('refuting');
  const [hoveredCitation, setHoveredCitation] = useState<number | null>(null);
  const [expandedStandards, setExpandedStandards] = useState<Set<string>>(new Set());

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

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'verified':
        return <CheckCircle2 className="w-5 h-5 text-green-600" />;
      case 'violation':
        return <XCircle className="w-5 h-5 text-red-600" />;
      default:
        return <AlertTriangle className="w-5 h-5 text-yellow-600" />;
    }
  };

  const toggleStandard = (standard: string) => {
    const newExpanded = new Set(expandedStandards);
    if (newExpanded.has(standard)) {
      newExpanded.delete(standard);
    } else {
      newExpanded.add(standard);
    }
    setExpandedStandards(newExpanded);
  };
  return (
    <div>{/* Evidence Sources Section */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-xl font-semibold mb-4 text-gray-800">Evidence Sources</h2>
        
        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b border-gray-200">
          <button
            onClick={() => setActiveTab('supporting')}
            className={`px-4 py-2 font-semibold transition-colors relative ${
              activeTab === 'supporting'
                ? 'text-green-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Supporting Evidence
            <span className="ml-2 px-2 py-0.5 rounded-full text-xs bg-gray-100">
              {supportingEvidence.length}
            </span>
            {activeTab === 'supporting' && (
              <motion.div
                layoutId="activeTab"
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-green-600"
              />
            )}
          </button>
          <button
            onClick={() => setActiveTab('refuting')}
            className={`px-4 py-2 font-semibold transition-colors relative ${
              activeTab === 'refuting'
                ? 'text-red-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Refuting Evidence
            <span className="ml-2 px-2 py-0.5 rounded-full text-xs bg-gray-100">
              {refutingEvidence.length}
            </span>
            {activeTab === 'refuting' && (
              <motion.div
                layoutId="activeTab"
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-red-600"
              />
            )}
          </button>
        </div>

        {/* Evidence Cards */}
        <div className="space-y-4">
          {(activeTab === 'supporting' ? supportingEvidence : refutingEvidence).map((evidence, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ 
                opacity: hoveredCitation === evidence.id ? 1 : 0.6,
                y: 0,
                scale: hoveredCitation === evidence.id ? 1.02 : 1,
              }}
              transition={{ duration: 0.2 }}
              className={`border rounded-lg p-4 ${
                hoveredCitation === evidence.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              } transition-all`}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="text-sm text-black">{evidence.title}</h4>
                  </div>
                </div>
                <a
                  href={evidence.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 transition-colors"
                >
                  <ExternalLink className="w-5 h-5" />
                </a>
              </div>
              <p className="text-gray-700 text-sm bg-gray-50 p-3 rounded border-l-4 border-gray-300">
                "{evidence.article}"
              </p>
            </motion.div>
          ))}
        </div>
      </div></div>
  )
}

export default Evidence