'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import { useAuth } from '@/hooks/use-auth';
import { useRouter } from 'next/navigation';

export function Header() {
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  if (isLoading) {
    return (
      <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur">
        <div className="container flex h-16 items-center">
          <div className="mr-4 flex items-center space-x-2">
            <Link href="/" className="mr-6 flex items-center space-x-2">
              <span className="hidden font-bold sm:inline-block">Todo App</span>
            </Link>
          </div>
          <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
            <nav className="flex items-center space-x-2"></nav>
            <div className="flex items-center gap-2">
              <div className="animate-pulse rounded-md bg-muted h-8 w-20" />
            </div>
          </div>
        </div>
      </header>
    );
  }

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-gradient-to-r from-background to-secondary/20 backdrop-blur-lg shadow-lg">
      <div className="container flex h-16 items-center">
        <div className="mr-4 flex items-center space-x-2">
          <Link href="/" className="mr-6 flex items-center space-x-2 group">
            <span className="hidden font-bold sm:inline-block text-2xl text-glow group-hover:scale-105 transition-transform duration-300">Todo App</span>
          </Link>
        </div>
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <nav className="flex items-center space-x-2">
            {!isAuthenticated ? (
              <>
                <Link href="/login">
                  <Button variant="ghost" className="button-3d">Login</Button>
                </Link>
                <Link href="/signup">
                  <Button className="button-3d">Sign Up</Button>
                </Link>
              </>
            ) : (
              <div className="flex items-center gap-4">
                <span className="text-sm font-medium text-glow">{user?.name || user?.email}</span>
                <Button variant="outline" onClick={handleLogout} className="button-3d">
                  Logout
                </Button>
              </div>
            )}
          </nav>
          <div className="flex items-center gap-2">
            <ThemeToggle />
          </div>
        </div>
      </div>
    </header>
  );
}