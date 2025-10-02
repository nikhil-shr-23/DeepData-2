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

  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdn.unicorn-studio.com/latest/unicornStudio.umd.js';
    script.onload = () => {
      setIsLoaded(true);
    };
    document.head.appendChild(script);

    return () => {
      if (document.head.contains(script)) {
        document.head.removeChild(script);
      }
    };
  }, []);

  useEffect(() => {
    if (isLoaded && window.UnicornStudio) {
      try {
        window.UnicornStudio.init();
      } catch (error) {
        console.warn('UnicornStudio initialization failed:', error);
      }
    }
  }, [isLoaded]);

  const style = containerWidth && containerHeight 
    ? { width: `${containerWidth}px`, height: `${containerHeight}px` }
    : { width: '100%', height: '100%' };

  return (
    <div 
      className="unicorn-studio-embed"
      data-us-project="1grEuiVDSVmyvEMAYhA6" 
      style={style}
    >
      {/* Fallback content */}
      {!isLoaded && (
        <div className="w-full h-full bg-gradient-to-br from-purple-900/30 to-blue-900/30 rounded-lg flex items-center justify-center">
          <div className="text-white/50 text-sm">Loading animation...</div>
        </div>
      )}
    </div>
  );
};