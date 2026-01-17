'use client';

import { useState, useEffect, useContext, createContext, ReactNode } from 'react';
import { signIn, signOut, useSession } from '@/lib/auth';

// Define the authentication context type
interface AuthContextType {
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
          const response = await fetch('http://localhost:8000/api/auth/me', {
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
    try {
      const response = await fetch('http://localhost:8000/api/auth/login', {
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
        }
        return { ok: true, ...data };
      } else {
        return { error: data.detail || 'Login failed', ok: false };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { error: 'Network error occurred', ok: false };
    }
  };

  // Register function - calling the backend API directly
  const register = async (email: string, password: string, name: string) => {
    try {
      const response = await fetch('http://localhost:8000/api/auth/register', {
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
        return { error: data.detail || 'Registration failed', ok: false };
      }
    } catch (error) {
      console.error('Registration error:', error);
      return { error: 'Network error occurred', ok: false };
    }
  };

  // Logout function
  const logout = async () => {
    try {
      // Remove token from localStorage
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');

      // Call backend logout endpoint
      await fetch('http://localhost:8000/api/auth/logout', {
        method: 'POST',
      });
    } catch (error) {
      console.error('Logout error:', error);
      // Still remove local data even if backend call fails
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
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