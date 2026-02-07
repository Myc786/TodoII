'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';

export default function ResetPasswordPage() {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get('token');
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    if (password !== confirmPassword) {
      toast({
        title: 'Password reset failed',
        description: 'Passwords do not match',
        variant: 'destructive',
      });
      setIsLoading(false);
      return;
    }

    if (password.length < 8) {
      toast({
        title: 'Password reset failed',
        description: 'Password must be at least 8 characters',
        variant: 'destructive',
      });
      setIsLoading(false);
      return;
    }

    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

      const response = await fetch(`${API_BASE_URL}/auth/reset-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token,
          new_password: password
        }),
      });

      const data = await response.json();

      if (response.ok) {
        toast({
          title: 'Password reset successful',
          description: 'Your password has been reset successfully. You can now log in with your new password.',
        });

        // Redirect to login page after a short delay
        setTimeout(() => {
          router.push('/login');
        }, 2000);
      } else {
        toast({
          title: 'Password reset failed',
          description: data.detail || 'Failed to reset password. Please try again.',
          variant: 'destructive',
        });
      }
    } catch (error: any) {
      toast({
        title: 'Password reset failed',
        description: error.message || 'An unexpected error occurred. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackToLogin = () => {
    router.push('/login');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md mx-auto card-3d bg-gradient-to-br from-background to-secondary/30 p-0.5 shadow-lg hover:shadow-xl transition-all duration-300">
        <div className="surface-3d rounded-lg">
          <CardHeader className="text-center">
            <CardTitle className="text-glow">Reset Password</CardTitle>
            <CardDescription className="text-glow">
              Enter your new password
            </CardDescription>
          </CardHeader>
          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-4 p-6">
              <div className="space-y-2">
                <Label htmlFor="password" className="text-glow">New Password</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter new password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength={8}
                  disabled={isLoading}
                  className="transition-all duration-300 focus:shadow-lg focus:ring-2 focus:ring-primary/50"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="confirmPassword" className="text-glow">Confirm New Password</Label>
                <Input
                  id="confirmPassword"
                  type="password"
                  placeholder="Confirm new password"
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
                {isLoading ? 'Resetting password...' : 'Reset Password'}
              </Button>
              <div className="mt-4 text-center text-sm">
                <button
                  type="button"
                  onClick={handleBackToLogin}
                  className="text-blue-600 hover:underline text-glow"
                  disabled={isLoading}
                >
                  Back to Login
                </button>
              </div>
            </CardFooter>
          </form>
        </div>
      </Card>
    </div>
  );
}