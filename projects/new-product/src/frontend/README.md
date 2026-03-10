# Agent Memory Cloud Dashboard

React + TypeScript + Vite dashboard for Agent Memory Cloud.

## Tech Stack
- React 19
- TypeScript
- Vite 6
- Tailwind CSS
- React Router v7
- TanStack Query
- Recharts

## Getting Started

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Run E2E tests
npm run test:e2e
```

## Pages
- **Dashboard** (`/`) - Overview with analytics and agent leaderboard
- **Memories** (`/memories`) - Browse and filter agent memories
- **Search** (`/search`) - Full-text search across all memories
- **Settings** (`/settings`) - Manage API keys and usage stats

## Mock Data
Currently using mock data in `src/api/mockApi.ts`. This will be replaced with actual API calls once the backend (AMC-003) is complete.

## Next Steps
- [ ] Integrate with actual API endpoints
- [ ] Add E2E tests with Playwright
- [ ] Add loading states and error handling
- [ ] Implement real authentication flow
- [ ] Deploy to Vercel
