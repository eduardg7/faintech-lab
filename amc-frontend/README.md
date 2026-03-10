# Agent Memory Cloud - Frontend Dashboard

Next.js 14 dashboard for the Agent Memory Cloud API.

## Features

- 🔐 **Auth Flow**: API key authentication with localStorage persistence
- 📋 **Memory List**: Paginated list of agent memories with infinite scroll
- 🔍 **Search & Filters**: Keyword search and filters by type, agent, tags
- 📱 **Responsive Design**: Mobile-first design with Tailwind CSS
- ⚡ **Real-time Updates**: Automatic polling for new memories (60s interval)

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **State Management**: React Query (TanStack Query)
- **HTTP Client**: Axios
- **Language**: TypeScript

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables:
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000/v1" > .env.local
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Usage

1. Enter your AMC API key (format: `amc_live_xxxxxxxxxx`)
2. View your agent memories in the dashboard
3. Use search and filters to find specific memories
4. Memories auto-update every 60 seconds

## Project Structure

```
src/
├── app/
│   ├── layout.tsx      # Root layout with providers
│   ├── page.tsx        # Main page (auth gate)
│   └── globals.css     # Global styles
├── components/
│   ├── LoginForm.tsx   # API key input form
│   └── MemoryList.tsx  # Memory dashboard component
├── contexts/
│   └── AuthContext.tsx # Auth state management
├── lib/
│   └── api.ts          # API client functions
└── providers/
    └── QueryProvider.tsx # React Query provider
```

## API Integration

The dashboard integrates with the AMC API endpoints:

- `GET /memories` - List memories with filters
- `GET /memories/search` - Search memories by keyword

## Development

- **Build**: `npm run build`
- **Start**: `npm start`
- **Lint**: `npm run lint`

## Environment Variables

- `NEXT_PUBLIC_API_URL` - AMC API base URL (default: http://localhost:8000/v1)
