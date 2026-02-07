'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { validateTaskTitle } from '@/lib/utils';
import apiClient from '@/lib/api';
import { Task, Tag, CreateTaskRequest, UpdateTaskRequest, RecurrencePattern } from '@/lib/types';
import { PrioritySelector } from '@/components/task/priority-selector';
import { TagInput } from '@/components/task/tag-input';
import { RecurrenceInput } from '@/components/task/recurrence-input';
import { useToast } from '@/components/ui/use-toast';

interface TaskFormProps {
  onTaskCreated?: (task: Task) => void;
  onTaskUpdated?: (task: Task) => void;
  onCancel?: () => void;
  initialValues?: Partial<CreateTaskRequest>;
  availableTags?: Tag[];
  taskId?: string; // For updates
}

export function TaskForm({
  onTaskCreated,
  onTaskUpdated,
  onCancel,
  initialValues,
  availableTags = [],
  taskId
}: TaskFormProps) {
  const [title, setTitle] = useState(initialValues?.title || '');
  const [description, setDescription] = useState(initialValues?.description || '');
  const [priority, setPriority] = useState(initialValues?.priority || 'medium');
  const [selectedTags, setSelectedTags] = useState<Tag[]>([]);
  const [recurrencePattern, setRecurrencePattern] = useState<RecurrencePattern | undefined>(
    initialValues?.recurrence_pattern ? JSON.parse(initialValues.recurrence_pattern) : undefined
  );
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { toast } = useToast();

  // Load initial tags if available
  useEffect(() => {
    if (initialValues?.tag_ids && availableTags) {
      const initialSelectedTags = availableTags.filter(tag =>
        initialValues.tag_ids?.includes(tag.id)
      );
      setSelectedTags(initialSelectedTags);
    }
  }, [initialValues?.tag_ids, availableTags]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const validation = validateTaskTitle(title);
    if (!validation.isValid) {
      setError(validation.error || null);
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const taskData: CreateTaskRequest = {
        title,
        description: description || undefined,
        priority,
        recurrence_pattern: recurrencePattern ? JSON.stringify(recurrencePattern) : undefined,
        tag_ids: selectedTags.map(tag => tag.id)
      };

      let response;
      if (taskId) {
        // Update existing task
        const updateData: UpdateTaskRequest = {
          ...taskData,
          version: 1, // This should come from the task object in a real implementation
          title: taskData.title,
          description: taskData.description,
          priority: taskData.priority,
          tag_ids: taskData.tag_ids
        };

        response = await apiClient.updateTask(taskId, updateData);
        if (response.success && response.data && onTaskUpdated) {
          onTaskUpdated(response.data);
          toast({
            title: "Task updated",
            description: "Your task has been updated successfully."
          });
        }
      } else {
        // Create new task
        response = await apiClient.createTask(taskData);
        if (response.success && response.data && onTaskCreated) {
          onTaskCreated(response.data);
          toast({
            title: "Task created",
            description: "Your task has been created successfully."
          });

          // Reset form after successful submission
          setTitle('');
          setDescription('');
          setPriority('medium');
          setSelectedTags([]);
        }
      }

      if (!response.success) {
        setError(response.error || (taskId ? 'Failed to update task' : 'Failed to create task'));
      }
    } catch (err) {
      setError(`An error occurred while ${taskId ? 'updating' : 'creating'} the task`);
      console.error(`${taskId ? 'Task update' : 'Task creation'} error:`, err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleTagSelect = (tag: Tag) => {
    if (!selectedTags.some(t => t.id === tag.id)) {
      setSelectedTags([...selectedTags, tag]);
    }
  };

  const handleTagRemove = (tagId: string) => {
    setSelectedTags(selectedTags.filter(tag => tag.id !== tagId));
  };

  const handleTagCreate = async (tagName: string) => {
    try {
      // call API to create tag
      const response = await apiClient.createTag({ name: tagName });

      if (response.success && response.data) {
        // Add the real tag from the server
        setSelectedTags([...selectedTags, response.data]);
        toast({
          title: "Tag created",
          description: `Tag "${tagName}" created successfully.`
        });
      } else {
        toast({
          title: "Error",
          description: response.error || "Failed to create tag",
          variant: "destructive"
        });
      }
    } catch (err) {
      console.error("Tag creation error:", err);
      toast({
        title: "Error",
        description: "An unexpected error occurred while creating the tag",
        variant: "destructive"
      });
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

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-glow">
            Priority
          </label>
          <PrioritySelector
            value={priority}
            onChange={setPriority}
            disabled={isSubmitting}
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-glow">
            Tags
          </label>
          <TagInput
            selectedTags={selectedTags}
            availableTags={availableTags}
            onTagSelect={handleTagSelect}
            onTagRemove={handleTagRemove}
            onTagCreate={handleTagCreate}
            placeholder="Select or create tags..."
            disabled={isSubmitting}
          />
        </div>
      </div>

      <div className="space-y-2">
        <RecurrenceInput
          value={recurrencePattern}
          onChange={setRecurrencePattern}
          disabled={isSubmitting}
        />
      </div>

      {error && (
        <div className="text-sm text-red-600 text-glow">
          {error}
        </div>
      )}

      <div className="flex space-x-2 pt-2">
        <Button type="submit" disabled={!title.trim() || isSubmitting} className="button-3d flex-1">
          {isSubmitting ? `${taskId ? 'Updating' : 'Creating'}...` : (taskId ? 'Update Task' : 'Add Task')}
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