'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/hooks/use-auth';

interface SignupFormProps {
  onSignupSuccess?: () => void;
  onSwitchToLogin?: () => void;
}

export default function SignupForm({ onSignupSuccess, onSwitchToLogin }: SignupFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { toast } = useToast();
  const { register } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // Basic validation
    if (password !== confirmPassword) {
      toast({
        title: 'Signup failed',
        description: 'Passwords do not match',
        variant: 'destructive',
      });
      setIsLoading(false);
      return;
    }

    if (password.length < 8) {
      toast({
        title: 'Signup failed',
        description: 'Password must be at least 8 characters',
        variant: 'destructive',
      });
      setIsLoading(false);
      return;
    }

    try {
      const response = await register(email, password, name);

      if (response?.error) {
        toast({
          title: 'Signup failed',
          description: response.error || 'An error occurred during registration',
          variant: 'destructive',
        });
      } else {
        // Call the success callback if provided
        if (onSignupSuccess) {
          onSignupSuccess();
        } else {
          // Default behavior: redirect to dashboard/home
          router.push('/dashboard');
        }

        toast({
          title: 'Account created',
          description: 'Your account has been created successfully!',
        });
      }
    } catch (error: any) {
      toast({
        title: 'Signup failed',
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
          <CardTitle className="text-glow">Sign Up</CardTitle>
          <CardDescription className="text-glow">
            Create a new account to get started
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4 p-6">
            <div className="space-y-2">
              <Label htmlFor="name" className="text-glow">Name</Label>
              <Input
                id="name"
                type="text"
                placeholder="John Doe"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                disabled={isLoading}
                className="transition-all duration-300 focus:shadow-lg focus:ring-2 focus:ring-primary/50"
              />
            </div>
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
                minLength={8}
                disabled={isLoading}
                className="transition-all duration-300 focus:shadow-lg focus:ring-2 focus:ring-primary/50"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="confirmPassword" className="text-glow">Confirm Password</Label>
              <Input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                minLength={8}
                disabled={isLoading}
                className="transition-all duration-300 focus:shadow-lg focus:ring-2 focus:ring-primary/50"
              />
            </div>
          </CardContent>
          <CardFooter className="flex flex-col p-6 pt-0">
            <Button type="submit" className="w-full button-3d" disabled={isLoading}>
              {isLoading ? 'Creating account...' : 'Sign Up'}
            </Button>

            {onSwitchToLogin && (
              <div className="mt-4 text-center text-sm">
                Already have an account?{' '}
                <button
                  type="button"
                  onClick={onSwitchToLogin}
                  className="text-blue-600 hover:underline text-glow"
                  disabled={isLoading}
                >
                  Sign in
                </button>
              </div>
            )}
          </CardFooter>
        </form>
      </div>
    </Card>
  );
}