import React from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { Truck, DollarSign, FileText } from 'lucide-react';
import Section from '@/components/Section';
import Card from '@/components/Card';
import Button from '@/components/Button';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();

  const problems = [
    {
      icon: Truck,
      title: 'Finding Quality Loads',
      problem: 'Spending hours searching for loads that match your routes',
      solution: 'We match you with quality loads that fit your capacity and preferences',
    },
    {
      icon: DollarSign,
      title: 'Rate Negotiation',
      problem: 'Leaving money on the table with poor rate negotiations',
      solution: 'Our experts negotiate competitive rates so you earn what you deserve',
    },
    {
      icon: FileText,
      title: 'Paperwork Overload',
      problem: 'Drowning in documentation, compliance, and logistics management',
      solution: 'We handle all paperwork, compliance, and administrative tasks for you',
    },
  ];

  return (
    <>
      <Helmet>
        <title>Ace Dispatch - Professional Dispatch Services for Owner-Operators</title>
        <meta
          name="description"
          content="Focus on driving. We handle the loads, rates, and paperwork. Professional dispatch services for owner-operators and small fleets."
        />
      </Helmet>

      {/* Hero Section */}
      <div className="relative h-screen flex items-center justify-center overflow-hidden">
        {/* Background Image */}
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{ backgroundImage: 'url(https://images.unsplash.com/photo-1509082806432-f945e11c4deb)' }}
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
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-4 leading-tight">
              The <span className="text-dispatchRed">Ace</span> <span className="text-white">Standard</span> in <span className="text-gray-300">Dispatching</span>
            </h1>
            <p className="text-2xl md:text-3xl text-gray-200 italic font-light mb-8 tracking-wide">
              A driving partner in growth
            </p>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              <Button onClick={() => navigate('/contact')} size="lg">
                Get Started
              </Button>
            </motion.div>
          </motion.div>
        </div>

        {/* Decorative Elements */}
        <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-white to-transparent"></div>
      </div>

      {/* Problem/Solution Section */}
      <Section className="bg-white">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-darkGray mb-4">
            Why Choose <span className="text-dispatchRed">Ace</span> <span className="text-darkGray">Dispatch</span>?
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            We understand the challenges you face. Let us handle the headaches while you focus on the road.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {problems.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <Card className="h-full">
                <div className="flex flex-col items-center text-center">
                  <div className="w-16 h-16 bg-dispatchRed/10 rounded-full flex items-center justify-center mb-4">
                    <item.icon className="w-8 h-8 text-dispatchRed" />
                  </div>
                  <h3 className="text-xl font-bold text-darkGray mb-3">{item.title}</h3>
                  <p className="text-gray-600 mb-4 italic">"{item.problem}"</p>
                  <div className="w-12 h-1 bg-dispatchRed mb-4"></div>
                  <p className="text-gray-700 font-medium">{item.solution}</p>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </Section>

      {/* Final CTA Section */}
      <Section className="bg-white">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-3xl mx-auto"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-darkGray mb-6">
            Ready to Simplify Your Dispatch?
          </h2>
          <p className="text-lg text-gray-600 mb-8">
            Stop wasting time on paperwork and load searching. Partner with <span className="text-dispatchRed">Ace</span> <span className="text-darkGray">Dispatch</span> and focus on what you do best - driving.
          </p>
          <Button onClick={() => navigate('/contact')} size="lg">
            Start Dispatching Today
          </Button>
        </motion.div>
      </Section>
    </>
  );
};

export default HomePage;