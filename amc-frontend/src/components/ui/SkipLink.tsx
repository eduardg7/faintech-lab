'use client';

interface SkipLinkProps {
  targetId: string;
  label?: string;
}

/**
 * Skip link component for accessibility - WCAG 2.4.1 Bypass Blocks
 * Allows keyboard and screen reader users to skip directly to main content
 */
export default function SkipLink({
  targetId,
  label = 'Skip to main content'
}: SkipLinkProps) {
  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    const target = document.getElementById(targetId);
    if (target) {
      // Set focus to the target element
      target.setAttribute('tabindex', '-1');
      target.focus();
      // Remove tabindex after focus to prevent issues
      target.addEventListener('blur', () => {
        target.removeAttribute('tabindex');
      }, { once: true });
    }
  };

  return (
    <a
      href={`#${targetId}`}
      onClick={handleClick}
      className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-amc-primary focus:text-white focus:rounded-md focus:shadow-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white transition-all duration-200"
      aria-label={label}
    >
      {label}
    </a>
  );
}
