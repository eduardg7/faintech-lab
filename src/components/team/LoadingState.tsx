import { Loader2 } from 'lucide-react';

 interface LoadingStateProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

 export function LoadingState({ message = 'Loading...', size = 'md', className }: LoadingStateProps) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8'
  };

  return (
    <div className={`flex items-center justify-center p-${size === 'lg' ? '12' : 'md' : '6'} ${className || ''}`}>
      <div className="flex items-center gap-3">
        <Loader2 className={`${sizeClasses[size]} animate-spin text-muted-foreground`} />
        <span className="text-muted-foreground">{message}</span>
      </div>
    </div>
  );
}
