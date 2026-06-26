import React, { useState } from 'react';
import { Helmet } from 'react-helmet';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Phone, Mail, MapPin } from 'lucide-react';
import Section from '@/components/Section';
import Card from '@/components/Card';
import Button from '@/components/Button';
import { useToast } from '@/hooks/use-toast';

// HubSpot form endpoint (portal 245837044, form 924e9f4f..., region na2)
const HUBSPOT_SUBMIT_URL =
  'https://api.hsforms.com/submissions/v3/integration/submit/245837044/924e9f4f-dfad-4d37-8da7-e526c2c8b60b';

const ContactPage = () => {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    mcNumber: '',
    message: '',
    smsConsent: false,
  });

  const [errors, setErrors] = useState({});

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  const validatePhone = (phone) => {
    const re = /^[\d\s\-\(\)]+$/;
    return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validation
    const newErrors = {};
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone is required';
    } else if (!validatePhone(formData.phone)) {
      newErrors.phone = 'Please enter a valid phone number';
    }
    if (!formData.message.trim()) newErrors.message = 'Message is required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      toast({
        title: 'Validation Error',
        description: 'Please fill out all required fields correctly',
        variant: 'destructive',
      });
      return;
    }

    setIsSubmitting(true);

    try {
      // Include the MC# in the message body so nothing is lost
      const composedMessage = formData.mcNumber
        ? `MC#: ${formData.mcNumber}\n\n${formData.message}`
        : formData.message;

      // Build the HubSpot submission. SMS consent is only sent when the visitor
      // checks the box, so leads who don't opt in still come through.
      const fields = [
        { name: 'firstname', value: formData.name },
        { name: 'email', value: formData.email },
        { name: 'phone', value: formData.phone },
        { name: 'message', value: composedMessage },
      ];
      if (formData.smsConsent) {
        fields.push({ name: 'sms_consent', value: 'true' });
      }

      const response = await fetch(HUBSPOT_SUBMIT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          fields,
          context: {
            pageUri: typeof window !== 'undefined' ? window.location.href : 'https://www.acedispatch.us/contact',
            pageName: 'Contact - Ace Dispatch',
          },
        }),
      });

      if (!response.ok) {
        throw new Error(`HubSpot submission failed with status ${response.status}`);
      }

      toast({
        title: 'Message Sent Successfully!',
        description: "Thank you! We'll be in touch soon at the email you provided.",
      });

      // Reset form
      setFormData({
        name: '',
        email: '',
        phone: '',
        mcNumber: '',
        message: '',
        smsConsent: false,
      });
      setErrors({});
    } catch (error) {
      console.error('Form submission error:', error);
      toast({
        title: 'Error',
        description: 'Something went wrong. Please try calling us directly at (631) 807-3088.',
        variant: 'destructive',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <Helmet>
        <title>Contact Ace Dispatch - Get Started Today</title>
        <meta
          name="description"
          content="Contact Ace Dispatch to learn more about our dispatch services. We're here to help you succeed."
        />
      </Helmet>

      <Section className="bg-gradient-to-br from-gray-50 to-gray-100 py-16">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <h1 className="text-4xl md:text-5xl font-bold text-darkGray mb-4">
              Get in Touch
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Ready to simplify your dispatch? Fill out the form below and we'll get back to you within 24 hours.
            </p>
          </motion.div>

          <div className="grid lg:grid-cols-2 gap-8">
            {/* Contact Form */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <Card className="bg-white">
                <h2 className="text-2xl font-bold text-darkGray mb-6">Send Us a Message</h2>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-darkGray mb-2">
                      Name *
                    </label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      disabled={isSubmitting}
                      className={`w-full px-4 py-3 bg-white text-darkGray border ${
                        errors.name ? 'border-red-500' : 'border-gray-300'
                      } rounded-lg focus:ring-2 focus:ring-dispatchRed focus:border-transparent transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed`}
                      placeholder="Your full name"
                    />
                    {errors.name && <p className="mt-1 text-sm text-red-500">{errors.name}</p>}
                  </div>

                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-darkGray mb-2">
                      Email *
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      disabled={isSubmitting}
                      className={`w-full px-4 py-3 bg-white text-darkGray border ${
                        errors.email ? 'border-red-500' : 'border-gray-300'
                      } rounded-lg focus:ring-2 focus:ring-dispatchRed focus:border-transparent transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed`}
                      placeholder="your.email@example.com"
                    />
                    {errors.email && <p className="mt-1 text-sm text-red-500">{errors.email}</p>}
                  </div>

                  <div>
                    <label htmlFor="phone" className="block text-sm font-medium text-darkGray mb-2">
                      Phone *
                    </label>
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      disabled={isSubmitting}
                      className={`w-full px-4 py-3 bg-white text-darkGray border ${
                        errors.phone ? 'border-red-500' : 'border-gray-300'
                      } rounded-lg focus:ring-2 focus:ring-dispatchRed focus:border-transparent transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed`}
                      placeholder="(555) 123-4567"
                    />
                    {errors.phone && <p className="mt-1 text-sm text-red-500">{errors.phone}</p>}
                  </div>

                  <div>
                    <label htmlFor="mcNumber" className="block text-sm font-medium text-darkGray mb-2">
                      MC# (Motor Carrier Number)
                    </label>
                    <input
                      type="text"
                      id="mcNumber"
                      name="mcNumber"
                      value={formData.mcNumber}
                      onChange={handleChange}
                      disabled={isSubmitting}
                      className="w-full px-4 py-3 bg-white text-darkGray border border-gray-300 rounded-lg focus:ring-2 focus:ring-dispatchRed focus:border-transparent transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                      placeholder="MC-123456 (optional)"
                    />
                  </div>

                  <div>
                    <label htmlFor="message" className="block text-sm font-medium text-darkGray mb-2">
                      Message *
                    </label>
                    <textarea
                      id="message"
                      name="message"
                      value={formData.message}
                      onChange={handleChange}
                      disabled={isSubmitting}
                      rows="5"
                      className={`w-full px-4 py-3 bg-white text-darkGray border ${
                        errors.message ? 'border-red-500' : 'border-gray-300'
                      } rounded-lg focus:ring-2 focus:ring-dispatchRed focus:border-transparent transition-all duration-300 resize-none disabled:opacity-50 disabled:cursor-not-allowed`}
                      placeholder="Tell us about your needs..."
                    ></textarea>
                    {errors.message && <p className="mt-1 text-sm text-red-500">{errors.message}</p>}
                  </div>

                  <div className="flex items-start gap-3">
                    <input
                      type="checkbox"
                      id="smsConsent"
                      name="smsConsent"
                      checked={formData.smsConsent}
                      onChange={handleChange}
                      disabled={isSubmitting}
                      className="mt-1 h-4 w-4 flex-shrink-0 rounded border-gray-300 text-dispatchRed focus:ring-dispatchRed disabled:opacity-50 disabled:cursor-not-allowed"
                    />
                    <label htmlFor="smsConsent" className="text-xs text-gray-600 leading-relaxed">
                      I agree to receive text messages from Ace Dispatch at the number provided, about my inquiry and
                      services. Msg &amp; data rates may apply. Msg frequency varies. Reply STOP to opt out, HELP for
                      help. Consent is not a condition of any purchase. See our{' '}
                      <Link to="/privacy" className="text-dispatchRed hover:underline">Privacy Policy</Link> and{' '}
                      <Link to="/terms" className="text-dispatchRed hover:underline">Terms</Link>.
                    </label>
                  </div>

                  <Button type="submit" className="w-full" size="lg" disabled={isSubmitting}>
                    {isSubmitting ? 'Sending...' : 'Send Message'}
                  </Button>

                  <p className="text-xs text-gray-500 text-center mt-4">
                    Your message will be sent to <span className="font-medium text-dispatchRed">admin@acedispatch.us</span>
                  </p>
                </form>
              </Card>
            </motion.div>

            {/* Contact Information */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              <Card className="h-full bg-white">
                <h2 className="text-2xl font-bold text-darkGray mb-6">Contact Information</h2>
                <div className="space-y-6">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-dispatchRed/10 rounded-lg flex items-center justify-center flex-shrink-0">
                      <Phone className="w-6 h-6 text-dispatchRed" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-darkGray mb-1">Phone</h3>
                      <a href="tel:6318073088" className="text-gray-600 hover:text-dispatchRed transition-colors">
                        (631) 807-3088
                      </a>
                      <p className="text-sm text-gray-500">Available 24/7</p>
                    </div>
                  </div>

                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-dispatchRed/10 rounded-lg flex items-center justify-center flex-shrink-0">
                      <Mail className="w-6 h-6 text-dispatchRed" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-darkGray mb-1">Email</h3>
                      <a href="mailto:admin@acedispatch.us" className="text-gray-600 hover:text-dispatchRed transition-colors">
                        admin@acedispatch.us
                      </a>
                      <p className="text-sm text-gray-500">We'll respond within 24 hours</p>
                    </div>
                  </div>

                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-dispatchRed/10 rounded-lg flex items-center justify-center flex-shrink-0">
                      <MapPin className="w-6 h-6 text-dispatchRed" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-darkGray mb-1">Office</h3>
                      <p className="text-gray-600">236 Via D' Este #1402</p>
                      <p className="text-gray-600">Delray Beach, FL 33445</p>
                    </div>
                  </div>
                </div>

                <div className="mt-8 pt-8 border-t border-gray-200">
                  <h3 className="font-semibold text-darkGray mb-3">Business Hours</h3>
                  <div className="space-y-2 text-gray-600">
                    <p>Dispatch Services: 24/7</p>
                    <p>Office: Monday - Friday, 8am - 6pm EST</p>
                  </div>
                </div>
              </Card>
            </motion.div>
          </div>
        </div>
      </Section>
    </>
  );
};

export default ContactPage;
