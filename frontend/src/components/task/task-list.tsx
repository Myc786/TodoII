import { TaskCard } from './task-card';
import { Task } from '@/lib/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

interface TaskListProps {
  tasks?: Task[];
  loading?: boolean;
  onToggle: (taskId: string, version: number) => void;
  onUpdate: (taskId: string, updates: Partial<Task>) => void;
  onDelete: (taskId: string) => void;
  emptyMessage?: string;
}

export function TaskList({
  tasks,
  loading,
  onToggle,
  onUpdate,
  onDelete,
  emptyMessage = "No tasks found. Add a new task to get started!"
}: TaskListProps) {
  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Your Tasks</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[...Array(3)].map((_, index) => (
              <div key={index} className="flex items-center space-x-4">
                <Skeleton className="h-5 w-5" />
                <div className="space-y-2">
                  <Skeleton className="h-4 w-[250px]" />
                  <Skeleton className="h-4 w-[200px]" />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (tasks && tasks.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Your Tasks</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <p className="text-muted-foreground">{emptyMessage}</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Tasks ({tasks?.length || 0})</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {tasks?.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onToggle={onToggle}
              onUpdate={onUpdate}
              onDelete={onDelete}
            />
          ))}
        </div>
      </CardContent>
    </Card>
  );
}