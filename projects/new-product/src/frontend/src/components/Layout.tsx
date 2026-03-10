import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import clsx from 'clsx'

interface LayoutProps {
  children: ReactNode
}

const navItems = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/memories', label: 'Memories', icon: '📝' },
  { path: '/search', label: 'Search', icon: '🔍' },
  { path: '/settings', label: 'Settings', icon: '⚙️' },
]

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()
  const { logout } = useAuth()

  return (
    <div className="min-h-screen bg-dark-950 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-dark-900 border-r border-dark-800 flex flex-col">
        {/* Logo */}
        <div className="p-6 border-b border-dark-800">
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <span className="text-2xl">🧠</span>
            Agent Memory Cloud
          </h1>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {navItems.map(item => (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={clsx(
                    'flex items-center gap-3 px-4 py-3 rounded-lg transition-colors',
                    location.pathname === item.path
                      ? 'bg-primary-600 text-white'
                      : 'text-dark-300 hover:bg-dark-800 hover:text-white'
                  )}
                >
                  <span className="text-lg">{item.icon}</span>
                  <span className="font-medium">{item.label}</span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-dark-800">
          <button
            onClick={logout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-dark-400 hover:bg-dark-800 hover:text-white transition-colors"
          >
            <span className="text-lg">🚪</span>
            <span className="font-medium">Logout</span>
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  )
}
