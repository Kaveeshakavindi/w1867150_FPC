import React from 'react'

const Chip = ({ label }: { label: string }) => {
    const getClassificationColor = (greenwashing_status: string) => {
        switch (greenwashing_status) {
            case 'NotGreenwashing':
                return 'bg-green-100 text-green-800 border-green-300';
            case 'Greenwashing':
                return 'bg-red-100 text-red-800 border-red-300';
            default:
                return 'bg-yellow-100 text-yellow-800 border-yellow-300';
        }
    };
    return (
        <div>
            <span className={`px-4 py-2 rounded-full border-2 font-semibold text-sm ${getClassificationColor(label)}`}>
                {label}
            </span>
        </div>
    )
}

export default Chip