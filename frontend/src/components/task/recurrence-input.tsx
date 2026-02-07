'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { RecurrencePattern } from '@/lib/types';

interface RecurrenceInputProps {
  value?: RecurrencePattern;
  onChange: (pattern: RecurrencePattern | undefined) => void;
  disabled?: boolean;
}

export function RecurrenceInput({ value, onChange, disabled }: RecurrenceInputProps) {
  const [isOpen, setIsOpen] = useState(!!value);

  // Initialize with default values if opening for the first time
  const [type, setType] = useState<string>(value?.type || 'daily');
  const [interval, setInterval] = useState<number>(value?.interval || 1);
  const [daysOfWeek, setDaysOfWeek] = useState<boolean[]>(
    value?.days_of_week ? [0, 1, 2, 3, 4, 5, 6].map(day => value.days_of_week!.includes(day)) : [false, false, false, false, false, false, false]
  );
  const [dayOfMonth, setDayOfMonth] = useState<number>(value?.day_of_month || 1);
  const [endDate, setEndDate] = useState<string>(value?.end_date || '');
  const [occurrences, setOccurrences] = useState<number>(value?.occurrences || 0);

  // Update local state when value prop changes
  useState(() => {
    if (value) {
      setType(value.type || 'daily');
      setInterval(value.interval || 1);
      setDaysOfWeek(
        value.days_of_week ? [0, 1, 2, 3, 4, 5, 6].map(day => value.days_of_week!.includes(day)) : [false, false, false, false, false, false, false]
      );
      setDayOfMonth(value.day_of_month || 1);
      setEndDate(value.end_date || '');
      setOccurrences(value.occurrences || 0);
    }
  });

  const handleTypeChange = (newType: string) => {
    setType(newType);
    updatePattern(newType, interval, daysOfWeek, dayOfMonth, endDate, occurrences);
  };

  const handleIntervalChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = parseInt(e.target.value) || 1;
    setInterval(newValue);
    updatePattern(type, newValue, daysOfWeek, dayOfMonth, endDate, occurrences);
  };

  const handleDayOfWeekToggle = (dayIndex: number) => {
    const newDaysOfWeek = [...daysOfWeek];
    newDaysOfWeek[dayIndex] = !newDaysOfWeek[dayIndex];
    setDaysOfWeek(newDaysOfWeek);

    // Convert boolean array to number array for the pattern
    const selectedDays = newDaysOfWeek.reduce<number[]>((acc, isSelected, idx) => {
      if (isSelected) acc.push(idx);
      return acc;
    }, []);

    updatePattern(type, interval, selectedDays, dayOfMonth, endDate, occurrences);
  };

  const handleDayOfMonthChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = Math.max(1, Math.min(31, parseInt(e.target.value) || 1));
    setDayOfMonth(newValue);
    updatePattern(type, interval, daysOfWeek, newValue, endDate, occurrences);
  };

  const handleEndDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEndDate(e.target.value);
    updatePattern(type, interval, daysOfWeek, dayOfMonth, e.target.value, occurrences);
  };

  const handleOccurrencesChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = Math.max(0, parseInt(e.target.value) || 0);
    setOccurrences(newValue);
    updatePattern(type, interval, daysOfWeek, dayOfMonth, endDate, newValue);
  };

  const updatePattern = (
    newType: string,
    newInterval: number,
    newDaysOfWeek: number | boolean[] | number[],
    newDayOfMonth: number,
    newEndDate: string,
    newOccurrences: number
  ) => {
    const pattern: RecurrencePattern = {
      type: newType as 'daily' | 'weekly' | 'monthly' | 'custom',
      interval: newInterval,
    };

    if (newType === 'weekly') {
      // Handle both boolean array and number array
      let selectedDays: number[] = [];
      if (Array.isArray(newDaysOfWeek)) {
        // If it's a boolean array (indicating which days are selected), convert to number array
        if (typeof newDaysOfWeek[0] === 'boolean') {
          selectedDays = (newDaysOfWeek as boolean[]).reduce<number[]>((acc, isSelected, idx) => {
            if (isSelected) acc.push(idx);
            return acc;
          }, []);
        } else {
          // If it's already a number array, use it directly
          selectedDays = newDaysOfWeek as number[];
        }
      }
      pattern.days_of_week = selectedDays;
    }

    if (newType === 'monthly') {
      pattern.day_of_month = newDayOfMonth;
    }

    if (newEndDate) {
      pattern.end_date = newEndDate;
    }

    if (newOccurrences > 0) {
      pattern.occurrences = newOccurrences;
    }

    onChange(pattern);
  };

  const toggleRecurrence = () => {
    if (isOpen) {
      // Turn off recurrence
      setIsOpen(false);
      onChange(undefined);
    } else {
      // Turn on recurrence with default settings
      setIsOpen(true);
      const defaultPattern: RecurrencePattern = {
        type: 'daily',
        interval: 1,
      };
      onChange(defaultPattern);
    }
  };

  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <Checkbox
          id="enable-recurrence"
          checked={isOpen}
          onCheckedChange={toggleRecurrence}
          disabled={disabled}
        />
        <Label htmlFor="enable-recurrence" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-glow">
          Recurring Task
        </Label>
      </div>

      {isOpen && (
        <Card className="border bg-accent/20">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-glow">Recurrence Settings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-4 items-center gap-2">
              <Label className="text-sm text-glow">Every</Label>
              <Input
                type="number"
                min="1"
                value={interval}
                onChange={handleIntervalChange}
                disabled={disabled}
                className="col-span-1"
              />
              <Select value={type} onValueChange={handleTypeChange} disabled={disabled}>
                <SelectTrigger className="col-span-2">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="daily">day(s)</SelectItem>
                  <SelectItem value="weekly">week(s)</SelectItem>
                  <SelectItem value="monthly">month(s)</SelectItem>
                  <SelectItem value="custom">custom</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {type === 'weekly' && (
              <div className="space-y-2">
                <Label className="text-sm text-glow">Repeat on:</Label>
                <div className="flex flex-wrap gap-2">
                  {dayNames.map((day, index) => (
                    <div key={index} className="flex items-center gap-1">
                      <Checkbox
                        id={`day-${index}`}
                        checked={daysOfWeek[index]}
                        onCheckedChange={() => handleDayOfWeekToggle(index)}
                        disabled={disabled}
                      />
                      <Label htmlFor={`day-${index}`} className="text-sm text-glow">
                        {day}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {type === 'monthly' && (
              <div className="space-y-2">
                <Label className="text-sm text-glow">Day of month:</Label>
                <Input
                  type="number"
                  min="1"
                  max="31"
                  value={dayOfMonth}
                  onChange={handleDayOfMonthChange}
                  disabled={disabled}
                />
              </div>
            )}

            <div className="space-y-2">
              <Label className="text-sm text-glow">Ends:</Label>
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-2">
                  <Input
                    type="date"
                    value={endDate}
                    onChange={handleEndDateChange}
                    disabled={disabled}
                    placeholder="No end date"
                  />
                  <span className="text-sm text-muted-foreground">or</span>
                </div>
                <div className="flex items-center gap-2">
                  <Input
                    type="number"
                    min="0"
                    value={occurrences}
                    onChange={handleOccurrencesChange}
                    disabled={disabled}
                    placeholder="0 occurrences"
                    className="max-w-[120px]"
                  />
                  <span className="text-sm text-muted-foreground">occurrences</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}