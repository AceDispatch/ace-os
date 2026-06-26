import React from 'react';
import { motion } from 'framer-motion';
import Button from '@/components/Button';

const Hero = ({ 
  image, 
  headline, 
  subheading, 
  ctaText, 
  ctaAction,
  variant = 'full' 
}) => {
  const isSmall = variant === 'small';

  return (
    <div className={`relative ${isSmall ? 'h-[400px]' : 'h-screen'} flex items-center justify-center overflow-hidden`}>
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center"
        style={{ backgroundImage: `url(${image})` }}
      >
        <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/50 to-black/70"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-5xl mx-auto px-4 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <h1 className={`${isSmall ? 'text-4xl md:text-5xl' : 'text-5xl md:text-7xl'} font-bold text-white mb-6 leading-tight`}>
            {headline}
          </h1>
          {subheading && (
            <p className={`${isSmall ? 'text-lg md:text-xl' : 'text-xl md:text-2xl'} text-gray-200 mb-8 max-w-3xl mx-auto`}>
              {subheading}
            </p>
          )}
          {ctaText && ctaAction && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              <Button onClick={ctaAction} size="lg">
                {ctaText}
              </Button>
            </motion.div>
          )}
        </motion.div>
      </div>

      {/* Decorative Elements */}
      <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-white to-transparent"></div>
    </div>
  );
};

export default Hero;