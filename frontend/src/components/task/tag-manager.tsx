'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Plus, X } from 'lucide-react';
import { Tag } from '@/lib/types';

interface TagManagerProps {
  tags: Tag[];
  onTagCreate: (name: string, color?: string) => void;
  onTagDelete: (id: string) => void;
  onTagUpdate: (id: string, name: string, color?: string) => void;
  className?: string;
}

export function TagManager({ tags, onTagCreate, onTagDelete, onTagUpdate, className }: TagManagerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [newTagName, setNewTagName] = useState('');
  const [newTagColor, setNewTagColor] = useState('#3B82F6'); // Default blue
  const [editingTag, setEditingTag] = useState<Tag | null>(null);
  const [editTagName, setEditTagName] = useState('');
  const [editTagColor, setEditTagColor] = useState('');

  const handleCreateTag = () => {
    if (newTagName.trim()) {
      onTagCreate(newTagName.trim(), newTagColor);
      setNewTagName('');
      setNewTagColor('#3B82F6');
    }
  };

  const handleUpdateTag = () => {
    if (editingTag && editTagName.trim()) {
      onTagUpdate(editingTag.id, editTagName.trim(), editTagColor);
      setEditingTag(null);
      setEditTagName('');
      setEditTagColor('');
    }
  };

  const startEditing = (tag: Tag) => {
    setEditingTag(tag);
    setEditTagName(tag.name);
    setEditTagColor(tag.color || '#3B82F6');
  };

  const cancelEditing = () => {
    setEditingTag(null);
    setEditTagName('');
    setEditTagColor('');
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm" className={className}>
          <Plus className="h-4 w-4 mr-2" />
          Manage Tags
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Manage Tags</DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          {/* Create new tag */}
          <div className="space-y-2">
            <Label htmlFor="new-tag-name">Create New Tag</Label>
            <div className="flex space-x-2">
              <Input
                id="new-tag-name"
                value={newTagName}
                onChange={(e) => setNewTagName(e.target.value)}
                placeholder="Tag name"
                className="flex-1"
              />
              <Input
                type="color"
                value={newTagColor}
                onChange={(e) => setNewTagColor(e.target.value)}
                className="w-12 h-10 p-1"
              />
              <Button onClick={handleCreateTag} size="sm">
                Add
              </Button>
            </div>
          </div>

          {/* Existing tags */}
          <div className="space-y-2">
            <Label>Existing Tags</Label>
            <div className="space-y-2 max-h-60 overflow-y-auto">
              {tags.length === 0 ? (
                <p className="text-sm text-muted-foreground">No tags created yet.</p>
              ) : (
                tags.map((tag) => (
                  <div key={tag.id} className="flex items-center justify-between p-2 border rounded">
                    {editingTag?.id === tag.id ? (
                      <div className="flex-1 flex space-x-2">
                        <Input
                          value={editTagName}
                          onChange={(e) => setEditTagName(e.target.value)}
                          className="text-sm"
                        />
                        <Input
                          type="color"
                          value={editTagColor}
                          onChange={(e) => setEditTagColor(e.target.value)}
                          className="w-8 h-8 p-0.5"
                        />
                      </div>
                    ) : (
                      <div className="flex items-center space-x-2">
                        <Badge variant="secondary" style={{ backgroundColor: `${tag.color}20`, color: tag.color }}>
                          {tag.name}
                        </Badge>
                        <span className="text-xs text-muted-foreground">{tag.color}</span>
                      </div>
                    )}
                    <div className="flex space-x-1">
                      {editingTag?.id === tag.id ? (
                        <>
                          <Button onClick={handleUpdateTag} size="sm" variant="outline" className="h-8 w-8 p-0">
                            ✓
                          </Button>
                          <Button onClick={cancelEditing} size="sm" variant="outline" className="h-8 w-8 p-0">
                            ✕
                          </Button>
                        </>
                      ) : (
                        <>
                          <Button onClick={() => startEditing(tag)} size="sm" variant="outline" className="h-8 w-8 p-0">
                            ✏️
                          </Button>
                          <Button onClick={() => onTagDelete(tag.id)} size="sm" variant="outline" className="h-8 w-8 p-0">
                            <X className="h-3 w-3" />
                          </Button>
                        </>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}