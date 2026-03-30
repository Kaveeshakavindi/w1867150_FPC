import React from 'react'
import { ChevronRight, Info, Loader2, AlertCircle, CheckCircle2, XCircle, ExternalLink, ChevronDown, ChevronUp } from 'lucide-react';

const BreadCrumb = ({prev, current}: {prev: string, current: string}) => {
    return (
        <div className="flex items-center gap-2 text-sm text-gray-600 mb-6">
            <span>{prev}</span>
            <ChevronRight className="w-4 h-4" />
            <span className="text-green-600">{current}</span>
        </div>
    )
}

export default BreadCrumb