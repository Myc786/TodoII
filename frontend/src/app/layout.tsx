import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { AuthWrapper } from '@/components/auth/auth-wrapper';
import { ThemeProvider } from 'next-themes';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A simple todo application built with Next.js and Tailwind CSS',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <AuthWrapper>
            {children}
          </AuthWrapper>
        </ThemeProvider>
      </body>
    </html>
  );
}