import React from 'react';
import { Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

const LoadingSpinner = ({ message = 'Loading' }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 gap-6 min-h-[40vh]">
      <div className="relative h-16 w-16">
        <motion.span
          className="absolute inset-0 rounded-full border-2 border-cyan-500/20"
          animate={{ rotate: 360 }}
          transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
        />
        <motion.span
          className="absolute inset-1 rounded-full border-2 border-transparent border-t-cyan-400/80 border-r-violet-500/50"
          animate={{ rotate: -360 }}
          transition={{ duration: 1.2, repeat: Infinity, ease: 'linear' }}
        />
        <div className="absolute inset-0 flex items-center justify-center">
          <Loader2 className="h-7 w-7 text-cyan-400 animate-spin" aria-hidden />
        </div>
      </div>
      <motion.p
        className="text-sm text-zinc-400 font-medium tracking-wide text-center max-w-xs"
        initial={{ opacity: 0.6 }}
        animate={{ opacity: [0.6, 1, 0.6] }}
        transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
      >
        {message}
      </motion.p>
    </div>
  );
};

export default LoadingSpinner;
