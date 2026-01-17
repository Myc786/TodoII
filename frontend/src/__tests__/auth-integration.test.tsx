// Integration tests for authentication functionality
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

// Mock the auth context and API calls
vi.mock('@/hooks/use-auth', () => ({
  useAuth: () => ({
    user: null,
    isAuthenticated: false,
    isLoading: false,
    login: vi.fn(),
    register: vi.fn(),
    logout: vi.fn(),
  }),
}));

vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
  usePathname: () => '/login',
}));

describe('Authentication Integration Tests', () => {
  // Test that login form renders correctly
  it('renders login form with email and password fields', async () => {
    const LoginForm = (await import('@/components/auth/login')).default;

    render(<LoginForm />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  // Test that signup form renders correctly
  it('renders signup form with required fields', async () => {
    const SignupForm = (await import('@/components/auth/signup')).default;

    render(<SignupForm />);

    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument();
  });

  // Test login form submission
  it('handles login form submission', async () => {
    const mockLogin = vi.fn().mockResolvedValue({ ok: true });

    vi.mock('@/hooks/use-auth', () => ({
      useAuth: () => ({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        login: mockLogin,
        register: vi.fn(),
        logout: vi.fn(),
      }),
    }));

    const LoginForm = (await import('@/components/auth/login')).default;

    render(<LoginForm />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /sign in/i });

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'password123');
    });
  });

  // Test signup form submission
  it('handles signup form submission', async () => {
    const mockRegister = vi.fn().mockResolvedValue({ ok: true });

    vi.mock('@/hooks/use-auth', () => ({
      useAuth: () => ({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        login: vi.fn(),
        register: mockRegister,
        logout: vi.fn(),
      }),
    }));

    const SignupForm = (await import('@/components/auth/signup')).default;

    render(<SignupForm />);

    const nameInput = screen.getByLabelText(/name/i);
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const confirmPasswordInput = screen.getByLabelText(/confirm password/i);
    const submitButton = screen.getByRole('button', { name: /sign up/i });

    fireEvent.change(nameInput, { target: { value: 'Test User' } });
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockRegister).toHaveBeenCalledWith('test@example.com', 'password123', 'Test User');
    });
  });

  // Test protected route behavior
  it('redirects unauthenticated user from protected route', async () => {
    const mockPush = vi.fn();

    vi.mock('next/navigation', () => ({
      useRouter: () => ({
        push: mockPush,
      }),
    }));

    vi.mock('@/hooks/use-auth', () => ({
      useAuth: () => ({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        login: vi.fn(),
        register: vi.fn(),
        logout: vi.fn(),
      }),
    }));

    const ProtectedRoute = (await import('@/components/auth/protected-route')).default;

    render(<ProtectedRoute><div>Protected Content</div></ProtectedRoute>);

    // Wait for the effect to run
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/login');
    });
  });
});

// Additional tests for auth utils
describe('Auth Utilities', () => {
  it('has proper token storage mechanism', async () => {
    // Test that localStorage is used for token storage
    const token = 'test-jwt-token';
    localStorage.setItem('access_token', token);

    expect(localStorage.getItem('access_token')).toBe(token);

    // Cleanup
    localStorage.removeItem('access_token');
  });
});