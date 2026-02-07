'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TaskList } from '@/components/task/task-list';
import { TaskForm } from '@/components/task/task-form';
import { TagManager } from '@/components/task/tag-manager';
import { Task, Tag } from '@/lib/types';
import apiClient from '@/lib/api';

export default function DashboardPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading, user, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    } else if (isAuthenticated) {
      loadTasksAndTags();
    }
  }, [isAuthenticated, isLoading, router]);

  const loadTasksAndTags = async () => {
    setLoading(true);
    try {
      // Load both tasks and tags
      const [tasksResponse, tagsResponse] = await Promise.all([
        apiClient.getTasks(),
        apiClient.getTags()
      ]);

      if (tasksResponse.success && tasksResponse.data) {
        setTasks(tasksResponse.data);
      }

      if (tagsResponse.success && tagsResponse.data) {
        setTags(tagsResponse.data);
      }
    } catch (error) {
      console.error('Failed to load tasks or tags:', error);
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

  const handleTaskDelete = async (taskId: string) => {
    try {
      const response = await apiClient.deleteTask(taskId);
      if (response.success) {
        setTasks(prev => prev.filter(task => task.id !== taskId));
      } else {
        console.error('Failed to delete task:', response.error);
      }
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const handleTaskUpdate = async (taskId: string, updates: any) => {
    try {
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      const response = await apiClient.updateTask(taskId, {
        ...updates,
        version: task.version
      });

      if (response.success && response.data) {
        handleTaskUpdated(response.data);
      }
    } catch (error) {
      console.error('Failed to update task:', error);
    }
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

  // Tag management functions
  const handleTagCreate = async (name: string, color?: string) => {
    try {
      const response = await apiClient.createTag({ name, color });
      if (response.success && response.data) {
        const newTag = response.data;
        setTags(prev => [...prev, newTag]);
      }
    } catch (error) {
      console.error('Failed to create tag:', error);
    }
  };

  const handleTagDelete = async (id: string) => {
    try {
      await apiClient.deleteTag(id);
      setTags(prev => prev.filter(tag => tag.id !== id));
      // Also remove this tag from any tasks that had it
      setTasks(prev => prev.map(task => ({
        ...task,
        tags: task.tags?.filter(tag => tag.id !== id)
      })));
    } catch (error) {
      console.error('Failed to delete tag:', error);
    }
  };

  const handleTagUpdate = async (id: string, name: string, color?: string) => {
    try {
      const response = await apiClient.updateTag(id, { name, color });
      if (response.success && response.data) {
        const updatedTag = response.data;
        setTags(prev => prev.map(tag => tag.id === id ? updatedTag : tag));
      }
    } catch (error) {
      console.error('Failed to update tag:', error);
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
    <div className="min-h-screen bg-gradient-to-br from-background via-secondary/10 to-background">
      <header className="border-b glass-effect backdrop-blur-lg">
        <div className="container flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold text-glow-heavy">Todo Dashboard</h1>
          </div>
          <div className="flex items-center gap-4">
            <TagManager
              tags={tags}
              onTagCreate={handleTagCreate}
              onTagDelete={handleTagDelete}
              onTagUpdate={handleTagUpdate}
            />
            <span className="text-sm text-glow">
              Welcome, {user?.name || user?.email}!
            </span>
            <Button variant="outline" size="sm" onClick={handleLogout} className="button-3d">
              Logout
            </Button>
          </div>
        </div>
      </header>

      <main className="container py-8">
        <div className="max-w-4xl mx-auto space-y-8">
          <Card className="card-3d surface-3d depth-3">
            <CardHeader>
              <CardTitle className="text-glow-heavy">Create New Task</CardTitle>
            </CardHeader>
            <CardContent>
              <TaskForm
                onTaskCreated={handleTaskCreated}
                availableTags={tags}
              />
            </CardContent>
          </Card>

          <Card className="card-3d surface-3d depth-3">
            <CardHeader>
              <CardTitle className="text-glow-heavy">Your Tasks</CardTitle>
            </CardHeader>
            <CardContent>
              <TaskList
                tasks={tasks}
                loading={loading}
                onToggle={handleTaskToggle}
                onUpdate={handleTaskUpdate}
                onDelete={handleTaskDelete}
                availableTags={tags}
              />
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}