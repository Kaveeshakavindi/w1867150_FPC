import React from 'react'
import { motion } from 'motion/react';
import { Loader2 } from 'lucide-react';

const LoadingAnalysis = ({ currentStatus, progress }: { currentStatus: string; progress: number }) => {
  return (
    <div>
        <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                className="bg-white rounded-xl  p-12 flex flex-col items-center justify-center  text-center"
                >
                  <div className="flex flex-col items-center justify-center h-full">
                    {/* Pulsing Neural Network Graphic */}
                    <motion.div
                      animate={{ scale: [1, 1.1, 1] }}
                      transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
                      className="w-32 h-32 mb-8 relative"
                    >
                      <div className="absolute inset-0 bg-linear-to-br from-green-400 to-blue-400 rounded-full opacity-20 blur-xl" />
                      <div className="absolute inset-0 flex items-center justify-center">
                        <Loader2 className="w-16 h-16 text-green-600 animate-spin" />
                      </div>
                    </motion.div>

                    {/* Status Updates */}
                    <motion.div
                      key={currentStatus}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="text-center mb-8"
                    >
                      <h3 className="text-xl font-semibold mb-2">Analyzing Claims</h3>
                      <p className="text-gray-600">{currentStatus}</p>
                    </motion.div>

                    {/* Progress Bar */}
                    <div className="w-full max-w-md">
                      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${progress}%` }}
                          transition={{ duration: 0.3 }}
                          className="h-full bg-linear-to-r from-green-500 to-blue-500"
                        />
                      </div>
                      <p className="text-sm text-gray-500 mt-2 text-center">
                        {Math.round(progress)}% complete
                      </p>
                    </div>
                  </div>
                </motion.div>
    </div>
  )
}

export default LoadingAnalysis