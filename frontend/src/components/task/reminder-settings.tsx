'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Task } from '@/lib/types';

interface ReminderSettingsProps {
  task: Task;
  onReminderSet: (taskId: string, reminderTime: Date, reminderType: 'email' | 'browser_notification' | 'both') => void;
  disabled?: boolean;
}

export function ReminderSettings({ task, onReminderSet, disabled }: ReminderSettingsProps) {
  const [reminderEnabled, setReminderEnabled] = useState(false);
  const [reminderTime, setReminderTime] = useState<string>('');
  const [reminderType, setReminderType] = useState<'email' | 'browser_notification' | 'both'>('browser_notification');
  const [reminderOffset, setReminderOffset] = useState<number>(0); // Minutes before due date

  const handleEnableChange = () => {
    if (!reminderEnabled) {
      // Enable reminder - default to 15 minutes before due date if available
      if (task.due_date) {
        const dueDateTime = new Date(task.due_date);
        const reminderDateTime = new Date(dueDateTime.getTime() - 15 * 60000); // 15 minutes before
        setReminderTime(reminderDateTime.toISOString().slice(0, 16)); // Format as YYYY-MM-DDTHH:mm
      } else {
        // If no due date, set to tomorrow at 9 AM
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        tomorrow.setHours(9, 0, 0, 0);
        setReminderTime(tomorrow.toISOString().slice(0, 16));
      }
    }
    setReminderEnabled(!reminderEnabled);
  };

  const handleSetReminder = () => {
    if (reminderEnabled && reminderTime) {
      const reminderDateTime = new Date(reminderTime);
      onReminderSet(task.id, reminderDateTime, reminderType);
    }
  };

  const handleOffsetChange = (minutes: number) => {
    if (task.due_date) {
      const dueDateTime = new Date(task.due_date);
      const reminderDateTime = new Date(dueDateTime.getTime() - minutes * 60000); // Convert minutes to milliseconds
      setReminderTime(reminderDateTime.toISOString().slice(0, 16));
      setReminderOffset(minutes);
    }
  };

  return (
    <Card className="border bg-accent/20">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm text-glow">Reminder Settings</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-2">
          <Checkbox
            id="enable-reminder"
            checked={reminderEnabled}
            onCheckedChange={handleEnableChange}
            disabled={disabled}
          />
          <Label htmlFor="enable-reminder" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-glow">
            Set Reminder
          </Label>
        </div>

        {reminderEnabled && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="reminder-time" className="text-sm text-glow">
                  Reminder Time
                </Label>
                <Input
                  id="reminder-time"
                  type="datetime-local"
                  value={reminderTime}
                  onChange={(e) => setReminderTime(e.target.value)}
                  disabled={disabled}
                />
              </div>

              <div className="space-y-2">
                <Label className="text-sm text-glow">
                  Notification Type
                </Label>
                <Select value={reminderType} onValueChange={(value: 'email' | 'browser_notification' | 'both') => setReminderType(value)} disabled={disabled}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="browser_notification">Browser Notification</SelectItem>
                    <SelectItem value="email">Email</SelectItem>
                    <SelectItem value="both">Both</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {task.due_date && (
              <div className="space-y-2">
                <Label className="text-sm text-glow">
                  Or set relative to due date:
                </Label>
                <div className="flex flex-wrap gap-2">
                  <Button
                    type="button"
                    variant={reminderOffset === 0 ? "default" : "outline"}
                    size="sm"
                    onClick={() => handleOffsetChange(0)}
                    disabled={disabled}
                  >
                    At due time
                  </Button>
                  <Button
                    type="button"
                    variant={reminderOffset === 15 ? "default" : "outline"}
                    size="sm"
                    onClick={() => handleOffsetChange(15)}
                    disabled={disabled}
                  >
                    15 min before
                  </Button>
                  <Button
                    type="button"
                    variant={reminderOffset === 30 ? "default" : "outline"}
                    size="sm"
                    onClick={() => handleOffsetChange(30)}
                    disabled={disabled}
                  >
                    30 min before
                  </Button>
                  <Button
                    type="button"
                    variant={reminderOffset === 60 ? "default" : "outline"}
                    size="sm"
                    onClick={() => handleOffsetChange(60)}
                    disabled={disabled}
                  >
                    1 hour before
                  </Button>
                  <Button
                    type="button"
                    variant={reminderOffset === 1440 ? "default" : "outline"}
                    size="sm"
                    onClick={() => handleOffsetChange(1440)} // 24 hours = 1440 minutes
                    disabled={disabled}
                  >
                    1 day before
                  </Button>
                </div>
              </div>
            )}

            <Button
              type="button"
              onClick={handleSetReminder}
              disabled={disabled || !reminderTime}
              className="w-full"
            >
              Set Reminder
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}