import React from 'react';
import { Helmet } from 'react-helmet';
import { Link } from 'react-router-dom';
import Section from '@/components/Section';

const TermsPage = () => {
  return (
    <>
      <Helmet>
        <title>Terms of Service - Ace Dispatch</title>
        <meta
          name="description"
          content="Terms of Service for Ace Dispatch (A&C Consulting Group LLC), including our SMS/text messaging program terms."
        />
      </Helmet>

      <Section className="bg-white">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold text-darkGray mb-2">Terms of Service</h1>
          <p className="text-gray-500 mb-2">A&amp;C Consulting Group LLC d/b/a Ace Dispatch</p>
          <p className="text-gray-500 mb-10">Effective date: June 21, 2026</p>

          <div className="space-y-8 text-gray-700 leading-relaxed">
            <p>
              These Terms of Service ("Terms") govern your access to and use of the website at acedispatch.us and the
              services provided by A&amp;C Consulting Group LLC, doing business as Ace Dispatch ("Ace Dispatch," "we,"
              "us," or "our"). By accessing our website, contacting us, or using our services, you agree to these Terms.
              If you do not agree, do not use our website or services.
            </p>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">1. Our Services</h2>
              <p>
                Ace Dispatch provides truck dispatching and related sales and back-office support services to motor
                carriers, including locating freight, negotiating rates, coordinating loads, and handling related
                administrative tasks. We are not a motor carrier, a freight broker, a freight forwarder, or an insurer,
                and we do not assume the legal responsibilities of those parties unless separately and expressly licensed
                to do so. Specific services, fees, and terms for paying clients are set out in a separate service
                agreement.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">2. Eligibility</h2>
              <p>
                You must be at least 18 years old and authorized to act on behalf of the business you represent. By using
                our services you represent that the information you provide is accurate and that you have authority to
                enter into these Terms.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">3. Accounts and Information</h2>
              <p>
                You agree to provide accurate, current, and complete information and to keep it updated. You are
                responsible for activity conducted through your account or on your behalf.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">4. Text Messaging (SMS) Program</h2>
              <p className="mb-4">
                By providing your mobile number and opting in &mdash; verbally to one of our representatives, by texting
                us first, or by checking the SMS consent box on a form at acedispatch.us &mdash; you agree to receive
                text messages from Ace Dispatch related to your inquiry, your account, freight rate quotes, dispatching
                and load coordination, scheduling, onboarding, and customer support.
              </p>
              <ul className="list-disc pl-6 space-y-2 mb-4">
                <li>Message frequency varies.</li>
                <li>Message and data rates may apply.</li>
                <li>
                  You can opt out at any time by replying <strong>STOP</strong>; reply <strong>HELP</strong> for help, or
                  contact admin@acedispatch.us.
                </li>
                <li>
                  <strong>
                    Your mobile information and SMS consent are never sold or shared with third parties or affiliates for
                    marketing or promotional purposes.
                  </strong>
                </li>
                <li>Wireless carriers are not liable for delayed or undelivered messages.</li>
              </ul>
              <p>
                Consent to receive text messages is not a condition of purchasing any goods or services. For more detail
                on how we handle your information, see our <Link to="/privacy" className="text-dispatchRed hover:underline">Privacy Policy</Link>.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">5. Fees and Payment</h2>
              <p>
                Where services are provided for a fee, the charges, billing cycle, and payment terms are described in your
                service agreement or order. You authorize us (and our payment processor) to charge the payment method you
                provide for amounts due. Except as required by law or expressly stated, fees are non-refundable.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">6. Acceptable Use</h2>
              <p>
                You agree not to use our website or services to: violate any law or regulation; infringe the rights of
                others; transmit false, misleading, or fraudulent information; interfere with or disrupt the website or
                its security; or attempt unauthorized access to any system or data.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">7. Intellectual Property</h2>
              <p>
                The website and its content &mdash; text, graphics, logos, and the "Ace Dispatch" name and marks &mdash;
                are owned by or licensed to us and protected by intellectual-property laws. You may not copy, reproduce,
                or use them without our prior written permission.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">8. Third-Party Links and Services</h2>
              <p>
                Our website may link to or rely on third-party websites and services. We do not control and are not
                responsible for their content, policies, or practices. Your use of them is at your own risk and subject
                to their terms.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">9. Disclaimers</h2>
              <p>
                Our website and services are provided "as is" and "as available," without warranties of any kind, express
                or implied, including merchantability, fitness for a particular purpose, and non-infringement. We do not
                warrant that the services will be uninterrupted or error-free, or that any particular freight, rate, or
                business result will be achieved.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">10. Limitation of Liability</h2>
              <p>
                To the fullest extent permitted by law, A&amp;C Consulting Group LLC and its members, officers, and
                employees will not be liable for any indirect, incidental, special, consequential, or punitive damages, or
                for lost profits or revenues, arising out of or relating to your use of our website or services. Our total
                liability for any claim relating to the services will not exceed the amount you paid us for the services
                giving rise to the claim in the three (3) months before the claim arose.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">11. Indemnification</h2>
              <p>
                You agree to indemnify and hold harmless A&amp;C Consulting Group LLC and its members, officers, and
                employees from any claims, damages, losses, or expenses (including reasonable attorneys' fees) arising out
                of your use of the services, your violation of these Terms, or your violation of any law or third-party
                right.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">12. Governing Law and Disputes</h2>
              <p>
                These Terms are governed by the laws of the State of Florida, without regard to its conflict-of-laws
                rules. The exclusive venue for any dispute not resolved informally will be the state or federal courts
                located in Florida, and you consent to their jurisdiction. Before filing any claim, you agree to first
                contact us at admin@acedispatch.us so we can attempt to resolve it informally.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">13. Changes to These Terms</h2>
              <p>
                We may update these Terms from time to time. Changes are effective when posted, and the "Effective date"
                above will be updated. Your continued use of the website or services after changes are posted constitutes
                acceptance.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-darkGray mb-3">14. Contact</h2>
              <p>
                A&amp;C Consulting Group LLC d/b/a Ace Dispatch<br />
                Email: admin@acedispatch.us<br />
                Website: acedispatch.us<br />
                236 Via D' Este #1402, Delray Beach, FL 33445
              </p>
            </div>
          </div>
        </div>
      </Section>
    </>
  );
};

export default TermsPage;
