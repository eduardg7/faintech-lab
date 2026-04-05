'use client';

import { useState } from 'react';
import { MoreHorizontal, Trash2, UserPlus, Edit, Shield, Key, Settings } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface TeamAction {
  id: string;
  type: 'add' | 'remove' | 'update' | 'view';
  label: string;
  description: string;
  timestamp: string;
}

 interface TeamActionsProps {
  teamId: string;
  className?: string;
  onRefresh?: () => void;
}

 export function TeamActions({ teamId, className, onRefresh }: TeamActionsProps) {
  const [actions, setActions] = useState<TeamAction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchActions();
  }, [teamId]);

  const fetchActions = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/teams/${teamId}/actions`);
      if (!response.ok) throw new Error('Failed to fetch team actions');
      const data = await response.json();
      setActions(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load team actions');
    } finally {
      setLoading(false);
    }
  };

  const getActionIcon = (type: string) => {
    switch (type) {
      case 'add':
        return <UserPlus className="h-4 w-4" />;
      case 'remove':
        return <Trash2 className="h-4 w-4" />;
      case 'update':
        return <Edit className="h-4 w-4" />;
      case 'view':
        return <Shield className="h-4 w-4" />;
      default:
        return <Settings className="h-4 w-4" />;
    }
  };

  const getActionColor = (type: string) => {
    switch (type) {
      case 'add':
        return 'text-green-600 bg-green-50';
      case 'remove':
        return 'text-red-600 bg-red-50';
      case 'update':
        return 'text-blue-600 bg-blue-50';
      case 'view':
        return 'text-gray-600 bg-gray-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const seconds = Math.floor(diff / 1000);

    if (seconds < 60) return `${seconds}s ago`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    const days = Math.floor(seconds / 86400);
    return `${days}d ago`;
  };

  if (loading) {
    return (
      <div className={`flex items-center justify-center p-8 ${className || ''}`}>
        <div className="animate-pulse flex items-center gap-2">
          <Settings className="h-4 w-4 text-muted-foreground" />
          <span className="text-muted-foreground">Loading team actions...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`p-4 ${className || ''}`}>
        <Card className="border-destructive-200 bg-destructive-50">
          <CardHeader>
            <CardTitle className="text-destructive-600">Error Loading Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">{error}</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className={`space-y-4 ${className || ''}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Recent Actions</h3>
        <Button
          variant="outline"
          size="sm"
          onClick={onRefresh}
          aria-label="Refresh actions"
        >
          <MoreHorizontal className="h-4 w-4" />
        </Button>
      </div>

      {/* Actions List */}
      <div className="space-y-2">
        {actions.length === 0 ? (
          <div className="text-center py-8">
            <Settings className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <p className="text-muted-foreground">No recent actions</p>
          </div>
        ) : (
          actions.map((action) => (
            <Card key={action.id} className="border-l">
              <CardContent className="p-4">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-center gap-3">
                    {getActionIcon(action.type)}
                    <div className="flex-1">
                      <div className="font-medium">{action.label}</div>
                      <p className="text-sm text-muted-foreground mt-1">
                        {action.description}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Badge className={getActionColor(action.type)}>
                      {action.type}
                    </Badge>
                    <span className="text-xs text-muted-foreground">
                      {formatDate(action.timestamp)}
                    </span>
                  </div>
                </div>
              </Card>
            ))
          )
        )}
      </div>
    </div>
  );
}
