'use client';

import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { Task } from '@/lib/types';
import { cn } from '@/lib/utils';
import { Trash2, Pencil } from 'lucide-react';

interface TaskCardProps {
  task: Task;
  onToggle: (taskId: string, version: number) => void;
  onUpdate: (taskId: string, updates: Partial<Task>) => void;
  onDelete: (taskId: string) => void;
}

export function TaskCard({ task, onToggle, onDelete, onUpdate }: TaskCardProps) {
  return (
    <Card className={cn("card-3d bg-gradient-to-br from-background to-secondary/30 p-0.5 shadow-lg hover:shadow-xl transition-all duration-300", task.completed && 'opacity-75 animate-pulse')} aria-label={`${task.title} ${task.completed ? 'completed' : 'pending'} task`}>
      <div className="surface-3d h-full">
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
              <h3 className={cn(
                "font-medium text-lg leading-none tracking-tight truncate text-glow transition-all duration-300",
                task.completed && 'line-through text-muted-foreground'
              )}>
                {task.title}
              </h3>
              {task.description && (
                <p className={cn(
                  "text-sm text-muted-foreground mt-1 break-words transition-all duration-300",
                  task.completed && 'line-through'
                )}>
                  {task.description}
                </p>
              )}
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between p-4 pt-0">
          <div className="flex items-center space-x-2">
            <Badge variant={task.completed ? 'secondary' : 'default'} className={task.completed ? 'bg-green-500/20 text-green-600 dark:text-green-400 hover:bg-green-500/30' : 'bg-yellow-500/20 text-yellow-600 dark:text-yellow-400 hover:bg-yellow-500/30'} aria-label={task.completed ? 'Task status: completed' : 'Task status: pending'}>
              {task.completed ? 'Completed' : 'Pending'}
            </Badge>
            <span className="text-xs text-muted-foreground" aria-label={`Last updated: ${new Date(task.updated_at).toLocaleDateString()}`}>
              {new Date(task.updated_at).toLocaleDateString()}
            </span>
          </div>
          <div className="flex space-x-2">
            <Button
              variant="ghost"
              size="sm"
              className="button-3d"
              onClick={() => {
                // This would typically open an edit form or modal
                // For now, we'll just trigger the update callback with current values
                onUpdate(task.id, { title: task.title, description: task.description || '' });
              }}
              aria-label={`Edit task: ${task.title}`}
            >
              <Pencil className="h-4 w-4" aria-hidden="true" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              className="button-3d"
              onClick={() => onDelete(task.id)}
              aria-label={`Delete task: ${task.title}`}
            >
              <Trash2 className="h-4 w-4" aria-hidden="true" />
            </Button>
          </div>
        </CardFooter>
      </div>
    </Card>
  );
}