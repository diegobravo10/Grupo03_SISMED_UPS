import type { RouteObject } from 'react-router-dom'
import { AdministracionPage } from './pages'

export const administracionRoutes: RouteObject[] = [
  { path: 'administracion', element: <AdministracionPage /> },
]
