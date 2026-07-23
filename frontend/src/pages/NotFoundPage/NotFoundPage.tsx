import { Link } from 'react-router-dom'
import { PageHeader } from '@/components'

export function NotFoundPage() {
  return (
    <div className="page not-found-page">
      <span className="not-found-page__code">404</span>
      <PageHeader
        eyebrow="Ruta no disponible"
        title="Página no encontrada"
        description="La dirección ingresada no existe o fue modificada."
      />
      <Link className="button button--primary" to="/dashboard">
        Volver al Dashboard
      </Link>
    </div>
  )
}
