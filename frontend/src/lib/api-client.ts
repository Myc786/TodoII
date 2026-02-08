/**
 * API client with automatic token refresh
 *
 * This module provides a fetch wrapper that automatically handles token expiration
 * by refreshing the access token using the refresh token when a 401 response is received.
 */

interface FetchOptions extends RequestInit {
  skipAuth?: boolean;
  skipRefresh?: boolean;
}

/**
 * Refresh the access token using the refresh token
 */
async function refreshAccessToken(): Promise<boolean> {
  try {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      return false;
    }

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
      if (data.user) {
        localStorage.setItem('user', JSON.stringify(data.user));
      }
      return true;
    } else {
      // Refresh failed, clear tokens
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      return false;
    }
  } catch (error) {
    console.error('Error refreshing token:', error);
    return false;
  }
}

/**
 * Enhanced fetch with automatic token refresh on 401 errors
 *
 * @param url - The URL to fetch
 * @param options - Fetch options with additional skipAuth and skipRefresh flags
 * @returns Promise<Response>
 */
export async function authenticatedFetch(
  url: string,
  options: FetchOptions = {}
): Promise<Response> {
  const { skipAuth, skipRefresh, ...fetchOptions } = options;

  // Add authorization header if not skipped
  if (!skipAuth) {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchOptions.headers = {
        ...fetchOptions.headers,
        'Authorization': `Bearer ${token}`,
      };
    }
  }

  // Make the initial request
  let response = await fetch(url, fetchOptions);

  // If we got a 401 and refresh is not skipped, try to refresh the token
  if (response.status === 401 && !skipRefresh && !skipAuth) {
    const refreshed = await refreshAccessToken();

    if (refreshed) {
      // Retry the request with the new token
      const newToken = localStorage.getItem('access_token');
      if (newToken) {
        fetchOptions.headers = {
          ...fetchOptions.headers,
          'Authorization': `Bearer ${newToken}`,
        };
        response = await fetch(url, fetchOptions);
      }
    } else {
      // Refresh failed, redirect to login or handle accordingly
      // You might want to emit an event or call a callback here
      console.warn('Token refresh failed, user needs to re-authenticate');
      // Optionally redirect to login page
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('auth:logout'));
      }
    }
  }

  return response;
}

/**
 * Convenience method for authenticated GET requests
 */
export async function authenticatedGet(url: string, options?: FetchOptions): Promise<Response> {
  return authenticatedFetch(url, { ...options, method: 'GET' });
}

/**
 * Convenience method for authenticated POST requests
 */
export async function authenticatedPost(
  url: string,
  body?: any,
  options?: FetchOptions
): Promise<Response> {
  return authenticatedFetch(url, {
    ...options,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });
}

/**
 * Convenience method for authenticated PUT requests
 */
export async function authenticatedPut(
  url: string,
  body?: any,
  options?: FetchOptions
): Promise<Response> {
  return authenticatedFetch(url, {
    ...options,
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });
}

/**
 * Convenience method for authenticated DELETE requests
 */
export async function authenticatedDelete(url: string, options?: FetchOptions): Promise<Response> {
  return authenticatedFetch(url, { ...options, method: 'DELETE' });
}
