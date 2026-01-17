import { useContext } from 'react';
import { AuthContextType } from '@/components/auth/provider';

// Re-export the context type and hooks from the provider file
export type { AuthContextType };
export { useAuth, useRequireAuth } from '@/components/auth/provider';