'use client';

import { useState } from 'react';
import { UserPlus, X, Mail, Loader2 } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
} from '@/components/ui/select';

 { Badge } from '@/components/ui/badge';

 interface InviteTeamMemberProps {
  open: boolean;
  onClose: () => void;
  className?: string;
}

 interface TeamMemberFormData {
  email: string;
  role: 'admin' | 'member' | 'viewer';
}

 const availableRoles = [
  { value: 'admin', label: 'Admin' },
  { value: 'member', label: 'Member' },
  { value: 'viewer', label: 'Viewer' },
] as const;

 export function InviteTeamMemberDialog({ open, onClose, className }: InviteTeamMemberProps) {
  const [formData, setFormData] = useState<TeamMemberFormData>({
    email: '',
    role: 'member'
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError(null);
 // Clear error when user types
  };

  const handleRoleChange = (value: string) => {
    setFormData(prev => ({ ...prev, role: value as 'member' }));
    setError(null); // Reset role to member when changing role
  };
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    setSuccess(false);

    if (!formData.email || !formData.role) {
      setError('Please fill in all required fields');
      setIsSubmitting(false);
      return;
    }

    try {
      const response = await fetch('/api/teams/invite', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.message || 'Failed to send invitation');
        return;
      }

      setSuccess(true);
      setFormData({ email: '', role: 'member' });
      // Reset form after success
      setTimeout(() => {
        onClose();
      }, 2000);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className={className}>
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <UserPlus className="h-5 w-5" />
            Invite Team Member
          </DialogTitle>
          <DialogDescription>
            Add a new team member to your workspace
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Email Input */}
          <div className="space-y-2">
            <Label htmlFor="email">Email Address</Label>
            <Input
              id="email"
              type="email"
              placeholder="member@example.com"
              value={formData.email}
              onChange={handleInputChange}
              required
              aria-describedby="Enter member's email address"
              aria-invalid={error?.includes('email') ? 'Invalid email address' : ''}
              className="w-full"
              aria-label="Email address"
            />
            {error && error.includes('email') && (
              <p className="text-sm text-destructive-600 mt-1">
                {error}
              </p>
            ) : null}
          </div>

          {/* Role Select */}
          <div className="space-y-2">
            <Label htmlFor="role">Role</Label>
            <Select
              value={formData.role}
              onValueChange={handleRoleChange}
              aria-label="Select member role"
            >
              <SelectTrigger>Role</SelectTrigger>
              {availableRoles.map((role) => (
                <SelectItem key={role.value} value={role.value}>
                  <div className="flex items-center gap-2">
                    <span>{role.label}</span>
                    {role.value === 'admin' && (
                      <Badge variant="default" className="text-xs">
                        Full access
                      </Badge>
                    )}
                  </div>
                </SelectItem>
              ))}
            </Select>
          </div>
        </div>

        {/* Success Message */}
        {success && (
          <div className="p-3 rounded-md bg-green-50 border border-green-200">
            <div className="flex items-center gap-2 text-green-700">
              <Mail className="h-4 w-4" />
              <span>Invitation sent successfully!</span>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="p-3 rounded-md bg-destructive-50 border border-destructive-200">
            <div className="flex items-center gap-2 text-destructive-700">
              <Mail className="h-4 w-4" />
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <DialogFooter>
          <Button
            variant="outline"
            onClick={onClose}
            disabled={isSubmitting}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            disabled={isSubmitting || !formData.email || !formData.role}
            aria-busy={isSubmitting}
          >
            {isSubmitting ? (
              <>
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Sending invitation...</span>
            </>
          ) : (
            'Send Invitation'
          )}
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
  );
}
