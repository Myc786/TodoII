'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tag } from '@/lib/types';

interface TaskFiltersProps {
  activeFilter: 'all' | 'active' | 'completed';
  onFilterChange: (filter: 'all' | 'active' | 'completed') => void;
  selectedPriority: string | null;
  onPriorityChange: (priority: string | null) => void;
  selectedTags: string[];
  onTagToggle: (tagId: string) => void;
  availableTags: Tag[];
  dueDateFilter: 'all' | 'overdue' | 'today' | 'week';
  onDueDateChange: (filter: 'all' | 'overdue' | 'today' | 'week') => void;
}

export function TaskFilters({
  activeFilter,
  onFilterChange,
  selectedPriority,
  onPriorityChange,
  selectedTags,
  onTagToggle,
  availableTags,
  dueDateFilter,
  onDueDateChange
}: TaskFiltersProps) {
  const priorityOptions = [
    { value: 'high', label: 'High', color: 'bg-red-500' },
    { value: 'medium', label: 'Medium', color: 'bg-yellow-500' },
    { value: 'low', label: 'Low', color: 'bg-green-500' },
  ];

  const dueDateOptions = [
    { value: 'all', label: 'All Dates' },
    { value: 'overdue', label: 'Overdue' },
    { value: 'today', label: 'Today' },
    { value: 'week', label: 'This Week' },
  ];

  const activeFilters = [];

  if (activeFilter !== 'all') {
    activeFilters.push(activeFilter === 'active' ? 'Active' : 'Completed');
  }

  if (selectedPriority) {
    const priorityLabel = priorityOptions.find(p => p.value === selectedPriority)?.label;
    if (priorityLabel) {
      activeFilters.push(priorityLabel);
    }
  }

  if (selectedTags.length > 0) {
    selectedTags.forEach(tagId => {
      const tag = availableTags.find(t => t.id === tagId);
      if (tag) {
        activeFilters.push(tag.name);
      }
    });
  }

  if (dueDateFilter !== 'all') {
    const dueDateLabel = dueDateOptions.find(d => d.value === dueDateFilter)?.label;
    if (dueDateLabel) {
      activeFilters.push(dueDateLabel);
    }
  }

  const clearFilter = (filterType: string) => {
    switch (filterType) {
      case 'status':
        onFilterChange('all');
        break;
      case 'priority':
        onPriorityChange(null);
        break;
      case 'tags':
        selectedTags.forEach(tagId => onTagToggle(tagId));
        break;
      case 'dueDate':
        onDueDateChange('all');
        break;
    }
  };

  return React.createElement('div', { className: 'w-full' }, [
    React.createElement('div', {
      key: 'filters',
      className: 'flex flex-wrap gap-2 mb-4'
    }, [
      React.createElement('div', { key: 'status', className: 'flex flex-wrap gap-1' }, [
        React.createElement(Button, {
          key: 'all',
          variant: activeFilter === 'all' ? 'default' : 'outline',
          className: 'button-3d text-xs sm:text-sm',
          onClick: () => onFilterChange('all')
        }, 'All'),
        React.createElement(Button, {
          key: 'active',
          variant: activeFilter === 'active' ? 'default' : 'outline',
          className: 'button-3d text-xs sm:text-sm',
          onClick: () => onFilterChange('active')
        }, 'Active'),
        React.createElement(Button, {
          key: 'completed',
          variant: activeFilter === 'completed' ? 'default' : 'outline',
          className: 'button-3d text-xs sm:text-sm',
          onClick: () => onFilterChange('completed')
        }, 'Completed'),
      ])
    ]),

    activeFilters.length > 0 && React.createElement('div', {
      key: 'active-filters',
      className: 'flex flex-wrap gap-2 mb-4'
    }, [
      React.createElement('span', {
        className: 'text-xs text-muted-foreground'
      }, 'Active filters:'),
      ...activeFilters.map((filter, index) =>
        React.createElement(Badge, {
          key: index,
          variant: 'secondary',
          className: 'text-xs'
        }, filter)
      )
    ])
  ]);
}