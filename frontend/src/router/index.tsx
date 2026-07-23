import { createBrowserRouter } from 'react-router-dom'
import { AppLayout } from '@/layouts'
import { HomePage, NotFoundPage } from '@/pages'
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
    errorElement: <NotFoundPage />,
    children: [
      { index: true, element: <HomePage /> },
      ...pacientesRoutes,
      ...medicosRoutes,
      ...citasRoutes,
      ...administracionRoutes,
    ],
  },
])
