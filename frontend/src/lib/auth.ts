import { signIn, signOut, useSession,getSession } from 'next-auth/react';

// Export authentication functions
export { signIn, signOut, useSession, getSession };

// Export types for authentication
export type {
  Session,
  User
} from 'next-auth';