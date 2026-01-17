import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { Task } from '@/lib/types';

interface StatusBadgeProps {
  completed: boolean;
}

export function StatusBadge({ completed }: StatusBadgeProps) {
  return (
    <Badge
      variant={completed ? 'secondary' : 'default'}
      className={cn(
        completed
          ? 'bg-green-100 text-green-800 hover:bg-green-100'
          : 'bg-yellow-100 text-yellow-800 hover:bg-yellow-100'
      )}
    >
      {completed ? 'Completed' : 'Pending'}
    </Badge>
  );
}