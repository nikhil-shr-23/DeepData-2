'use client'

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Dashboard() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);
  const url = 'https://urban-flood-analytics.streamlit.app/'
  
  // Fallback to open in new tab if iframe fails
  const openInNewTab = () => {
    window.open(url, '_blank', 'noopener,noreferrer');
  };
  
  const handleLoad = () => {
    setIsLoading(false);
  };
  
  const handleError = () => {
    console.log('Iframe failed to load, likely due to authentication redirect or X-Frame-Options');
    setIsLoading(false);
    setHasError(true);
  };
  
  return (
    <div className="w-screen h-screen m-0 p-0 overflow-hidden bg-gray-900 relative">
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
      {/* Loading overlay */}
      {isLoading && (
        <div className="absolute inset-0 bg-gray-900 flex items-center justify-center z-10">
          <div className="text-center">
            <div className="w-16 h-16 border-4 border-blue-400/30 border-t-blue-400 rounded-full animate-spin mx-auto mb-4" />
            <div className="text-white text-lg font-medium font-montserrat">Loading Dashboard...</div>
            <div className="text-white/60 text-sm mt-2">Team Codezilla</div>
          </div>
        </div>
      )}
      
      {/* Error state */}
      {hasError && (
        <div className="absolute inset-0 bg-gray-900 flex items-center justify-center z-10">
          <div className="text-center">
            <div className="text-red-400 text-6xl mb-4">⚠️</div>
            <div className="text-white text-xl font-medium font-montserrat mb-2">Dashboard Requires Authentication</div>
            <div className="text-white/60 text-sm mb-6 max-w-md mx-auto">
              The Streamlit app cannot be loaded in an iframe due to authentication requirements. 
              Click below to open it in a new tab.
            </div>
            <div className="space-x-4">
              <button 
                onClick={openInNewTab}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors cursor-pointer"
              >
                Open in New Tab
              </button>
              <button 
                onClick={() => window.location.reload()}
                className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg transition-colors cursor-pointer"
              >
                Retry Iframe
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Main iframe */}
      <iframe 
        src={url} 
        title="Urban Flood Risk Analytics Dashboard"
        className="w-full h-full border-0 m-0 p-0"
        onLoad={handleLoad}
        onError={handleError}
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
        referrerPolicy="no-referrer-when-downgrade"
      />
    </div>
  )
}
