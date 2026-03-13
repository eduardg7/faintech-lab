'use client';

import { cn } from '@/lib/utils';

interface SkeletonProps {
  className?: string;
  animate?: boolean;
}

/**
 * Base Skeleton component with pulse animation
 */
export function Skeleton({ className, animate = true }: SkeletonProps) {
  return (
    <div
      className={cn(
        'rounded-md bg-gray-200',
        animate && 'animate-pulse',
        className
      )}
      aria-hidden="true"
    />
  );
}

/**
 * Skeleton for memory card in list view
 */
export function MemoryCardSkeleton() {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 space-y-3" aria-hidden="true">
      {/* Header: Type badge + Agent + Timestamp */}
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2">
          <Skeleton className="h-5 w-16 rounded" /> {/* Type badge */}
          <Skeleton className="h-4 w-20" /> {/* Agent ID */}
        </div>
        <Skeleton className="h-4 w-32" /> {/* Timestamp */}
      </div>

      {/* Content */}
      <div className="space-y-2">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-3/4" />
        <Skeleton className="h-4 w-1/2" />
      </div>

      {/* Tags */}
      <div className="flex gap-2">
        <Skeleton className="h-6 w-14 rounded" />
        <Skeleton className="h-6 w-16 rounded" />
        <Skeleton className="h-6 w-12 rounded" />
      </div>
    </div>
  );
}

/**
 * Skeleton for dashboard stats card
 */
export function DashboardStatSkeleton() {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6" aria-hidden="true">
      <Skeleton className="h-4 w-24 mb-2" /> {/* Label */}
      <Skeleton className="h-8 w-16 mb-1" /> {/* Value */}
      <Skeleton className="h-3 w-20" /> {/* Subtitle */}
    </div>
  );
}

/**
 * Skeleton for full dashboard stats row
 */
export function DashboardStatsSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {Array.from({ length: 4 }).map((_, i) => (
        <DashboardStatSkeleton key={i} />
      ))}
    </div>
  );
}

/**
 * Skeleton for memory list
 */
export function MemoryListSkeleton({ count = 5 }: { count?: number }) {
  return (
    <div className="space-y-4" aria-label="Loading memories..." role="status">
      {Array.from({ length: count }).map((_, i) => (
        <MemoryCardSkeleton key={i} />
      ))}
      <span className="sr-only">Loading...</span>
    </div>
  );
}

/**
 * Skeleton for search bar
 */
export function SearchBarSkeleton() {
  return (
    <div className="flex gap-2 mb-6" aria-hidden="true">
      <Skeleton className="h-10 flex-1 rounded-lg" />
      <Skeleton className="h-10 w-24 rounded-lg" />
    </div>
  );
}

/**
 * Skeleton for filters row
 */
export function FiltersSkeleton() {
  return (
    <div className="flex flex-wrap gap-2 mb-6" aria-hidden="true">
      <Skeleton className="h-10 w-32 rounded-lg" />
      <Skeleton className="h-10 w-40 rounded-lg" />
      <Skeleton className="h-10 w-28 rounded-lg" />
    </div>
  );
}

/**
 * Full page skeleton for memory dashboard
 */
export function MemoryDashboardSkeleton() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-10 w-20 rounded" />
      </div>

      {/* Search */}
      <SearchBarSkeleton />

      {/* Filters */}
      <FiltersSkeleton />

      {/* Memory List */}
      <MemoryListSkeleton count={5} />
    </div>
  );
}

/**
 * Skeleton for agent dashboard page
 */
export function AgentDashboardSkeleton() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-6">
        <Skeleton className="h-8 w-64 mb-2" />
        <Skeleton className="h-4 w-48" />
      </div>

      {/* Stats Grid */}
      <DashboardStatsSkeleton />

      {/* Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-4">
          <Skeleton className="h-6 w-32 mb-4" />
          <MemoryListSkeleton count={3} />
        </div>
        <div className="space-y-4">
          <Skeleton className="h-6 w-32 mb-4" />
          <MemoryListSkeleton count={3} />
        </div>
      </div>
    </div>
  );
}
