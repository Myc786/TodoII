'use client';

import { Button } from '@/components/ui/button';

interface TaskFiltersProps {
  activeFilter: 'all' | 'active' | 'completed';
  onFilterChange: (filter: 'all' | 'active' | 'completed') => void;
}

export function TaskFilters({ activeFilter, onFilterChange }: TaskFiltersProps) {
  return (
    <div className="flex space-x-2 mb-4">
      <Button
        variant={activeFilter === 'all' ? 'default' : 'outline'}
        className="button-3d"
        onClick={() => onFilterChange('all')}
      >
        All
      </Button>
      <Button
        variant={activeFilter === 'active' ? 'default' : 'outline'}
        className="button-3d"
        onClick={() => onFilterChange('active')}
      >
        Active
      </Button>
      <Button
        variant={activeFilter === 'completed' ? 'default' : 'outline'}
        className="button-3d"
        onClick={() => onFilterChange('completed')}
      >
        Completed
      </Button>
    </div>
  );
}