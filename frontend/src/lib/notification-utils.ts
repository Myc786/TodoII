/**
 * Utility functions for handling browser notifications and alerts.
 */

/**
 * Check if browser notifications are supported
 */
export const isNotificationSupported = (): boolean => {
  return 'Notification' in window;
};

/**
 * Request permission for browser notifications
 */
export const requestNotificationPermission = (): Promise<NotificationPermission> => {
  if (!isNotificationSupported()) {
    return Promise.reject(new Error('Notifications not supported'));
  }

  return Notification.requestPermission();
};

/**
 * Show a browser notification
 */
export const showNotification = (title: string, options?: NotificationOptions): void => {
  if (!isNotificationSupported()) {
    console.warn('Notifications not supported');
    return;
  }

  if (Notification.permission === 'granted') {
    new Notification(title, options);
  } else {
    console.warn('Notification permission not granted');
  }
};

/**
 * Show a toast notification (using the system's toast component)
 */
export const showToast = (message: string, type: 'success' | 'error' | 'info' | 'warning' = 'info'): void => {
  // This would typically use the project's toast notification system
  // For now, we'll use console logging and a simple alert as fallback
  console.log(`[${type.toUpperCase()}] ${message}`);

  // In a real implementation, this would call the toast service:
  // toast({ title: type.charAt(0).toUpperCase() + type.slice(1), description: message, variant: type });
};

/**
 * Schedule a reminder notification
 */
export const scheduleReminder = (taskTitle: string, reminderTime: Date, reminderType: 'email' | 'browser_notification' | 'both' = 'browser_notification'): void => {
  const now = new Date();
  const timeDiff = reminderTime.getTime() - now.getTime(); // Difference in milliseconds

  if (timeDiff <= 0) {
    // Time has already passed, show notification immediately
    showNotification(`Reminder: ${taskTitle}`, {
      body: `It's time to work on: ${taskTitle}`,
      icon: '/favicon.ico',
      tag: `task-reminder-${Date.now()}`
    });
    return;
  }

  // Schedule the notification for the future
  setTimeout(() => {
    if (reminderType === 'browser_notification' || reminderType === 'both') {
      showNotification(`Reminder: ${taskTitle}`, {
        body: `It's time to work on: ${taskTitle}`,
        icon: '/favicon.ico',
        tag: `task-reminder-${Date.now()}`
      });
    }

    // In a real implementation, you would also send an email if reminderType includes 'email'
    // This would involve calling an API endpoint to send the email
  }, timeDiff);
};

/**
 * Format a date for display in the UI
 */
export const formatDateTimeForDisplay = (date: Date | string): string => {
  if (typeof date === 'string') {
    date = new Date(date);
  }

  return date.toLocaleString([], {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

/**
 * Check if a reminder time is in the past
 */
export const isReminderOverdue = (reminderTime: Date | string): boolean => {
  const now = new Date();
  const reminderDate = typeof reminderTime === 'string' ? new Date(reminderTime) : reminderTime;

  return reminderDate < now;
};