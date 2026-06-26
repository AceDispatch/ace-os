import React from 'react';
import { Helmet } from 'react-helmet';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ExternalLink, Clock } from 'lucide-react';
import Section from '@/components/Section';
import Card from '@/components/Card';
import Button from '@/components/Button';

const OnboardingPage = () => {
  const navigate = useNavigate();

  const handleRedirect = () => {
    navigate('/contact');
  };

  return (
    <>
      <Helmet>
        <title>Carrier Onboarding - Ace Dispatch</title>
        <meta
          name="description"
          content="Get started with Ace Dispatch. Complete our onboarding process to begin your dispatch services."
        />
      </Helmet>

      <Section className="bg-gradient-to-br from-gray-50 to-gray-100 min-h-[80vh] flex items-center">
        <div className="max-w-3xl mx-auto w-full">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Card className="bg-white text-center">
              <div className="flex justify-center mb-6">
                <div className="w-20 h-20 bg-dispatchRed/10 rounded-full flex items-center justify-center">
                  <Clock className="w-10 h-10 text-dispatchRed" />
                </div>
              </div>

              <h1 className="text-4xl md:text-5xl font-bold text-darkGray mb-4">
                Carrier Onboarding Portal
              </h1>
              
              <p className="text-lg text-gray-600 mb-8">
                We're preparing our streamlined onboarding experience to get you on the road faster than ever.
              </p>

              <div className="bg-gray-50 rounded-lg p-6 mb-8">
                <h2 className="text-xl font-bold text-darkGray mb-4">What You'll Need:</h2>
                <ul className="text-left space-y-3 text-gray-700">
                  <li className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 bg-dispatchRed rounded-full mt-2 flex-shrink-0"></div>
                    <span>MC Authority and DOT numbers</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 bg-dispatchRed rounded-full mt-2 flex-shrink-0"></div>
                    <span>Current insurance certificates</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 bg-dispatchRed rounded-full mt-2 flex-shrink-0"></div>
                    <span>Vehicle information and specifications</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 bg-dispatchRed rounded-full mt-2 flex-shrink-0"></div>
                    <span>Preferred lanes and routes</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 bg-dispatchRed rounded-full mt-2 flex-shrink-0"></div>
                    <span>W-9 form for payment processing</span>
                  </li>
                </ul>
              </div>

              <Button onClick={handleRedirect} size="lg" className="mb-4">
                <ExternalLink className="w-5 h-5 mr-2" />
                Access Onboarding Portal
              </Button>

              <p className="text-sm text-gray-500">
                Need assistance? Contact us at <a href="tel:6318073088" className="text-dispatchRed hover:underline">(631) 807-3088</a> or <a href="mailto:admin@acedispatch.us" className="text-dispatchRed hover:underline">admin@acedispatch.us</a>
              </p>
            </Card>
          </motion.div>
        </div>
      </Section>
    </>
  );
};

export default OnboardingPage;