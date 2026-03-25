import { Suspense } from 'react'

export default function AgentPage({ params }: { params: { id: string } }) {
  return (
    <div>
      <h1>Agent {params.id}</h1>
      <p>Agent details page</p>
    </div>
  )
}

export function generateStaticParams() {
  return [
    { id: '1' },
    { id: '2' },
    { id: '3' }
  ]
}
