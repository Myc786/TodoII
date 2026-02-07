'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Header } from '@/components/layout/header';
import { TaskCard } from '@/components/task/task-card';
import { TaskForm } from '@/components/task/task-form';
import { TaskList } from '@/components/task/task-list';
import { apiClient } from '@/lib/api';
import { Task } from '@/lib/types';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/hooks/use-auth';

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const { toast } = useToast();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  // Fetch tasks on component mount (only if authenticated)
  useEffect(() => {
    if (!isAuthenticated || authLoading) return;

    const fetchTasks = async () => {
      try {
        setLoading(true);
        const response = await apiClient.getTasks();
        if (response.success && response.data) {
          setTasks(response.data);
        } else {
          toast({
            title: 'Error',
            description: response.error || 'Failed to fetch tasks',
            variant: 'destructive',
          });
        }
      } catch (error) {
        toast({
          title: 'Error',
          description: 'An unexpected error occurred while fetching tasks',
          variant: 'destructive',
        });
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [isAuthenticated, authLoading]);

  // Listen for external task updates (e.g., from chatbot)
  useEffect(() => {
    const handleTaskUpdate = () => {
      // Re-fetch tasks when an external update occurs
      apiClient.getTasks().then(response => {
        if (response.success && response.data) {
          setTasks(response.data);
        }
      });
    };

    window.addEventListener('task-updated', handleTaskUpdate);
    return () => window.removeEventListener('task-updated', handleTaskUpdate);
  }, [isAuthenticated, authLoading]);

  // Show loading if auth is loading
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mb-4"></div>
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return null; // Will be redirected by useEffect
  }

  // Handler functions
  const handleAddTask = async (task: Task) => {
    // Task is already created by TaskForm, just update state
    setTasks([task, ...tasks]);
    // Toast is already shown by TaskForm
  };

  const handleToggleTask = async (taskId: string, version: number) => {
    try {
      // Optimistic update
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? { ...task, completed: !task.completed, version: task.version + 1 } : task
        )
      );

      const response = await apiClient.toggleTaskCompletion(taskId, { version: version + 1 });
      if (response.success && response.data) {
        // Update with server response in case of any changes
        setTasks(prevTasks =>
          prevTasks.map(task =>
            task.id === taskId ? response.data! : task
          )
        );
      } else {
        // Rollback on error
        setTasks(prevTasks =>
          prevTasks.map(task =>
            task.id === taskId ? { ...task, completed: !task.completed, version: task.version - 1 } : task
          )
        );
        toast({
          title: 'Error',
          description: response.error || 'Failed to update task',
          variant: 'destructive',
        });
      }
    } catch (error) {
      // Rollback on error
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? { ...task, completed: !task.completed } : task
        )
      );
      toast({
        title: 'Error',
        description: 'Failed to update task',
        variant: 'destructive',
      });
    }
  };

  const handleUpdateTask = async (taskId: string, updates: Partial<Task>) => {
    try {
      const taskToUpdate = tasks.find(task => task.id === taskId);
      if (!taskToUpdate) return;

      // Optimistic update
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? { ...task, ...updates } : task
        )
      );

      const updateData = {
        title: updates.title || taskToUpdate.title,
        description: updates.description || taskToUpdate.description,
        completed: updates.completed ?? taskToUpdate.completed,
        version: taskToUpdate.version + 1
      };

      const response = await apiClient.updateTask(taskId, updateData);
      if (response.success && response.data) {
        // Update with server response in case of any changes
        setTasks(prevTasks =>
          prevTasks.map(task =>
            task.id === taskId ? response.data! : task
          )
        );
      } else {
        // Rollback on error
        setTasks(prevTasks =>
          prevTasks.map(task =>
            task.id === taskId ? { ...task, ...taskToUpdate } : task
          )
        );
        toast({
          title: 'Error',
          description: response.error || 'Failed to update task',
          variant: 'destructive',
        });
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update task',
        variant: 'destructive',
      });
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      // Optimistic update
      setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));

      const response = await apiClient.deleteTask(taskId);
      if (!response.success) {
        // Rollback on error
        const deletedTask = tasks.find(task => task.id === taskId);
        if (deletedTask) {
          setTasks(prevTasks => [...prevTasks, deletedTask]);
        }
        toast({
          title: 'Error',
          description: response.error || 'Failed to delete task',
          variant: 'destructive',
        });
      } else {
        toast({
          title: 'Success',
          description: 'Task deleted successfully',
        });
      }
    } catch (error) {
      // Rollback on error
      const deletedTask = tasks.find(task => task.id === taskId);
      if (deletedTask) {
        setTasks(prevTasks => [...prevTasks, deletedTask]);
      }
      toast({
        title: 'Error',
        description: 'Failed to delete task',
        variant: 'destructive',
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-secondary/10 to-background">
      <Header />
      <main className="container mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-8 container-3d">
          <h1 className="text-4xl font-bold tracking-tight text-glow-heavy text-center lg:text-left floating-element">Dashboard</h1>
          <p className="text-muted-foreground mt-2 text-center lg:text-left text-glow">
            Welcome back, {user?.name || user?.email}! Manage your tasks efficiently.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Task List Section */}
          <div className="lg:col-span-2">
            <div className="card-3d surface-3d depth-3 rounded-xl">
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-glow-heavy">Your Tasks</h2>
                  <span className="text-sm text-muted-foreground text-glow">
                    {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
                  </span>
                </div>

                <TaskList
                  tasks={tasks}
                  loading={loading}
                  onToggle={handleToggleTask}
                  onUpdate={handleUpdateTask}
                  onDelete={handleDeleteTask}
                  emptyMessage={
                    <div className="text-center py-12">
                      <div className="mx-auto h-16 w-16 rounded-full bg-gradient-to-br from-muted to-secondary flex items-center justify-center mb-4 shadow-inner glass-effect">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                        </svg>
                      </div>
                      <h3 className="text-lg font-medium mb-1 text-glow-heavy">No tasks yet</h3>
                      <p className="text-muted-foreground mb-4 text-glow">Get started by creating your first task</p>
                    </div>
                  }
                />
              </div>
            </div>
          </div>

          {/* Task Form Section */}
          <div className="lg:col-span-1">
            <div className="card-3d surface-3d depth-3 rounded-xl sticky top-6 mb-6">
              <div className="p-6">
                <h2 className="text-xl font-semibold mb-6 text-glow-heavy">Add New Task</h2>
                <TaskForm onTaskCreated={handleAddTask} />
              </div>
            </div>

            {/* Stats Section */}
            <div className="card-3d surface-3d depth-3 rounded-xl">
              <div className="p-6">
                <h3 className="font-medium mb-4 text-glow-heavy">Quick Stats</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 rounded-md bg-secondary/20 hover:bg-secondary/30 transition-colors depth-1">
                    <span className="text-muted-foreground text-glow">Total Tasks</span>
                    <span className="font-medium text-glow-heavy">{tasks.length}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 rounded-md bg-secondary/20 hover:bg-secondary/30 transition-colors depth-1">
                    <span className="text-muted-foreground text-glow">Completed</span>
                    <span className="font-medium text-glow-heavy">{tasks.filter(t => t.completed).length}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 rounded-md bg-secondary/20 hover:bg-secondary/30 transition-colors depth-1">
                    <span className="text-muted-foreground text-glow">Pending</span>
                    <span className="font-medium text-glow-heavy">{tasks.filter(t => !t.completed).length}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}