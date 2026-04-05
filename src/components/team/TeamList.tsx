'use client';

import { useState, useEffect } from 'react';
import { Users, Plus, Search, MoreVertical } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

interface TeamMember {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'member' | 'viewer';
  avatar?: string;
  joinedAt: string;
  lastActiveAt: string;
}


interface TeamListProps {
  onSelectTeam?: (teamId: string) => void;
  className?: string;
}

export function TeamList({ onSelectTeam, className }: TeamListProps) {
  const [teams, setTeams] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchTeams();
  }, []);

  const fetchTeams = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/teams');
      if (!response.ok) throw new Error('Failed to fetch teams');
      const data = await response.json();
      setTeams(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load teams');
    } finally {
      setLoading(false);
    }
  };

  const getRoleBadgeVariant = (role: string) => {
    switch (role) {
      case 'admin':
        return 'default';
      case 'member':
        return 'outline';
      case 'viewer':
        return 'outline';
      default:
        return 'outline';
    }
  };

  const filteredTeams = teams.filter(team =>
    team.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    team.email.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className={`flex items-center justify-center p-8 ${className || ''}`}>
        <div className="animate-pulse flex items-center gap-2">
          <Users className="h-4 w-4 text-muted-foreground" />
          <span className="text-muted-foreground">Loading team members...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`p-4 ${className || ''}`}>
        <Card className="border-destructive-200 bg-destructive-50">
          <CardHeader>
            <CardTitle className="text-destructive-600">Error Loading Team</CardTitle>
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
      {/* Search Bar */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search team members..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-input bg-background"
          aria-label="Search team members"
        />
      </div>

      {/* Team Count */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">
          Team Members ({filteredTeams.length})
        </h3>
        <Button
          variant="outline"
          size="sm"
          className="gap-2"
          aria-label="Add new team member"
        >
          <Plus className="h-4 w-4" />
          Add Member
        </Button>
      </div>

      {/* Team List */}
      <div className="space-y-2">
        {filteredTeams.length === 0 ? (
          <div className="text-center py-8">
            <Users className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <p className="text-muted-foreground">
              {searchQuery ? 'No team members found matching your search.' : 'No team members found.'}
            </p>
          </div>
        ) : (
          filteredTeams.map((team) => (
            <Card
              key={team.id}
              className="cursor-pointer hover:border-primary-300 transition-all"
              onClick={() => onSelectTeam?.(team.id)}
            >
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {team.avatar ? (
                      <img
                        src={team.avatar}
                        alt={team.name}
                        className="h-10 w-10 rounded-full"
                      />
                    ) : (
                      <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                        <Users className="h-5 w-5 text-primary-foreground" />
                      </div>
                    )}
                    <div className="flex-1">
                      <div className="font-medium">{team.name}</div>
                      <CardDescription className="text-sm">{team.email}</CardDescription>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Badge variant={getRoleBadgeVariant(team.role)}>
                      {team.role.charAt(0).toUpperCase() + team.role.slice(1)}
                    </Badge>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-8 w-8 p-0"
                      aria-label={`More options for ${team.name}`}
                    >
                      <MoreVertical className="h-4 w-4 text-muted-foreground" />
                    </Button>
                  </div>
                </div>

                {/* Additional Info */}
                <div className="mt-3 flex items-center gap-4 text-xs text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <span>Joined:</span>
                    <span>{formatDate(team.joinedAt)}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <span>Last active:</span>
                    <span>{formatDate(team.lastActiveAt)}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
