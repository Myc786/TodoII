'use client';

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface PrioritySelectorProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
  className?: string;
}

export function PrioritySelector({ value, onChange, disabled = false, className }: PrioritySelectorProps) {
  const priorityOptions = [
    { value: 'low', label: 'Low', badgeVariant: 'secondary' },
    { value: 'medium', label: 'Medium', badgeVariant: 'default' },
    { value: 'high', label: 'High', badgeVariant: 'destructive' },
  ];

  const selectedOption = priorityOptions.find(option => option.value === value) || priorityOptions[1]; // Default to medium

  return (
    <Select value={value} onValueChange={onChange} disabled={disabled}>
      <SelectTrigger className={cn("w-[180px]", className)}>
        <Badge
          variant={selectedOption.badgeVariant as 'default' | 'secondary' | 'destructive' | 'outline'}
          className="mr-2"
        >
          {selectedOption.label}
        </Badge>
        <SelectValue placeholder="Select priority" />
      </SelectTrigger>
      <SelectContent>
        {priorityOptions.map((option) => (
          <SelectItem key={option.value} value={option.value}>
            <div className="flex items-center">
              <Badge
                variant={option.badgeVariant as 'default' | 'secondary' | 'destructive' | 'outline'}
                className="mr-2"
              >
                {option.label}
              </Badge>
            </div>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}