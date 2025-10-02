'use client'

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Dashboard() {
  const router = useRouter();
  const dashboardUrl = 'https://urban-flood-analytics.streamlit.app/';
  const githubUrl = 'https://github.com/nikhil-shr-23/DeepData-2';
  
  useEffect(() => {
    // Automatically open dashboard in new tab after a brief delay
    const timer = setTimeout(() => {
      window.open(dashboardUrl, '_blank', 'noopener,noreferrer');
    }, 2000);
    
    return () => clearTimeout(timer);
  }, []);
  
  const openDashboard = () => {
    window.open(dashboardUrl, '_blank', 'noopener,noreferrer');
  };
  
  const openSourceCode = () => {
    window.open(githubUrl, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className="w-screen h-screen m-0 p-0 overflow-hidden bg-gray-900 flex items-center justify-center">
      {/* Back button */}
      <button
        onClick={() => router.push('/')}
        className="absolute top-4 left-4 z-20 bg-black/50 hover:bg-black/70 text-white p-2 rounded-lg backdrop-blur-sm transition-all duration-200 cursor-pointer"
        title="Back to Landing Page"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
      </button>
      
      <div className="text-center">
        <div className="w-20 h-20 border-4 border-blue-400/30 border-t-blue-400 rounded-full animate-spin mx-auto mb-6" />
        <div className="text-white text-2xl font-bold font-montserrat mb-3">Opening Dashboard...</div>
        <div className="text-white/70 text-base mb-6 max-w-md mx-auto">
          The dashboard will open in a new tab automatically in 2 seconds
        </div>
        <div className="text-white/40 text-sm mb-8">Team Codezilla - Urban Flood Risk Analytics</div>
        
        <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
          {/* Open Dashboard Button */}
          <button 
            onClick={openDashboard}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-all duration-300 cursor-pointer flex items-center gap-2 font-medium hover:scale-105 shadow-lg"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
            Open Dashboard Now
          </button>
          
          {/* Source Code Button */}
          <button 
            onClick={openSourceCode}
            className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 rounded-lg transition-all duration-300 cursor-pointer flex items-center gap-2 font-medium hover:scale-105 shadow-lg"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.30.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
            View Source Code
          </button>
        </div>
        
        <div className="mt-8 text-white/50 text-xs">
          <p>Built with Next.js, TypeScript & Streamlit</p>
        </div>
      </div>
    </div>
  );
}