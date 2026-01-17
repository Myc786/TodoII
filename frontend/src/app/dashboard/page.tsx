'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TaskList } from '@/components/task/task-list';
import { TaskForm } from '@/components/task/task-form';
import { TaskFilters } from '@/components/task/task-filters';
import { Task } from '@/lib/types';
import apiClient from '@/lib/api';

export default function DashboardPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading, user, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState<'all' | 'active' | 'completed'>('all');

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    } else if (isAuthenticated) {
      loadTasks();
    }
  }, [isAuthenticated, isLoading, router]);

  const loadTasks = async () => {
    setLoading(true);
    try {
      const response = await apiClient.getTasks();
      if (response.success && response.data) {
        setTasks(response.data);
      }
    } catch (error) {
      console.error('Failed to load tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskCreated = (newTask: Task) => {
    setTasks(prev => [newTask, ...prev]);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(prev => prev.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (deletedTaskId: string) => {
    setTasks(prev => prev.filter(task => task.id !== deletedTaskId));
  };

  const handleTaskToggle = async (taskId: string, version: number) => {
    try {
      const response = await apiClient.toggleTaskCompletion(taskId, { version });
      if (response.success && response.data) {
        handleTaskUpdated(response.data);
      }
    } catch (error) {
      console.error('Failed to toggle task:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mb-4"></div>
          <p className="text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will be redirected by useEffect
  }

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold">Todo Dashboard</h1>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground">
              Welcome, {user?.name || user?.email}!
            </span>
            <Button variant="outline" size="sm" onClick={handleLogout}>
              Logout
            </Button>
          </div>
        </div>
      </header>

      <main className="container py-8">
        <div className="max-w-4xl mx-auto space-y-8">
          <Card>
            <CardHeader>
              <CardTitle>Create New Task</CardTitle>
            </CardHeader>
            <CardContent>
              <TaskForm onTaskCreated={handleTaskCreated} />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Your Tasks</CardTitle>
            </CardHeader>
            <CardContent>
              <TaskFilters activeFilter={activeFilter} onFilterChange={setActiveFilter} />
              <TaskList
                tasks={tasks.filter(task => {
                  if (activeFilter === 'active') return !task.completed;
                  if (activeFilter === 'completed') return task.completed;
                  return true; // 'all' filter
                })}
                loading={loading}
                onToggle={handleTaskToggle}
                onUpdate={handleTaskUpdated}
                onDelete={handleTaskDeleted}
              />
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}