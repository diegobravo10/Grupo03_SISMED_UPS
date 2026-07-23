import type { RouteObject } from 'react-router-dom'
import { MedicosPage } from './pages'

export const medicosRoutes: RouteObject[] = [
  { path: 'medicos', element: <MedicosPage /> },
]
