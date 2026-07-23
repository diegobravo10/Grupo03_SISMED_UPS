import type { RouteObject } from 'react-router-dom'
import { AdministracionPage } from './pages'

export const administracionRoutes: RouteObject[] = [
  {
    path: 'administracion',
    children: [
      { index: true, element: <AdministracionPage /> },
      { path: 'caja', element: <AdministracionPage section="Caja" /> },
      {
        path: 'comprobantes',
        element: <AdministracionPage section="Comprobantes" />,
      },
    ],
  },
]
