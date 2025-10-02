'use client'

import { Component } from "@/components/ui/open-ai-codex-animated-background";
import { Button } from "@/components/ui/button";
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Home() {
  const router = useRouter();
  const [isVisible, setIsVisible] = useState(false);
  const githubUrl = 'https://github.com/nikhil-shr-23/DeepData-2';

  useEffect(() => {
    // Trigger fade-in animation after component mounts
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, 100);

    return () => clearTimeout(timer);
  }, []);

  const handleNavigate = () => {
    router.push('/dashboard');
  };
  
  const openSourceCode = () => {
    window.open(githubUrl, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Background Animation */}
      <div className="absolute inset-0 z-0">
        <Component />
      </div>
      
      {/* Content */}
      <div className={`relative z-10 flex flex-col items-center justify-center min-h-screen p-8 transition-all duration-1000 transform ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
      }`}>
        {/* Square Container for Animation */}
        <div className="w-96 h-96 mb-8 rounded-lg overflow-hidden shadow-2xl border border-white/10 bg-gradient-to-br from-purple-900/30 to-blue-900/30">
          <Component containerWidth={384} containerHeight={384} />
        </div>
        
        {/* Team Name */}
        <h1 
          className="text-6xl font-bold mb-12 text-white text-center transition-all duration-1000 delay-300 font-montserrat"
          style={{ 
            opacity: isVisible ? 1 : 0,
            transform: isVisible ? 'translateY(0)' : 'translateY(20px)'
          }}
        >
          Team Codezilla
        </h1>
        
        {/* Buttons */}
        <div className={`transition-all duration-1000 delay-500 ${
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}>
          <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
            <Button 
              onClick={handleNavigate}
              size="lg"
              className="bg-white text-black hover:bg-gray-200 font-semibold px-8 py-3 rounded-full text-lg shadow-lg transition-all duration-300 hover:scale-105 cursor-pointer flex items-center gap-2"
            >
              Take me to project
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </Button>
            
            <Button 
              onClick={openSourceCode}
              size="lg"
              className="bg-gray-800 text-white hover:bg-gray-700 font-semibold px-8 py-3 rounded-full text-lg shadow-lg transition-all duration-300 hover:scale-105 cursor-pointer flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
              </svg>
              View Source
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}