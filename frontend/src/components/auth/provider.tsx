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

  // Effect to check for existing session in localStorage
  useEffect(() => {
    const loadSession = async () => {
      const token = localStorage.getItem('access_token');
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
          } else {
            // Token is invalid, clear local storage
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
          }
        } catch (error) {
          console.error('Error validating session:', error);
          // Clear invalid session data
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');
        }
      }

      setIsLoading(false);
    };

    loadSession();
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
        // Store the token in localStorage (or use a more secure method in production)
        if (data.access_token) {
          localStorage.setItem('access_token', data.access_token);
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
      // Remove token from localStorage
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');

      // Update the session state to reflect the logout
      setSession(null);

      // Call backend logout endpoint
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
      await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
        },
      });
    } catch (error) {
      console.error('Logout error:', error);
      // Still remove local data and update session state even if backend call fails
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      setSession(null);
    }
  };

  // Refresh token function
  const refreshToken = async (): Promise<boolean> => {
    // With NextAuth, token refresh is typically handled automatically
    // This function is a placeholder for cases where manual refresh is needed
    try {
      // For now, we'll just return true to indicate success
      return true;
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