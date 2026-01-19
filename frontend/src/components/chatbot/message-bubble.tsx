import { cn } from '@/lib/utils';
import { format } from 'date-fns';

interface MessageBubbleProps {
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

export function MessageBubble({ content, sender, timestamp }: MessageBubbleProps) {
  return (
    <div className={cn(
      "flex flex-col",
      sender === 'user' ? 'items-end' : 'items-start'
    )}>
      <div
        className={cn(
          "max-w-[85%] rounded-2xl px-4 py-2 text-sm",
          sender === 'user'
            ? 'bg-primary text-primary-foreground rounded-br-sm'
            : 'bg-secondary text-secondary-foreground rounded-bl-sm'
        )}
      >
        {content}
      </div>
      <div className={cn(
        "text-xs text-muted-foreground mt-1",
        sender === 'user' ? 'text-right' : 'text-left'
      )}>
        {format(timestamp, 'HH:mm')}
      </div>
    </div>
  );
}