'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Plus } from 'lucide-react';
import { Tag } from '@/lib/types';

interface TagCreatorProps {
  onTagCreate: (name: string, color?: string) => void;
  className?: string;
}

export function TagCreator({ onTagCreate, className }: TagCreatorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [tagName, setTagName] = useState('');
  const [tagColor, setTagColor] = useState('#3B82F6'); // Default blue

  const handleCreateTag = () => {
    if (tagName.trim()) {
      onTagCreate(tagName.trim(), tagColor);
      setTagName('');
      setTagColor('#3B82F6');
      setIsOpen(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm" className={className}>
          <Plus className="h-4 w-4 mr-2" />
          New Tag
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-sm">
        <DialogHeader>
          <DialogTitle>Create New Tag</DialogTitle>
        </DialogHeader>

        <div className="space-y-4 py-2">
          <div className="space-y-2">
            <Label htmlFor="tag-name">Tag Name</Label>
            <Input
              id="tag-name"
              value={tagName}
              onChange={(e) => setTagName(e.target.value)}
              placeholder="Enter tag name"
              autoFocus
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="tag-color">Tag Color</Label>
            <div className="flex items-center space-x-2">
              <Input
                type="color"
                id="tag-color"
                value={tagColor}
                onChange={(e) => setTagColor(e.target.value)}
                className="w-12 h-10 p-1"
              />
              <Input
                type="text"
                value={tagColor}
                onChange={(e) => setTagColor(e.target.value)}
                className="flex-1 font-mono text-sm"
                placeholder="#RRGGBB"
              />
            </div>
          </div>

          <Button onClick={handleCreateTag} className="w-full">
            Create Tag
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}