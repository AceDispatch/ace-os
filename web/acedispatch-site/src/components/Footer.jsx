import React from 'react';
import { Link } from 'react-router-dom';
import { Phone, Mail, MapPin } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-darkGray text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <img 
                src="https://horizons-cdn.hostinger.com/1191ea2e-bcfd-4bab-a9f3-4c5fa4e256be/c7c96b8a1debfe34ff8f0b30873ed207.png" 
                alt="Ace Dispatch Logo" 
                className="h-10 w-auto object-contain"
              />
              <span className="text-xl font-bold">
                <span className="text-dispatchRed">Ace</span> <span className="text-white">Dispatch</span>
              </span>
            </div>
            <p className="text-gray-400 mb-4 max-w-md">
              Professional dispatch services for owner-operators and small fleets. We handle the loads, rates, and paperwork so you can focus on driving.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-gray-400 hover:text-white transition-colors duration-300">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/services" className="text-gray-400 hover:text-white transition-colors duration-300">
                  Services
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-gray-400 hover:text-white transition-colors duration-300">
                  About
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-400 hover:text-white transition-colors duration-300">
                  Contact
                </Link>
              </li>
              <li>
                <Link to="/onboarding" className="text-gray-400 hover:text-white transition-colors duration-300">
                  Onboarding
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact</h3>
            <ul className="space-y-3">
              <li className="flex items-start gap-2">
                <Phone className="w-5 h-5 text-dispatchRed flex-shrink-0 mt-0.5" />
                <a href="tel:6318073088" className="text-gray-400 hover:text-white transition-colors duration-300">
                  (631) 807-3088
                </a>
              </li>
              <li className="flex items-start gap-2">
                <Mail className="w-5 h-5 text-dispatchRed flex-shrink-0 mt-0.5" />
                <a href="mailto:admin@acedispatch.us" className="text-gray-400 hover:text-white transition-colors duration-300">
                  admin@acedispatch.us
                </a>
              </li>
              <li className="flex items-start gap-2">
                <MapPin className="w-5 h-5 text-dispatchRed flex-shrink-0 mt-0.5" />
                <span className="text-gray-400">
                  236 Via D' Este #1402<br />
                  Delray Beach, FL 33445
                </span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-700 mt-8 pt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
          <p className="text-gray-400 text-sm">
            © {new Date().getFullYear()} <span className="text-dispatchRed">Ace</span> <span className="text-white">Dispatch</span>. All rights reserved.
          </p>
          <div className="flex items-center gap-4">
            <Link
              to="/privacy"
              className="text-gray-400 hover:text-white text-sm transition-colors duration-300"
            >
              Privacy Policy
            </Link>
            <Link
              to="/terms"
              className="text-gray-400 hover:text-white text-sm transition-colors duration-300"
            >
              Terms of Service
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;