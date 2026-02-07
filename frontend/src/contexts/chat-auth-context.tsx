'use client';

import { createContext, useContext, ReactNode, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode'; // Note: Using jwt-decode library

// Define the shape of our auth context
interface ChatAuthContextType {
  isAuthenticated: boolean;
  user: any | null;
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
  getAuthToken: () => string | null;
  refreshToken: () => Promise<boolean>;
}

// Create the context with a default undefined value
const ChatAuthContext = createContext<ChatAuthContextType | undefined>(undefined);

// Define the provider props type
interface ChatAuthProviderProps {
  children: ReactNode;
}

// Create the authentication provider component
export const ChatAuthProvider = ({ children }: ChatAuthProviderProps) => {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<any | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  // Initialize from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('access_token');
    if (storedToken) {
      try {
        // Validate token and set user context
        const decodedToken: any = jwtDecode(storedToken);
        const currentTime = Date.now() / 1000;

        if (decodedToken.exp < currentTime) {
          // Token is expired, clear it
          localStorage.removeItem('access_token');
          setToken(null);
          setUser(null);
          setIsAuthenticated(false);
        } else {
          setToken(storedToken);
          setUser(decodedToken);
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Error decoding token:', error);
        localStorage.removeItem('access_token');
        setToken(null);
        setUser(null);
        setIsAuthenticated(false);
      }
    }
  }, []);

  // Login function
  const login = (newToken: string) => {
    try {
      const decodedToken: any = jwtDecode(newToken);
      localStorage.setItem('access_token', newToken);
      setToken(newToken);
      setUser(decodedToken);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Error decoding token during login:', error);
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('access_token');
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
  };

  // Get current auth token
  const getAuthToken = (): string | null => {
    // Check if token is still valid
    if (token) {
      try {
        const decodedToken: any = jwtDecode(token);
        const currentTime = Date.now() / 1000;

        if (decodedToken.exp < currentTime) {
          // Token is expired
          logout();
          return null;
        }
        return token;
      } catch (error) {
        console.error('Error decoding token:', error);
        logout();
        return null;
      }
    }
    return null;
  };

  // Refresh token function (placeholder - implement actual refresh logic)
  const refreshToken = async (): Promise<boolean> => {
    // In a real implementation, you would call your backend to refresh the token
    // For now, we'll just check if the current token is still valid
    const currentToken = localStorage.getItem('access_token');
    if (currentToken) {
      try {
        const decodedToken: any = jwtDecode(currentToken);
        const currentTime = Date.now() / 1000;

        if (decodedToken.exp - currentTime > 300) { // Token is valid for more than 5 minutes
          return true;
        } else {
          // Token is expiring soon, might need to refresh
          // Implement actual refresh logic here
          return false;
        }
      } catch (error) {
        console.error('Error decoding token during refresh:', error);
        return false;
      }
    }
    return false;
  };

  // Prepare the context value
  const contextValue: ChatAuthContextType = {
    isAuthenticated,
    user,
    token,
    login,
    logout,
    getAuthToken,
    refreshToken
  };

  return (
    <ChatAuthContext.Provider value={contextValue}>
      {children}
    </ChatAuthContext.Provider>
  );
};

// Custom hook to consume the chat authentication context
export const useChatAuth = () => {
  const context = useContext(ChatAuthContext);
  if (context === undefined) {
    throw new Error('useChatAuth must be used within a ChatAuthProvider');
  }
  return context;
};

// Export the context for use in other files if needed
export { ChatAuthContext };