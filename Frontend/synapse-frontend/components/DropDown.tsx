import React from 'react'

const DropDown = ({ selectedCompany, setSelectedCompany, companies }: { selectedCompany: string; setSelectedCompany: (company: string) => void; companies: string[]; }) => {
    return (
        <div className='mb-4'>
            <label className="block text-sm font-medium text-gray-700 py-2">
                Select Company
            </label>
            <select
                value={selectedCompany}
                onChange={(e) => setSelectedCompany(e.target.value)}
                className="w-full border border-gray-300 text-gray-700 rounded-xl px-3 py-3 bg-white"
                
            >
                <option value="">Choose a company</option>
                {companies.map((company) => (
                    <option key={company}>{company}</option>
                ))}
            </select>
        </div>
    )
}

export default DropDown