"use client";

import { cn } from "@/lib/utils";
import { useState, useEffect } from "react";
import dynamic from 'next/dynamic';

// Dynamically import UnicornScene to avoid SSR issues
const UnicornScene = dynamic(() => import('unicornstudio-react'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full bg-gradient-to-br from-purple-900/20 to-blue-900/20 animate-pulse rounded-lg flex items-center justify-center">
      <div className="text-white/50 text-sm font-medium">Loading Animation...</div>
    </div>
  )
});

export const useWindowSize = () => {
  const [windowSize, setWindowSize] = useState({
    width: 800, // Default fallback values
    height: 600,
  });
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    if (mounted) {
      handleResize(); // Set initial size
      window.addEventListener('resize', handleResize);
      return () => window.removeEventListener('resize', handleResize);
    }
  }, [mounted]);

  return windowSize;
};

export const Component = ({ containerWidth, containerHeight }: { containerWidth?: number; containerHeight?: number } = {}) => {
  const { width: windowWidth, height: windowHeight } = useWindowSize();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Use container dimensions if provided, otherwise use window dimensions
  const width = containerWidth || windowWidth;
  const height = containerHeight || windowHeight;

  // Show loading placeholder during SSR and initial hydration
  if (!mounted) {
    return (
      <div className={cn("flex flex-col items-center w-full h-full")}>
        <div className="w-full h-full bg-gradient-to-br from-purple-900/20 to-blue-900/20 animate-pulse rounded-lg flex items-center justify-center">
          <div className="text-white/50 text-sm font-medium">Loading Animation...</div>
        </div>
      </div>
    );
  }

  return (
    <div className={cn("flex flex-col items-center w-full h-full")} suppressHydrationWarning>
      <UnicornScene 
        production={true} 
        projectId="1grEuiVDSVmyvEMAYhA6" 
        width={width} 
        height={height} 
      />
    </div>
  );
};
