'use client';

import { useState } from 'react';
import { Settings, Save, AlertTriangle, Info } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
} from '@/components/ui/select';

interface TeamSettingsData {
  name: string;
  description?: string;
  isPublic: boolean;
  allowInvites: boolean;
  maxMembers: number;
}

 interface TeamSettingsProps {
  teamId: string;
  className?: string;
  onUpdate?: (settings: TeamSettingsData) => void;
}

 export function TeamSettings({ teamId, className, onUpdate }: TeamSettingsProps) {
  const [settings, setSettings] = useState<TeamSettingsData>({
    name: '',
    description: '',
    isPublic: false,
    allowInvites: true,
    maxMembers: 10
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, [teamId]);

  const fetchSettings = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/teams/${teamId}/settings`);
      if (!response.ok) throw new Error('Failed to fetch team settings');
      const data = await response.json();
      setSettings(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load team settings');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      setError(null);

      const response = await fetch(`/api/teams/${teamId}/settings`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings)
      });

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.message || 'Failed to update team settings');
        return;
      }

      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
      onUpdate?.(settings);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update team settings');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className={`flex items-center justify-center p-8 ${className || ''}`}>
        <div className="animate-pulse flex items-center gap-2">
          <Settings className="h-4 w-4 text-muted-foreground" />
          <span className="text-muted-foreground">Loading team settings...</span>
        </div>
      </div>
    );
  }

  return (
    <div className={`space-y-4 ${className || ''}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Team Settings</h3>
        <Button
          variant="default"
          size="sm"
          onClick={handleSave}
          disabled={saving}
          aria-busy={saving}
        >
          {saving ? (
            <>
              <Save className="h-4 w-4 animate-spin" />
              <span>Saving...</span>
            </>
          ) : (
            <>
            <Save className="h-4 w-4" />
            <span>Save</span>
          </>
        </Button>
      </div>

      {/* Success Message */}
      {success && (
        <div className="p-3 rounded-md bg-green-50 border border-green-200">
          <div className="flex items-center gap-2 text-green-700">
            <Info className="h-4 w-4" />
            <span>Settings updated successfully!</span>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="p-3 rounded-md bg-destructive-50 border border-destructive-200">
          <div className="flex items-center gap-2 text-destructive-700">
            <AlertTriangle className="h-4 w-4" />
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* Settings Form */}
      <div className="space-y-4">
        {/* Team Name */}
        <div className="space-y-2">
          <Label htmlFor="name">Team Name</Label>
          <Input
            id="name"
            value={settings.name}
            onChange={(e) => setSettings({ ...settings, name: e.target.value })}
            placeholder="Enter team name"
            required
            aria-label="Team name"
          />
        </div>

        {/* Team Description */}
        <div className="space-y-2">
          <Label htmlFor="description">Description</Label>
          <Input
            id="description"
            value={settings.description}
            onChange={(e) => setSettings({ ...settings, description: e.target.value })}
            placeholder="Enter team description"
            aria-label="Team description"
          />
        </div>

        {/* Public Team Toggle */}
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <Label htmlFor="isPublic">Public Team</Label>
          </div>
          <Badge variant={settings.isPublic ? 'default' : 'outline'}>
            {settings.isPublic ? 'Public' : 'Private'}
          </Badge>
        </div>
        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            id="isPublic"
            checked={settings.isPublic}
            onChange={(e) => setSettings({ ...settings, isPublic: e.target.checked })}
            aria-label="Toggle public team"
          />
        </div>

        {/* Allow Invites Toggle */}
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <Label htmlFor="allowInvites">Allow Invites</Label>
          </div>
          <Badge variant={settings.allowInvites ? 'default' : 'outline'}>
            {settings.allowInvites ? 'Enabled' : 'Disabled'}
          </Badge>
        </div>
        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            id="allowInvites"
            checked={settings.allowInvites}
            onChange={(e) => setSettings({ ...settings, allowInvites: e.target.checked })}
            aria-label="Toggle allow invites"
          />
        </div>

        {/* Max Members */}
        <div className="space-y-2">
          <Label htmlFor="maxMembers">Maximum Members</Label>
          <Input
            type="number"
            id="maxMembers"
            value={settings.maxMembers}
            onChange={(e) => setSettings({ ...settings, maxMembers: parseInt(e.target.value) })}
            placeholder="Enter maximum members"
            min={1}
            max={50}
            required
            aria-label="Maximum members"
          />
          <CardDescription>
            The maximum number of team members allowed
          </CardDescription>
        </div>
      </div>
    </div>
  );
}
