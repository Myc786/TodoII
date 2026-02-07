// Helper functions for working with new data structures
import { Task, Tag } from './types';

/**
 * Validates if a priority level is valid
 * @param priority - The priority level to validate
 * @returns boolean indicating if the priority is valid
 */
export function isValidPriority(priority: string | undefined): boolean {
  if (!priority) return true; // Allow undefined
  return ['high', 'medium', 'low'].includes(priority.toLowerCase());
}

/**
 * Validates if a date string is in valid ISO format
 * @param dateString - The date string to validate
 * @returns boolean indicating if the date is valid
 */
export function isValidDate(dateString: string | undefined): boolean {
  if (!dateString) return true; // Allow undefined
  const date = new Date(dateString);
  return !isNaN(date.getTime()); // Valid date
}

/**
 * Formats a date for display
 * @param date - The date to format
 * @returns Formatted date string
 */
export function formatDateForDisplay(date: string | undefined): string {
  if (!date) return '';
  return new Date(date).toLocaleDateString();
}

/**
 * Formats a date for API requests
 * @param date - The date to format
 * @returns Formatted date string for API
 */
export function formatDateForApi(date: Date | string | undefined): string | undefined {
  if (!date) return undefined;
  if (typeof date === 'string') return date;
  return date.toISOString();
}

/**
 * Validates recurrence pattern structure
 * @param pattern - The recurrence pattern to validate
 * @returns boolean indicating if the pattern is valid
 */
export function isValidRecurrencePattern(pattern: any): boolean {
  if (!pattern) return true; // Allow undefined

  try {
    const parsed = typeof pattern === 'string' ? JSON.parse(pattern) : pattern;

    // Check required fields based on type
    if (!parsed.type) return false;

    switch (parsed.type.toLowerCase()) {
      case 'daily':
        return true;
      case 'weekly':
        return Array.isArray(parsed.days) && parsed.days.length > 0;
      case 'monthly':
        return typeof parsed.day_of_month === 'number';
      case 'custom':
        return typeof parsed.interval_days === 'number';
      default:
        return false;
    }
  } catch (e) {
    return false;
  }
}

/**
 * Gets the next occurrence date for a recurrence pattern
 * @param pattern - The recurrence pattern
 * @param startDate - The starting date
 * @returns Date of next occurrence
 */
export function getNextOccurrence(pattern: any, startDate: Date = new Date()): Date {
  if (!pattern) return startDate;

  try {
    const parsed = typeof pattern === 'string' ? JSON.parse(pattern) : pattern;

    switch (parsed.type.toLowerCase()) {
      case 'daily':
        return new Date(startDate.setDate(startDate.getDate() + 1));
      case 'weekly':
        // For simplicity, just add 7 days
        return new Date(startDate.setDate(startDate.getDate() + 7));
      case 'monthly':
        // Add a month
        return new Date(startDate.setMonth(startDate.getMonth() + 1));
      case 'custom':
        // Add custom interval days
        return new Date(startDate.setDate(startDate.getDate() + parsed.interval_days));
      default:
        return startDate;
    }
  } catch (e) {
    return startDate;
  }
}

/**
 * Checks if a task is overdue
 * @param task - The task to check
 * @returns boolean indicating if the task is overdue
 */
export function isTaskOverdue(task: Task): boolean {
  if (!task.due_date || task.completed) return false;

  const dueDate = new Date(task.due_date);
  const now = new Date();
  return dueDate < now;
}

/**
 * Calculates days remaining until due date
 * @param task - The task to check
 * @returns number of days remaining (negative if overdue)
 */
export function daysUntilDue(task: Task): number | null {
  if (!task.due_date) return null;

  const dueDate = new Date(task.due_date);
  const now = new Date();
  const diffTime = dueDate.getTime() - now.getTime();
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

/**
 * Sorts tasks by priority
 * @param tasks - Array of tasks to sort
 * @returns Sorted array of tasks
 */
export function sortByPriority(tasks: Task[]): Task[] {
  const priorityOrder: { [key: string]: number } = { high: 3, medium: 2, low: 1 };

  return [...tasks].sort((a, b) => {
    const priorityA = priorityOrder[a.priority?.toLowerCase() || 'medium'] || 2;
    const priorityB = priorityOrder[b.priority?.toLowerCase() || 'medium'] || 2;
    return priorityB - priorityA; // Higher priority first
  });
}

/**
 * Sorts tasks by due date
 * @param tasks - Array of tasks to sort
 * @returns Sorted array of tasks
 */
export function sortByDueDate(tasks: Task[]): Task[] {
  return [...tasks].sort((a, b) => {
    if (!a.due_date && !b.due_date) return 0;
    if (!a.due_date) return 1;
    if (!b.due_date) return -1;

    const dateA = new Date(a.due_date);
    const dateB = new Date(b.due_date);
    return dateA.getTime() - dateB.getTime(); // Earlier dates first
  });
}

/**
 * Filters tasks by priority
 * @param tasks - Array of tasks to filter
 * @param priority - Priority level to filter by
 * @returns Filtered array of tasks
 */
export function filterByPriority(tasks: Task[], priority: string): Task[] {
  return tasks.filter(task => task.priority?.toLowerCase() === priority.toLowerCase());
}

/**
 * Filters tasks by tag
 * @param tasks - Array of tasks to filter
 * @param tagName - Tag name to filter by
 * @returns Filtered array of tasks
 */
export function filterByTag(tasks: Task[], tagName: string): Task[] {
  return tasks.filter(task =>
    task.tags?.some(tag => tag.name.toLowerCase().includes(tagName.toLowerCase()))
  );
}

/**
 * Filters tasks by due date range
 * @param tasks - Array of tasks to filter
 * @param startDate - Start date for range
 * @param endDate - End date for range
 * @returns Filtered array of tasks
 */
export function filterByDueDateRange(tasks: Task[], startDate?: Date, endDate?: Date): Task[] {
  return tasks.filter(task => {
    if (!task.due_date) return false;

    const taskDate = new Date(task.due_date);
    if (startDate && taskDate < startDate) return false;
    if (endDate && taskDate > endDate) return false;

    return true;
  });
}