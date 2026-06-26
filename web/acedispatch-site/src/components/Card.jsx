import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

const Card = ({ children, className }) => {
  return (
    <motion.div
      whileHover={{ y: -5, boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)' }}
      transition={{ duration: 0.3 }}
      className={cn(
        'bg-white rounded-xl shadow-lg p-6 md:p-8 transition-all duration-300',
        className
      )}
    >
      {children}
    </motion.div>
  );
};

export default Card;