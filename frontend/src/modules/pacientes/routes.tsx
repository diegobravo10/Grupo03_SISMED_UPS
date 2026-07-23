import type { RouteObject } from 'react-router-dom'
import { PacientesPage } from './pages'

export const pacientesRoutes: RouteObject[] = [
  { path: 'pacientes', element: <PacientesPage /> },
]
