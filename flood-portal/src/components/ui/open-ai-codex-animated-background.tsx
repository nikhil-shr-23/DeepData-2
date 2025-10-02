"use client";
import React, { useEffect, useState } from 'react';

declare global {
  interface Window {
    UnicornStudio: {
      init: () => void;
    };
  }
}

interface ComponentProps {
  containerWidth?: number;
  containerHeight?: number;
}

export const Component: React.FC<ComponentProps> = ({ 
  containerWidth, 
  containerHeight 
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [loadTimeout, setLoadTimeout] = useState(false);

  useEffect(() => {
    // Check if script already exists
    const existingScript = document.querySelector('script[src="https://cdn.unicorn-studio.com/latest/unicornStudio.umd.js"]');
    
    if (existingScript) {
      setIsLoaded(true);
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://cdn.unicorn-studio.com/latest/unicornStudio.umd.js';
    script.onload = () => {
      setIsLoaded(true);
    };
    script.onerror = () => {
      console.warn('Failed to load UnicornStudio script');
      setLoadTimeout(true);
    };
    
    document.head.appendChild(script);

    // Timeout fallback
    const timeout = setTimeout(() => {
      if (!isLoaded) {
        setLoadTimeout(true);
      }
    }, 5000);

    return () => {
      clearTimeout(timeout);
      if (document.head.contains(script)) {
        document.head.removeChild(script);
      }
    };
  }, [isLoaded]);

  useEffect(() => {
    if (isLoaded && window.UnicornStudio) {
      try {
        window.UnicornStudio.init();
      } catch (error) {
        console.warn('UnicornStudio initialization failed:', error);
        setLoadTimeout(true);
      }
    }
  }, [isLoaded]);

  const style = containerWidth && containerHeight 
    ? { width: `${containerWidth}px`, height: `${containerHeight}px` }
    : { width: '100%', height: '100%' };

  // If loading failed, show a beautiful gradient background
  if (loadTimeout || (!isLoaded && typeof window !== 'undefined')) {
    return (
      <div 
        className="w-full h-full bg-gradient-to-br from-purple-900/40 via-blue-800/50 to-indigo-900/60 rounded-lg relative overflow-hidden"
        style={style}
      >
        {/* Animated gradient background */}
        <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 via-blue-500/20 to-teal-400/20 animate-pulse"></div>
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(120,119,198,0.3),transparent_50%)] animate-pulse"></div>
        
        {/* Floating particles effect */}
        <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-white/30 rounded-full animate-bounce delay-700"></div>
        <div className="absolute top-3/4 right-1/3 w-1 h-1 bg-blue-300/50 rounded-full animate-bounce delay-1000"></div>
        <div className="absolute bottom-1/4 left-1/2 w-3 h-3 bg-purple-400/40 rounded-full animate-bounce delay-300"></div>
      </div>
    );
  }

  return (
    <div 
      className="unicorn-studio-embed w-full h-full"
      data-us-project="1grEuiVDSVmyvEMAYhA6" 
      style={style}
    >
      {/* Loading state */}
      {!isLoaded && (
        <div className="w-full h-full bg-gradient-to-br from-purple-900/40 via-blue-800/50 to-indigo-900/60 rounded-lg flex items-center justify-center">
          <div className="flex flex-col items-center space-y-3">
            <div className="w-8 h-8 border-2 border-white/30 border-t-white/70 rounded-full animate-spin"></div>
            <div className="text-white/60 text-sm font-medium">Loading animation...</div>
          </div>
        </div>
      )}
    </div>
  );
};
