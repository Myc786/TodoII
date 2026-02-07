import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { AuthWrapper } from '@/components/auth/auth-wrapper';
import { ThemeProvider } from '@/contexts/theme-context';
import { AuthenticatedChatWidget } from '@/components/chatbot/authenticated-chat-widget';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A simple todo application built with Next.js and Tailwind CSS',
};

import { Toaster } from "@/components/ui/toaster";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider>
          <AuthWrapper>
            {children}
            <AuthenticatedChatWidget />
            <Toaster />
          </AuthWrapper>
        </ThemeProvider>
      </body>
    </html>
  );
}