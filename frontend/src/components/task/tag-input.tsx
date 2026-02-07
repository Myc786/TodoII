'use client';

import { useState, useRef, KeyboardEvent } from 'react';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Tag } from '@/lib/types';

interface TagInputProps {
  selectedTags: Tag[];
  availableTags: Tag[];
  onTagSelect: (tag: Tag) => void;
  onTagRemove: (tagId: string) => void;
  onTagCreate?: (tagName: string) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
}

export function TagInput({
  selectedTags,
  availableTags,
  onTagSelect,
  onTagRemove,
  onTagCreate,
  placeholder = "Select or create tags...",
  disabled = false,
  className
}: TagInputProps) {
  const [inputValue, setInputValue] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [focusedIndex, setFocusedIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);

  // Filter available tags based on input
  const filteredTags = availableTags.filter(tag =>
    tag.name.toLowerCase().includes(inputValue.toLowerCase()) &&
    !selectedTags.some(selected => selected.id === tag.id)
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
    setShowSuggestions(true);
    setFocusedIndex(-1);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && inputValue === '' && selectedTags.length > 0) {
      // Remove last tag when backspace is pressed on empty input
      const lastTag = selectedTags[selectedTags.length - 1];
      onTagRemove(lastTag.id);
    } else if (e.key === 'Enter' && inputValue.trim() !== '') {
      e.preventDefault();
      // If we have a focused suggestion, select it
      if (focusedIndex >= 0 && filteredTags[focusedIndex]) {
        onTagSelect(filteredTags[focusedIndex]);
      } else {
        // Otherwise, create a new tag if onTagCreate is provided
        if (onTagCreate) {
          onTagCreate(inputValue.trim());
        } else {
          // Just add as a temporary tag object
          onTagSelect({
            id: `temp_${Date.now()}`,
            name: inputValue.trim(),
            user_id: 'temp',
            created_at: new Date().toISOString()
          });
        }
      }
      setInputValue('');
      setShowSuggestions(false);
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setFocusedIndex(prev => Math.min(prev + 1, filteredTags.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setFocusedIndex(prev => Math.max(prev - 1, -1));
    }
  };

  const handleTagClick = (tag: Tag) => {
    onTagSelect(tag);
    setInputValue('');
    setShowSuggestions(false);
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  const handleSuggestionMouseDown = () => {
    // Prevent blur when clicking on a suggestion
    setTimeout(() => {
      if (inputRef.current) {
        inputRef.current.focus();
      }
    }, 0);
  };

  return (
    <div className={cn("relative", className)}>
      <div className="flex flex-wrap gap-2 mb-2">
        {selectedTags.map(tag => (
          <Badge
            key={tag.id}
            variant="secondary"
            className="flex items-center gap-1"
          >
            {tag.name}
            {!disabled && (
              <button
                type="button"
                onClick={() => onTagRemove(tag.id)}
                className="ml-1 rounded-full hover:bg-secondary-foreground/20"
                aria-label={`Remove ${tag.name} tag`}
              >
                <X className="h-3 w-3" />
              </button>
            )}
          </Badge>
        ))}
      </div>

      <Input
        ref={inputRef}
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        onFocus={() => inputValue && setShowSuggestions(true)}
        onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
        placeholder={placeholder}
        disabled={disabled}
        className="w-full"
      />

      {showSuggestions && filteredTags.length > 0 && (
        <div className="absolute z-10 w-full mt-1 bg-background border border-input rounded-md shadow-lg max-h-60 overflow-auto">
          <div className="p-1">
            {filteredTags.map((tag, index) => (
              <div
                key={tag.id}
                onMouseDown={handleSuggestionMouseDown}
                onClick={() => handleTagClick(tag)}
                className={cn(
                  "px-3 py-2 text-sm cursor-pointer rounded-sm hover:bg-accent",
                  index === focusedIndex && "bg-accent"
                )}
              >
                <Badge variant="secondary">{tag.name}</Badge>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}