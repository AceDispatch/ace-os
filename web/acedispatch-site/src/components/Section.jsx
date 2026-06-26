import React from 'react';
import { cn } from '@/lib/utils';

const Section = ({ children, className }) => {
  return (
    <section className={cn('py-16 px-4', className)}>
      <div className="max-w-7xl mx-auto">
        {children}
      </div>
    </section>
  );
};

export default Section;