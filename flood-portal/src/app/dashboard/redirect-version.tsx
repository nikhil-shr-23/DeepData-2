'use client'

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function DashboardRedirect() {
  const router = useRouter();
  const url = 'https://urban-flood-analytics.streamlit.app/';
  
  useEffect(() => {
    // Redirect to Streamlit app in the same tab after a brief delay
    const timer = setTimeout(() => {
      window.location.href = url;
    }, 2000);
    
    return () => clearTimeout(timer);
  }, []);
  
  const openNow = () => {
    window.location.href = url;
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
        <div className="w-16 h-16 border-4 border-blue-400/30 border-t-blue-400 rounded-full animate-spin mx-auto mb-4" />
        <div className="text-white text-xl font-medium font-montserrat mb-2">Redirecting to Dashboard...</div>
        <div className="text-white/60 text-sm mb-6">You will be redirected to the Streamlit app in 2 seconds</div>
        <div className="text-white/40 text-xs mb-4">Team Codezilla</div>
        
        <button 
          onClick={openNow}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors cursor-pointer"
        >
          Open Now
        </button>
      </div>
    </div>
  );
}