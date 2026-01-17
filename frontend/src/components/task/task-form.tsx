'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { validateTaskTitle } from '@/lib/utils';
import apiClient from '@/lib/api';
import { Task } from '@/lib/types';

interface TaskFormProps {
  onTaskCreated?: (task: Task) => void;
  onCancel?: () => void;
  initialValues?: Partial<{ title: string; description?: string }>;
}

export function TaskForm({ onTaskCreated, onCancel, initialValues }: TaskFormProps) {
  const [title, setTitle] = useState(initialValues?.title || '');
  const [description, setDescription] = useState(initialValues?.description || '');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const validation = validateTaskTitle(title);
    if (!validation.isValid) {
      setError(validation.error);
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const response = await apiClient.createTask({
        title,
        description: description || undefined
      });

      if (response.success && response.data) {
        if (onTaskCreated) {
          onTaskCreated(response.data);
        }
        // Reset form after successful submission
        setTitle('');
        setDescription('');
      } else {
        setError(response.error || 'Failed to create task');
      }
    } catch (err) {
      setError('An error occurred while creating the task');
      console.error('Task creation error:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <label htmlFor="title" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-glow">
          Title *
        </label>
        <Input
          id="title"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            if (error) setError(null);
          }}
          placeholder="What needs to be done?"
          required
          disabled={isSubmitting}
          className="transition-all duration-300 focus:shadow-lg focus:ring-2 focus:ring-primary/50"
        />
      </div>

      <div className="space-y-2">
        <label htmlFor="description" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-glow">
          Description
        </label>
        <Textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add details..."
          disabled={isSubmitting}
          className="transition-all duration-300 focus:shadow-lg focus:ring-2 focus:ring-primary/50"
        />
      </div>

      {error && (
        <div className="text-sm text-red-600 text-glow">
          {error}
        </div>
      )}

      <div className="flex space-x-2 pt-2">
        <Button type="submit" disabled={!title.trim() || isSubmitting} className="button-3d flex-1">
          {isSubmitting ? 'Creating...' : (initialValues ? 'Update Task' : 'Add Task')}
        </Button>
        {onCancel && (
          <Button type="button" variant="outline" onClick={onCancel} disabled={isSubmitting} className="button-3d">
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
}