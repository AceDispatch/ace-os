import React from 'react';
import { Helmet } from 'react-helmet';
import { Link } from 'react-router-dom';
import Section from '@/components/Section';

const PrivacyPolicyPage = () => {
  return (
    <>
      <Helmet>
        <title>Privacy Policy - Ace Dispatch</title>
        <meta
          name="description"
          content="Privacy Policy for Ace Dispatch (A&C Consulting Group LLC). We never share or sell your mobile information or SMS consent with third parties for marketing."
        />
      </Helmet>

      <Section className="bg-white">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold text-darkGray mb-2">Privacy Policy</h1>
          <p className="text-gray-500 mb-2">A&amp;C Consulting Group LLC d/b/a Ace Dispatch</p>
          <p className="text-gray-500 mb-10">Last updated: June 21, 2026</p>

          <div className="space-y-8 text-gray-700 leading-relaxed">
            <p>
              This Privacy Policy explains how A&amp;C Consulting Group LLC, doing business as Ace Dispatch ("Ace
              Dispatch," "we," "us," or "our"), collects, uses, and protects your information when you visit acedispatch.us,
              contact us, or use our dispatch services. By using our website or services, you agree to this Policy.
            </p>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">Information We Collect</h2>
              <p className="mb-3">We collect information you provide directly and information collected automatically:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>
                  <strong>Information you give us:</strong> name, email address, phone and mobile number, mailing address,
                  motor carrier (MC) number, company information, and the contents of messages you send us through our
                  contact form, by phone, or by text.
                </li>
                <li>
                  <strong>Information collected automatically:</strong> basic usage and device data such as IP address,
                  browser type, and pages visited, collected through cookies and similar technologies.
                </li>
              </ul>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">How We Use Your Information</h2>
              <p className="mb-3">We use your information to:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>respond to your inquiries and provide quotes;</li>
                <li>provide and manage dispatch and related services;</li>
                <li>communicate with you by phone, email, and (with your consent) text message;</li>
                <li>handle onboarding, paperwork, billing, and support;</li>
                <li>operate, secure, and improve our website and services; and</li>
                <li>comply with our legal obligations.</li>
              </ul>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">SMS / Text Messaging Terms &amp; Consent</h2>
              <p className="mb-4">
                When you provide your mobile number to Ace Dispatch &mdash; by giving it to one of our representatives
                during a call, by texting us first, or by submitting it through a form on acedispatch.us and agreeing to
                be contacted &mdash; you consent to receive text messages from us about your inquiry, your account,
                quotes, dispatching and load coordination, scheduling, and customer support.
              </p>
              <ul className="list-disc pl-6 space-y-2">
                <li>Message frequency varies. Message and data rates may apply.</li>
                <li>
                  Reply <strong>STOP</strong> to opt out at any time. Reply <strong>HELP</strong> for help, or contact
                  admin@acedispatch.us.
                </li>
                <li>
                  <strong>
                    Your mobile opt-in information and consent are never shared with or sold to third parties or
                    affiliates for marketing or promotional purposes. Text-messaging originator opt-in data and consent
                    are not shared with any third parties under any circumstances.
                  </strong>
                </li>
                <li>Wireless carriers are not liable for delayed or undelivered messages.</li>
              </ul>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">How We Share Information</h2>
              <p className="mb-3">
                We do <strong>not</strong> sell your personal information, and we do <strong>not</strong> share your
                personal information with third parties or affiliates for their own marketing or advertising purposes. We
                share personal information only:
              </p>
              <ul className="list-disc pl-6 space-y-2">
                <li>
                  with service providers who perform functions on our behalf (for example, our telephone/SMS provider,
                  our CRM, and our payment processor), and only as needed to provide our services to you;
                </li>
                <li>in connection with a business transfer (merger, acquisition, or sale of assets); or</li>
                <li>when required by law or to protect our legal rights.</li>
              </ul>
              <p className="mt-3">
                We may share aggregated or anonymized, non-personal data for analytics.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">Cookies and Analytics</h2>
              <p>
                We use cookies and similar technologies to operate the website, remember preferences, and understand how
                the site is used. You can block or disable cookies in your browser settings, though some features may not
                work as intended.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">Data Retention</h2>
              <p>
                We keep your information for as long as needed to provide our services, comply with our legal obligations,
                resolve disputes, and enforce our agreements. When information is no longer needed, we take reasonable
                steps to delete or de-identify it.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">How We Protect Your Information</h2>
              <p>
                We use reasonable administrative, technical, and physical safeguards to protect your information. No
                method of transmission or storage is completely secure, however, and we cannot guarantee absolute
                security.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">Your Rights and Choices</h2>
              <p>
                Depending on where you live, you may have the right to access, correct, or delete your personal
                information, or to opt out of certain processing. To make a request, contact us at admin@acedispatch.us.
                California residents may request information about the categories of personal information we collect and
                how it is used; as stated above, we do not sell personal information. You can opt out of text messages at
                any time by replying STOP.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">Third-Party Links</h2>
              <p>
                Our website may link to third-party sites we do not control. We are not responsible for their content or
                privacy practices, and we encourage you to review their policies.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">Children's Privacy</h2>
              <p>
                Our website and services are intended for businesses and individuals 18 and older. We do not knowingly
                collect personal information from children.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">Changes to This Policy</h2>
              <p>
                We may update this Privacy Policy from time to time. Changes are effective when posted, and the "Last
                updated" date above will be revised. Your continued use of the website or services after changes are
                posted constitutes acceptance.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">Contact Us</h2>
              <p>
                A&amp;C Consulting Group LLC d/b/a Ace Dispatch<br />
                Email: admin@acedispatch.us<br />
                Website: acedispatch.us<br />
                236 Via D' Este #1402, Delray Beach, FL 33445
              </p>
              <p className="mt-3">
                See also our <Link to="/terms" className="text-dispatchRed hover:underline">Terms of Service</Link>.
              </p>
            </div>
          </div>
        </div>
      </Section>
    </>
  );
};

export default PrivacyPolicyPage;
