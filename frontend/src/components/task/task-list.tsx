'use client';

import { useState, useMemo, ReactNode } from 'react';
import { TaskCard } from './task-card';
import { Task } from '@/lib/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { SearchInput } from './search-input';
import { TaskFilters } from './task-filters';
import { SortControls } from './sort-controls';
import { Tag } from '@/lib/types';

interface TaskListProps {
  tasks?: Task[];
  loading?: boolean;
  onToggle: (taskId: string, version: number) => void;
  onUpdate: (taskId: string, updates: Partial<Task>) => void;
  onDelete: (taskId: string) => void;
  availableTags?: Tag[];
  emptyMessage?: ReactNode;
}

export function TaskList({
  tasks = [],
  loading,
  onToggle,
  onUpdate,
  onDelete,
  availableTags = [],
  emptyMessage = "No tasks found. Add a new task to get started!"
}: TaskListProps) {
  // State for search, filters, and sorting
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [priorityFilter, setPriorityFilter] = useState<string | null>(null);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [dueDateFilter, setDueDateFilter] = useState<'all' | 'overdue' | 'today' | 'week'>('all');
  const [sortBy, setSortBy] = useState<string>('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  // Handler functions
  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  const handleStatusChange = (status: 'all' | 'active' | 'completed') => {
    setStatusFilter(status);
  };

  const handlePriorityChange = (priority: string | null) => {
    setPriorityFilter(priority);
  };

  const handleTagToggle = (tagId: string) => {
    setSelectedTags(prev =>
      prev.includes(tagId)
        ? prev.filter(id => id !== tagId)
        : [...prev, tagId]
    );
  };

  const handleDueDateChange = (filter: 'all' | 'overdue' | 'today' | 'week') => {
    setDueDateFilter(filter);
  };

  const handleSortChange = (newSortBy: string, newSortOrder: 'asc' | 'desc') => {
    setSortBy(newSortBy);
    setSortOrder(newSortOrder);
  };

  // Filter and sort tasks
  const filteredAndSortedTasks = useMemo(() => {
    if (!tasks) return [];

    return tasks
      .filter(task => {
        // Search filter
        if (searchQuery) {
          const query = searchQuery.toLowerCase();
          if (
            !task.title.toLowerCase().includes(query) &&
            !(task.description && task.description.toLowerCase().includes(query))
          ) {
            return false;
          }
        }

        // Status filter
        if (statusFilter !== 'all') {
          if (statusFilter === 'active' && task.completed) return false;
          if (statusFilter === 'completed' && !task.completed) return false;
        }

        // Priority filter
        if (priorityFilter && task.priority !== priorityFilter) {
          return false;
        }

        // Tag filter
        if (selectedTags.length > 0) {
          if (!task.tags || task.tags.length === 0) return false;

          const hasSelectedTag = task.tags.some(tag =>
            selectedTags.includes(tag.id)
          );
          if (!hasSelectedTag) return false;
        }

        // Due date filter
        if (task.due_date && dueDateFilter !== 'all') {
          const dueDate = new Date(task.due_date);
          const today = new Date();
          today.setHours(0, 0, 0, 0);

          const endOfWeek = new Date(today);
          endOfWeek.setDate(today.getDate() + 7);

          switch (dueDateFilter) {
            case 'overdue':
              if (dueDate >= today) return false;
              break;
            case 'today':
              if (dueDate.toDateString() !== today.toDateString()) return false;
              break;
            case 'week':
              if (dueDate < today || dueDate > endOfWeek) return false;
              break;
          }
        }

        return true;
      })
      .sort((a, b) => {
        let aValue: any, bValue: any;

        switch (sortBy) {
          case 'due_date':
            aValue = a.due_date ? new Date(a.due_date).getTime() : Infinity;
            bValue = b.due_date ? new Date(b.due_date).getTime() : Infinity;
            break;
          case 'priority':
            // Define priority order: high > medium > low
            const priorityOrder: Record<string, number> = { 'high': 3, 'medium': 2, 'low': 1 };
            aValue = priorityOrder[a.priority || 'medium'] || 2;
            bValue = priorityOrder[b.priority || 'medium'] || 2;
            break;
          case 'title':
            aValue = a.title.toLowerCase();
            bValue = b.title.toLowerCase();
            break;
          case 'created_at':
          default:
            aValue = new Date(a.created_at).getTime();
            bValue = new Date(b.created_at).getTime();
            break;
        }

        if (sortOrder === 'asc') {
          return aValue > bValue ? 1 : aValue < bValue ? -1 : 0;
        } else {
          return aValue < bValue ? 1 : aValue > bValue ? -1 : 0;
        }
      });
  }, [tasks, searchQuery, statusFilter, priorityFilter, selectedTags, dueDateFilter, sortBy, sortOrder]);

  if (loading) {
    return (
      <Card className="card-3d surface-3d depth-3">
        <CardHeader>
          <CardTitle className="text-glow-heavy">Your Tasks</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="mb-4">
            <SearchInput onSearch={handleSearch} placeholder="Search tasks..." />
          </div>
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

  return (
    <Card className="card-3d surface-3d depth-3">
      <CardHeader>
        <CardTitle className="text-glow-heavy">Your Tasks ({filteredAndSortedTasks.length})</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-6 space-y-4">
          <SearchInput onSearch={handleSearch} placeholder="Search tasks..." />
          <TaskFilters
            activeFilter={statusFilter}
            onFilterChange={handleStatusChange}
            selectedPriority={priorityFilter}
            onPriorityChange={handlePriorityChange}
            selectedTags={selectedTags}
            onTagToggle={handleTagToggle}
            availableTags={availableTags}
            dueDateFilter={dueDateFilter}
            onDueDateChange={handleDueDateChange}
          />
          <SortControls
            sortBy={sortBy}
            sortOrder={sortOrder}
            onSortChange={handleSortChange}
          />
        </div>

        {filteredAndSortedTasks.length === 0 ? (
          <div className="text-center py-8">
            {typeof emptyMessage === 'string' ? (
              <p className="text-muted-foreground text-glow">{emptyMessage}</p>
            ) : (
              emptyMessage
            )}
          </div>
        ) : (
          <div className="space-y-4 container-3d">
            {filteredAndSortedTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onToggle={onToggle}
                onUpdate={onUpdate}
                onDelete={onDelete}
              />
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}