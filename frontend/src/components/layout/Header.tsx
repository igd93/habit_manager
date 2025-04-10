import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';

export default function Header() {
  return (
    <header className="py-6 px-4 md:px-6 border-b">
      <div className="container mx-auto flex justify-between items-center">
        <div className="font-bold text-2xl">
          <Link to="/">HabitTracker</Link>
        </div>
        <nav className="hidden md:flex gap-6">
          <a href="#features" className="text-gray-600 hover:text-gray-900">
            Features
          </a>
          <a href="#about" className="text-gray-600 hover:text-gray-900">
            About
          </a>
          <a href="#pricing" className="text-gray-600 hover:text-gray-900">
            Pricing
          </a>
        </nav>
        <div className="flex gap-4">
          <Button variant="outline" asChild>
            <Link to="/login">Login</Link>
          </Button>
          <Button asChild>
            <Link to="/signup">Sign Up</Link>
          </Button>
        </div>
      </div>
    </header>
  );
}
