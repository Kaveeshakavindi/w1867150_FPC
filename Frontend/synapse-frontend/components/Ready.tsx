import { AlertCircle } from 'lucide-react';
import { motion } from 'motion/react';
import React from 'react'

const Ready = () => {
    return (
        <div>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="bg-white rounded-xl  p-12 flex flex-col items-center justify-center  text-center"
            >
                    <AlertCircle className="w-12 h-12 text-green-600" />
                <h2 className="text-xl text-gray-800 font-semibold my-3">
                    Ready to Analyze
                </h2>
                <p className="text-gray-400 max-w-md text-sm">
                    Enter a company name and sustainability claim to begin the analysis.
                    Our AI will evaluate the claim using external evidence.
                </p>
            </motion.div>
        </div>
    )
}

export default Ready