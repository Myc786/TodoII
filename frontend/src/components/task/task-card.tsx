'use client';

import { useState } from 'react';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { Task } from '@/lib/types';
import { cn } from '@/lib/utils';
import { Trash2, Pencil, Clock, Calendar, Bell } from 'lucide-react';
import { isTaskOverdue, formatDateForDisplay } from '@/lib/task-helpers';
import { ReminderSettings } from '@/components/task/reminder-settings';

interface TaskCardProps {
  task: Task;
  onToggle: (taskId: string, version: number) => void;
  onUpdate: (taskId: string, updates: Partial<Task>) => void;
  onDelete: (taskId: string) => void;
}

export function TaskCard({ task, onToggle, onDelete, onUpdate }: TaskCardProps) {
  // Determine priority badge variant
  const priorityVariants = {
    high: 'destructive',
    medium: 'default',
    low: 'secondary'
  } as const;
  const priorityVariant = priorityVariants[task.priority as keyof typeof priorityVariants] || 'default';

  // State for reminder settings
  const [showReminderSettings, setShowReminderSettings] = useState(false);

  const handleReminderSet = (taskId: string, reminderTime: Date, reminderType: 'email' | 'browser_notification' | 'both') => {
    // In a real implementation, this would call an API to create the reminder
    console.log(`Setting reminder for task ${taskId} at ${reminderTime} via ${reminderType}`);
    setShowReminderSettings(false);
  };

  return (
    <Card className={cn("card-3d surface-3d depth-2 rounded-lg transition-all duration-300", task.completed && 'opacity-75 animate-pulse')} aria-label={`${task.title} ${task.completed ? 'completed' : 'pending'} task`}>
      <CardContent className="p-4">
        <div className="flex items-start space-x-3">
          <Checkbox
            id={`task-${task.id}`}
            checked={task.completed}
            onCheckedChange={() => onToggle(task.id, task.version)}
            className="mt-1 checkbox-3d"
            aria-label={`Mark "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
          />
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <h3 className={cn(
                "font-medium text-lg leading-none tracking-tight truncate text-glow-heavy transition-all duration-300",
                task.completed && 'line-through text-muted-foreground'
              )}>
                {task.title}
              </h3>

              {/* Priority badge */}
              {task.priority && (
                <Badge variant={priorityVariant} className="ml-2 text-xs">
                  {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                </Badge>
              )}
            </div>

            {task.description && (
              <p className={cn(
                "text-sm text-muted-foreground mt-1 break-words transition-all duration-300 text-glow",
                task.completed && 'line-through'
              )}>
                {task.description}
              </p>
            )}

            {/* Tags */}
            {task.tags && task.tags.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-2">
                {task.tags.map(tag => (
                  <Badge key={tag.id} variant="secondary" className="text-xs">
                    {tag.name}
                  </Badge>
                ))}
              </div>
            )}

            {/* Due date */}
            {task.due_date && (
              <div className={`flex items-center mt-2 text-xs ${isTaskOverdue(task) ? 'text-red-500' : 'text-muted-foreground'}`}>
                <Calendar className="h-3 w-3 mr-1" />
                <span>Due: {formatDateForDisplay(task.due_date)}</span>
                {isTaskOverdue(task) && <span className="ml-1">(Overdue)</span>}
              </div>
            )}

            {/* Recurrence indicator */}
            {task.recurrence_pattern && (
              <div className="flex items-center mt-1 text-xs text-blue-500">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span>Recurring</span>
              </div>
            )}
          </div>
        </div>

        {/* Reminder Settings Panel */}
        {showReminderSettings && (
          <div className="mt-4 pt-4 border-t border-border">
            <ReminderSettings
              task={task}
              onReminderSet={handleReminderSet}
              disabled={task.completed}
            />
          </div>
        )}
      </CardContent>
      <CardFooter className="flex justify-between p-4 pt-0">
        <div className="flex items-center space-x-2">
          <Badge variant={task.completed ? 'secondary' : 'default'} className={cn(task.completed ? 'bg-green-500/20 text-green-600 dark:text-green-400 hover:bg-green-500/30' : 'bg-yellow-500/20 text-yellow-600 dark:text-yellow-400 hover:bg-yellow-500/30', 'depth-1')} aria-label={task.completed ? 'Task status: completed' : 'Task status: pending'}>
            {task.completed ? 'Completed' : 'Pending'}
          </Badge>

          {task.due_date && (
            <Badge variant={isTaskOverdue(task) ? 'destructive' : 'outline'} className="text-xs">
              <Clock className="h-3 w-3 mr-1" />
              {formatDateForDisplay(task.due_date)}
            </Badge>
          )}

          <span className="text-xs text-muted-foreground text-glow" aria-label={`Last updated: ${new Date(task.updated_at).toLocaleDateString()}`}>
            {new Date(task.updated_at).toLocaleDateString()}
          </span>
        </div>
        <div className="flex space-x-2">
          <Button
            variant="ghost"
            size="sm"
            className="button-3d depth-1"
            onClick={() => {
              // This would typically open an edit form or modal
              // For now, we'll just trigger the update callback with current values
              onUpdate(task.id, {
                title: task.title,
                description: task.description || '',
                priority: task.priority || 'medium',
                due_date: task.due_date
              });
            }}
            aria-label={`Edit task: ${task.title}`}
          >
            <Pencil className="h-4 w-4" aria-hidden="true" />
          </Button>

          <Button
            variant="ghost"
            size="sm"
            className="button-3d depth-1"
            onClick={() => setShowReminderSettings(!showReminderSettings)}
            aria-label={`Set reminder for task: ${task.title}`}
            disabled={task.completed}
          >
            <Bell className="h-4 w-4" aria-hidden="true" />
          </Button>

          <Button
            variant="ghost"
            size="sm"
            className="button-3d depth-1"
            onClick={() => onDelete(task.id)}
            aria-label={`Delete task: ${task.title}`}
          >
            <Trash2 className="h-4 w-4" aria-hidden="true" />
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
}