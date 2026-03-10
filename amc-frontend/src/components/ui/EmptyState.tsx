'use client';

interface EmptyStateProps {
  hasFilters?: boolean;
  onClearFilters?: () => void;
}

export default function EmptyState({ 
  hasFilters = false, 
  onClearFilters 
}: EmptyStateProps) {
  return (
    <div 
      className="text-center py-12 px-4"
      role="status"
      aria-live="polite"
    >
      <div className="mb-4">
        <svg 
          className="mx-auto h-12 w-12 text-gray-400" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
          aria-hidden="true"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth={2} 
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
          />
        </svg>
      </div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">
        {hasFilters ? 'No Matching Memories' : 'No Memories Yet'}
      </h3>
      <p className="text-sm text-gray-600 mb-4">
        {hasFilters 
          ? 'Try adjusting your search or filters to find what you\'re looking for.'
          : 'Your agent memories will appear here once they start storing data.'
        }
      </p>
      {hasFilters && onClearFilters && (
        <button
          onClick={onClearFilters}
          className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amc-primary transition-colors"
          aria-label="Clear all filters"
        >
          <svg 
            className="mr-2 h-4 w-4" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
            aria-hidden="true"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M6 18L18 6M6 6l12 12" 
            />
          </svg>
          Clear Filters
        </button>
      )}
    </div>
  );
}
