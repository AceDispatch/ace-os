import React from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { Shield, Users, TrendingUp, Award } from 'lucide-react';
import Hero from '@/components/Hero';
import Section from '@/components/Section';
import Card from '@/components/Card';
import Button from '@/components/Button';
import { useNavigate } from 'react-router-dom';

const AboutPage = () => {
  const navigate = useNavigate();

  const values = [
    {
      icon: Shield,
      title: 'Reliability',
      description: 'We\'re available 24/7 to support you on the road. Count on us to be there when you need us most.'
    },
    {
      icon: Users,
      title: 'Transparency',
      description: 'Clear communication, honest rates, and no hidden fees. You always know exactly what you\'re getting.'
    },
    {
      icon: TrendingUp,
      title: 'Support',
      description: 'Your success is our success. We\'re invested in helping you grow your business and maximize earnings.'
    },
    {
      icon: Award,
      title: 'Expertise',
      description: 'Years of industry experience and deep freight market knowledge working for you every single day.'
    }
  ];

  return (
    <>
      <Helmet>
        <title>About Ace Dispatch - Your Long-Term Dispatch Partner</title>
        <meta
          name="description"
          content="Learn about Ace Dispatch - a dedicated dispatch service partner for owner-operators, not a load board or broker."
        />
      </Helmet>

      {/* Hero Section */}
      <Hero
        image="https://images.unsplash.com/photo-1618914241697-13c434a6ba53"
        headline="About Ace Dispatch"
        subheading="Your trusted partner in professional dispatch services"
        variant="small"
      />

      {/* Company Story Section */}
      <Section className="bg-white">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-darkGray mb-8 text-center">
              Our Story
            </h2>
            <div className="space-y-6 text-lg text-gray-700">
              <p>
                <span className="text-dispatchRed font-semibold">Ace</span> <span className="text-darkGray font-semibold">Dispatch</span> was founded with a simple mission: to help owner-operators and small fleets succeed by taking the stress out of dispatch. Through refined tactics, proven tools, and a team that genuinely cares, we support you at every step of the journey.
              </p>
              <p>
                As a company we strive to set the standard for U.S. dispatching through accountability, compliance, and a commitment to doing things the right way. We bring peace of mind to brokers and shippers by holding our carrier relationships to a higher standard, ensuring every shipment is handled with professionalism, transparency, and care.
              </p>
              <p>
                Every carrier we work with gets personalized service from a dedicated dispatcher who knows their routes, preferences, and business goals. We negotiate the best rates, find the right loads, and handle all the administrative work so you can focus on the road ahead.
              </p>
            </div>
          </motion.div>
        </div>
      </Section>

      {/* Positioning Section */}
      <Section className="bg-gradient-to-br from-gray-50 to-gray-100">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="max-w-4xl mx-auto"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-darkGray mb-8 text-center">
            What Makes Us Different
          </h2>
          <Card className="bg-white">
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-bold text-dispatchRed mb-3">We Build The Route That's Right For YOU</h3>
                <p className="text-gray-700">
                  Our load finding philosophy revolves around building out your entire weeks route plan, and customizing that plan to fit your scheduling needs, so you're home when you want, and making the most along the way!
                </p>
              </div>
              <div className="w-full h-px bg-gray-200"></div>
              <div>
                <h3 className="text-2xl font-bold text-dispatchRed mb-3">We Develop Relationships On YOUR Behalf</h3>
                <p className="text-gray-700">
                  We represent your operation directly, helping build and maintain trusted shipper relationships in a compliant, professional way, creating consistency and long-term opportunity for every carrier we work with.
                </p>
              </div>
              <div className="w-full h-px bg-gray-200"></div>
              <div>
                <h3 className="text-2xl font-bold text-dispatchRed mb-3">We're NOT Just Software</h3>
                <p className="text-gray-700">
                  While we do employ cutting edge technology, we're real people providing personalized service. You'll have a dedicated dispatcher who knows your business and advocates for you every single day.
                </p>
              </div>
              <div className="w-full h-px bg-gray-200"></div>
              <div>
                <h3 className="text-2xl font-bold text-dispatchRed mb-3">We ARE Your Long-Term Partner</h3>
                <p className="text-gray-700">
                  We're invested in your business beyond day-to-day dispatch. Our role isn't just to run your loads, it's to help you scale into the future, building a plan that's tailored specifically to your operation.
                </p>
              </div>
            </div>
          </Card>
        </motion.div>
      </Section>

      {/* Values Section */}
      <Section className="bg-white">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-darkGray mb-4">
            Our Core Values
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            These principles guide everything we do at <span className="text-dispatchRed">Ace</span> <span className="text-darkGray">Dispatch</span>
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {values.map((value, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <Card className="h-full text-center">
                <div className="flex flex-col items-center">
                  <div className="w-16 h-16 bg-dispatchRed/10 rounded-full flex items-center justify-center mb-4">
                    <value.icon className="w-8 h-8 text-dispatchRed" />
                  </div>
                  <h3 className="text-xl font-bold text-darkGray mb-3">{value.title}</h3>
                  <p className="text-gray-600">{value.description}</p>
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
            Partner With Us
          </h2>
          <p className="text-lg text-gray-300 mb-8">
            Ready to experience dispatch services that truly put you first? Let\'s start a conversation.
          </p>
          <Button onClick={() => navigate('/contact')} size="lg">
            Contact Us Today
          </Button>
        </motion.div>
      </Section>
    </>
  );
};

export default AboutPage;