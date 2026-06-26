import React from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { Search, DollarSign, FileCheck, Heart } from 'lucide-react';
import Hero from '@/components/Hero';
import Section from '@/components/Section';
import Card from '@/components/Card';
import Button from '@/components/Button';
import { useNavigate } from 'react-router-dom';

const ServicesPage = () => {
  const navigate = useNavigate();

  const services = [
    {
      icon: Search,
      title: 'Load Finding',
      description: 'Access to quality loads matched to your capacity and routes',
      benefits: [
        'Personalized load matching based on your preferences',
        'Access to exclusive freight networks',
        'Consistent load flow to keep you moving',
        'Deadhead reduction strategies',
      ],
    },
    {
      icon: DollarSign,
      title: 'Rate Negotiation',
      description: 'We negotiate rates so you get fair compensation',
      benefits: [
        'Expert negotiators on your side',
        'Market-based rate analysis',
        'Maximize your revenue per mile',
        'Transparent rate breakdowns',
      ],
    },
    {
      icon: FileCheck,
      title: 'Paperwork Management',
      description: 'Documentation, compliance, and logistics handled',
      benefits: [
        'All documentation managed for you',
        'Compliance monitoring and updates',
        'Invoice processing and follow-up',
        'Digital record keeping',
      ],
    },
    {
      icon: Heart,
      title: 'Stress Reduction',
      description: 'Dedicated support so you focus on what you do best',
      benefits: [
        '24/7 dispatcher availability',
        'Personal account manager',
        'Proactive problem solving',
        'Peace of mind on the road',
      ],
    },
  ];

  return (
    <>
      <Helmet>
        <title>Our Dispatch Services - Ace Dispatch</title>
        <meta
          name="description"
          content="Comprehensive dispatch services including load finding, rate negotiation, paperwork management, and dedicated support for owner-operators."
        />
      </Helmet>

      {/* Hero Section */}
      <Hero
        image="https://images.unsplash.com/photo-1688413399498-e35ed74b554f"
        headline="Our Dispatch Services"
        subheading="Comprehensive solutions to keep you moving and profitable"
        variant="small"
      />

      {/* Services Grid */}
      <Section className="bg-white">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-darkGray mb-4">
            What We Do for You
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            From finding loads to managing paperwork, we handle it all so you can focus on driving
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8">
          {services.map((service, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <Card className="h-full group">
                <div className="flex flex-col h-full">
                  <div className="flex items-start gap-4 mb-4">
                    <div className="w-14 h-14 bg-dispatchRed/10 rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform duration-300">
                      <service.icon className="w-7 h-7 text-dispatchRed" />
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-darkGray mb-2">{service.title}</h3>
                      <p className="text-gray-600">{service.description}</p>
                    </div>
                  </div>
                  <div className="mt-4">
                    <h4 className="font-semibold text-darkGray mb-3">Key Benefits:</h4>
                    <ul className="space-y-2">
                      {service.benefits.map((benefit, idx) => (
                        <li key={idx} className="flex items-start gap-2">
                          <div className="w-1.5 h-1.5 bg-dispatchRed rounded-full mt-2 flex-shrink-0"></div>
                          <span className="text-gray-700">{benefit}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </Section>

      {/* CTA Section */}
      <Section className="bg-gradient-to-br from-darkGray to-gray-800">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-3xl mx-auto"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to Get Started?
          </h2>
          <p className="text-lg text-gray-300 mb-8">
            Let's discuss how our dispatch services can help grow your business
          </p>
          <Button onClick={() => navigate('/contact')} size="lg">
            Request Dispatch Services
          </Button>
        </motion.div>
      </Section>
    </>
  );
};

export default ServicesPage;