'use client'

import { Component } from "@/components/ui/open-ai-codex-animated-background";
import { Button } from "@/components/ui/button";
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Home() {
  const router = useRouter();
  const [isVisible, setIsVisible] = useState(false);

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
        
        {/* Button */}
        <div className={`transition-all duration-1000 delay-500 ${
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}>
          <Button 
            onClick={handleNavigate}
            size="lg"
            className="bg-white text-black hover:bg-gray-200 font-semibold px-8 py-3 rounded-full text-lg shadow-lg transition-all duration-300 hover:scale-105 cursor-pointer"
          >
            Take me to project
          </Button>
        </div>
      </div>
    </div>
  );
}
