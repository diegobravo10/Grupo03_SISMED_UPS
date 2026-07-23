import { Navigate, type RouteObject } from 'react-router-dom'
import { CajaPage, ComprobantesPage } from './pages'

export const administracionRoutes: RouteObject[] = [
  {
    path: 'administracion',
    children: [
      { index: true, element: <Navigate to="caja" replace /> },
      { path: 'caja', element: <CajaPage /> },
      { path: 'comprobantes', element: <ComprobantesPage /> },
    ],
  },
]
