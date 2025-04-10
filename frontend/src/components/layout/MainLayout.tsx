import React from 'react';
import { Helmet } from 'react-helmet-async';

interface MainLayoutProps {
  children: React.ReactNode;
  title?: string;
  description?: string;
}

export default function MainLayout({
  children,
  title = 'HabitTracker - Track and Build Better Habits',
  description = 'A simple and effective way to track and build better habits in your daily life.',
}: MainLayoutProps) {
  return (
    <div className="min-h-screen flex flex-col">
      <Helmet>
        <title>{title}</title>
        <meta name="description" content={description} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Helmet>

      {children}
    </div>
  );
}
