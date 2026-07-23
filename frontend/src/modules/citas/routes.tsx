import type { RouteObject } from 'react-router-dom'
import { CitasPage } from './pages'

export const citasRoutes: RouteObject[] = [
  { path: 'citas', element: <CitasPage /> },
]
