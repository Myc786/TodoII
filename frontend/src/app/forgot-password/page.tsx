'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);
  const router = useRouter();
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

      const response = await fetch(`${API_BASE_URL}/auth/forgot-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setEmailSent(true);
        toast({
          title: 'Password reset email sent',
          description: data.message || `We've sent a password reset link to ${email}. Please check your inbox.`,
        });
      } else {
        toast({
          title: 'Password reset failed',
          description: data.detail || 'Failed to send password reset email. Please try again.',
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

  if (emailSent) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background p-4">
        <Card className="w-full max-w-md mx-auto card-3d bg-gradient-to-br from-background to-secondary/30 p-0.5 shadow-lg hover:shadow-xl transition-all duration-300">
          <div className="surface-3d rounded-lg">
            <CardHeader className="text-center">
              <CardTitle className="text-glow">Check Your Email</CardTitle>
              <CardDescription className="text-glow">
                We've sent a password reset link to your email address
              </CardDescription>
            </CardHeader>
            <CardContent className="p-6 text-center">
              <p>We sent a password reset link to:</p>
              <p className="font-semibold mt-2 text-glow">{email}</p>
              <p className="mt-4 text-sm text-muted-foreground">
                Didn't receive the email? Check your spam folder or request a new link.
              </p>
            </CardContent>
            <CardFooter className="flex flex-col p-6 pt-0">
              <Button onClick={handleBackToLogin} className="w-full button-3d">
                Back to Login
              </Button>
            </CardFooter>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md mx-auto card-3d bg-gradient-to-br from-background to-secondary/30 p-0.5 shadow-lg hover:shadow-xl transition-all duration-300">
        <div className="surface-3d rounded-lg">
          <CardHeader className="text-center">
            <CardTitle className="text-glow">Reset Password</CardTitle>
            <CardDescription className="text-glow">
              Enter your email and we'll send you a link to reset your password
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
            </CardContent>
            <CardFooter className="flex flex-col p-6 pt-0">
              <Button type="submit" className="w-full button-3d" disabled={isLoading}>
                {isLoading ? 'Sending reset link...' : 'Send Reset Link'}
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