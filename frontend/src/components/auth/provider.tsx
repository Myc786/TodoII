'use client';

import { useState, useEffect, useContext, createContext, ReactNode } from 'react';
import { signIn, signOut, useSession } from '@/lib/auth';

// Define the authentication context type
export interface AuthContextType {
  user: any | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<any>;
  register: (email: string, password: string, name: string) => Promise<any>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<boolean>;
}

// Create the authentication context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Define the provider props type
interface AuthProviderProps {
  children: ReactNode;
}

// Create the authentication provider component
export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [isLoading, setIsLoading] = useState(true);
  const [session, setSession] = useState<{ user: any } | null>(null);

  // Helper function to clear authentication storage
  const clearAuthStorage = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  };

  // Helper function to refresh access token using refresh token
  const refreshAccessToken = async (refreshToken: string): Promise<boolean> => {
    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          refresh_token: refreshToken
        })
      });

      if (response.ok) {
        const data = await response.json();
        // Store new tokens
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('user', JSON.stringify(data.user));
        return true;
      } else {
        return false;
      }
    } catch (error) {
      console.error('Error refreshing token:', error);
      return false;
    }
  };

  // Effect to check for existing session in localStorage
  useEffect(() => {
    const loadSession = async () => {
      const token = localStorage.getItem('access_token');
      const refreshToken = localStorage.getItem('refresh_token');
      const userData = localStorage.getItem('user');

      if (token && userData) {
        try {
          // Validate the token by fetching user profile
          const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
          const response = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });

          if (response.ok) {
            const user = JSON.parse(userData);
            setSession({ user });
          } else if (response.status === 401 && refreshToken) {
            // Access token expired, try to refresh
            const refreshed = await refreshAccessToken(refreshToken);
            if (refreshed) {
              const user = JSON.parse(userData);
              setSession({ user });
            } else {
              // Refresh failed, clear storage
              clearAuthStorage();
            }
          } else {
            // Token is invalid, clear local storage
            clearAuthStorage();
          }
        } catch (error) {
          console.error('Error validating session:', error);
          // Clear invalid session data
          clearAuthStorage();
        }
      }

      setIsLoading(false);
    };

    loadSession();

    // Listen for auth:logout events (e.g., from failed token refresh)
    const handleAuthLogout = () => {
      clearAuthStorage();
      setSession(null);
    };

    window.addEventListener('auth:logout', handleAuthLogout);

    return () => {
      window.removeEventListener('auth:logout', handleAuthLogout);
    };
  }, []);

  // Login function - calling the backend API directly
  const login = async (email: string, password: string) => {
    console.log('Login attempt starting for:', email);
    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
      console.log('Connecting to API:', API_BASE_URL);
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store tokens in localStorage (or use a more secure method in production)
        if (data.access_token) {
          localStorage.setItem('access_token', data.access_token);
          if (data.refresh_token) {
            localStorage.setItem('refresh_token', data.refresh_token);
          }
          localStorage.setItem('user', JSON.stringify(data.user));

          // Update the session state to reflect the new authentication status
          setSession({ user: data.user });
        }
        return { ok: true, ...data };
      } else {
        console.warn('Login failed response:', data);
        return { error: data.detail || data.message || 'Login failed', ok: false };
      }
    } catch (error) {
      console.error('Login error details:', error);
      return { error: 'Network error occurred', ok: false };
    }
  };

  // Register function - calling the backend API directly
  const register = async (email: string, password: string, name: string) => {
    console.log('Registration attempt starting for:', email);
    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
      console.log('Connecting to API:', API_BASE_URL);
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          name
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // After successful registration, automatically log the user in
        return await login(email, password);
      } else {
        console.warn('Registration failed response:', data);
        return { error: data.detail || data.message || 'Registration failed', ok: false };
      }
    } catch (error) {
      console.error('Registration error details:', error);
      return { error: 'Network error occurred', ok: false };
    }
  };

  // Logout function
  const logout = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const refreshToken = localStorage.getItem('refresh_token');

      // Call backend logout endpoint to revoke refresh token
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
      if (token) {
        await fetch(`${API_BASE_URL}/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            refresh_token: refreshToken,
            revoke_all: false
          })
        });
      }

      // Remove tokens from localStorage
      clearAuthStorage();

      // Update the session state to reflect the logout
      setSession(null);
    } catch (error) {
      console.error('Logout error:', error);
      // Still remove local data and update session state even if backend call fails
      clearAuthStorage();
      setSession(null);
    }
  };

  // Refresh token function (public API for manual refresh)
  const refreshToken = async (): Promise<boolean> => {
    try {
      const refreshTokenValue = localStorage.getItem('refresh_token');
      if (!refreshTokenValue) {
        return false;
      }

      const success = await refreshAccessToken(refreshTokenValue);
      if (success) {
        // Reload user data
        const userData = localStorage.getItem('user');
        if (userData) {
          setSession({ user: JSON.parse(userData) });
        }
      }
      return success;
    } catch (error) {
      console.error('Token refresh error:', error);
      return false;
    }
  };

  // Prepare the context value
  const contextValue: AuthContextType = {
    user: session?.user || null,
    isAuthenticated: !!session?.user,
    isLoading,
    login,
    register,
    logout,
    refreshToken
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to consume the authentication context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Hook to protect routes that require authentication
export const useRequireAuth = () => {
  const { isAuthenticated, isLoading } = useAuth();

  // Return true if authenticated, false if not, and null if still loading
  if (isLoading) return null;
  return isAuthenticated;
};