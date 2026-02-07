/**
 * Responsive utilities for the Todo Chatbot Extension
 */

import { useState, useEffect } from 'react';

// Breakpoints
export const BREAKPOINTS = {
  sm: 640,   // Small screens
  md: 768,   // Medium screens
  lg: 1024,  // Large screens
  xl: 1280,  // Extra large screens
  '2xl': 1536 // 2x extra large screens
};

// Hook to get current screen size
export function useScreenSize() {
  const [screenSize, setScreenSize] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  });

  useEffect(() => {
    const handleResize = () => {
      setScreenSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return screenSize;
}

// Hook to check if screen matches a breakpoint
export function useBreakpoint(breakpoint: keyof typeof BREAKPOINTS) {
  const screenSize = useScreenSize();
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    setMatches(screenSize.width >= BREAKPOINTS[breakpoint]);
  }, [screenSize, breakpoint]);

  return matches;
}

// Hook to check if mobile device
export function useIsMobile() {
  return useBreakpoint('md'); // Returns true if screen is smaller than md (768px)
}

// Hook to check if tablet device
export function useIsTablet() {
  const screenSize = useScreenSize();
  const [isTablet, setIsTablet] = useState(false);

  useEffect(() => {
    setIsTablet(screenSize.width >= BREAKPOINTS.sm && screenSize.width < BREAKPOINTS.lg);
  }, [screenSize]);

  return isTablet;
}

// Hook to check if desktop device
export function useIsDesktop() {
  return useBreakpoint('lg'); // Returns true if screen is larger than lg (1024px)
}

// Function to get device type
export function getDeviceType(): 'mobile' | 'tablet' | 'desktop' {
  if (typeof window === 'undefined') return 'desktop'; // Server-side default

  const width = window.innerWidth;
  if (width < BREAKPOINTS.md) {
    return 'mobile';
  } else if (width < BREAKPOINTS.lg) {
    return 'tablet';
  } else {
    return 'desktop';
  }
}

// Hook to get device type
export function useDeviceType() {
  const [deviceType, setDeviceType] = useState<'mobile' | 'tablet' | 'desktop'>('desktop');
  const screenSize = useScreenSize();

  useEffect(() => {
    setDeviceType(getDeviceType());
  }, [screenSize]);

  return deviceType;
}