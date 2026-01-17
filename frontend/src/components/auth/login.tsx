'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/hooks/use-auth';

interface LoginFormProps {
  onLoginSuccess?: () => void;
  onSwitchToSignup?: () => void;
}

export default function LoginForm({ onLoginSuccess, onSwitchToSignup }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { toast } = useToast();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await login(email, password);

      if (response?.error) {
        toast({
          title: 'Login failed',
          description: response.error || 'Invalid credentials',
          variant: 'destructive',
        });
      } else {
        // Call the success callback if provided
        if (onLoginSuccess) {
          onLoginSuccess();
        } else {
          // Default behavior: redirect to dashboard/home
          router.push('/dashboard');
        }

        toast({
          title: 'Login successful',
          description: 'Welcome back!',
        });
      }
    } catch (error: any) {
      toast({
        title: 'Login failed',
        description: error.message || 'An unexpected error occurred. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto card-3d bg-gradient-to-br from-background to-secondary/30 p-0.5 shadow-lg hover:shadow-xl transition-all duration-300">
      <div className="surface-3d rounded-lg">
        <CardHeader className="text-center">
          <CardTitle className="text-glow">Login</CardTitle>
          <CardDescription className="text-glow">
            Enter your credentials to access your account
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4 p-6">
            <div className="space-y-2">
              <Label htmlFor="email" className="text-glow">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={isLoading}
                className="transition-all duration-300 focus:shadow-lg focus:ring-2 focus:ring-primary/50"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password" className="text-glow">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={isLoading}
                className="transition-all duration-300 focus:shadow-lg focus:ring-2 focus:ring-primary/50"
              />
            </div>
          </CardContent>
          <CardFooter className="flex flex-col p-6 pt-0">
            <Button type="submit" className="w-full button-3d" disabled={isLoading}>
              {isLoading ? 'Signing in...' : 'Sign In'}
            </Button>

            {onSwitchToSignup && (
              <div className="mt-4 text-center text-sm">
                Don't have an account?{' '}
                <button
                  type="button"
                  onClick={onSwitchToSignup}
                  className="text-blue-600 hover:underline text-glow"
                  disabled={isLoading}
                >
                  Sign up
                </button>
              </div>
            )}
          </CardFooter>
        </form>
      </div>
    </Card>
  );
}