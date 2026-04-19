import React from 'react';
import { motion } from 'framer-motion';

const fade = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.35, ease: [0.22, 1, 0.36, 1] },
};

export function PageMotion({ children, className }) {
  return (
    <motion.div className={className} {...fade}>
      {children}
    </motion.div>
  );
}

export function Stagger({ children, className, stagger = 0.06 }) {
  return (
    <motion.div
      className={className}
      initial="hidden"
      animate="show"
      variants={{
        hidden: {},
        show: {
          transition: { staggerChildren: stagger },
        },
      }}
    >
      {children}
    </motion.div>
  );
}

export function StaggerItem({ children, className }) {
  return (
    <motion.div
      className={className}
      variants={{
        hidden: { opacity: 0, y: 10 },
        show: { opacity: 1, y: 0, transition: { duration: 0.32 } },
      }}
    >
      {children}
    </motion.div>
  );
}
