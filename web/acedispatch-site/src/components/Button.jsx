import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

const Button = ({ 
  children, 
  onClick, 
  variant = 'primary', 
  size = 'md',
  type = 'button',
  className 
}) => {
  const baseStyles = 'font-semibold rounded-lg transition-all duration-300 inline-flex items-center justify-center';
  
  const variants = {
    primary: 'bg-dispatchRed text-white hover:bg-dispatchRed/90 shadow-lg hover:shadow-xl',
    secondary: 'bg-white text-dispatchRed border-2 border-dispatchRed hover:bg-dispatchRed hover:text-white shadow-md hover:shadow-lg',
  };

  const sizes = {
    sm: 'px-4 py-2 text-sm min-h-[36px]',
    md: 'px-6 py-3 text-base min-h-[44px]',
    lg: 'px-8 py-4 text-lg min-h-[52px]',
  };

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      type={type}
      className={cn(baseStyles, variants[variant], sizes[size], className)}
    >
      {children}
    </motion.button>
  );
};

export default Button;