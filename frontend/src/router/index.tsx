import { Navigate, createBrowserRouter } from 'react-router-dom'
import { AppLayout } from '@/layouts'
import { DashboardPage, NotFoundPage } from '@/pages'
import {
  administracionRoutes,
  citasRoutes,
  medicosRoutes,
  pacientesRoutes,
} from '@/modules'

export const appRouter = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: 'dashboard', element: <DashboardPage /> },
      ...pacientesRoutes,
      ...medicosRoutes,
      ...citasRoutes,
      ...administracionRoutes,
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])
