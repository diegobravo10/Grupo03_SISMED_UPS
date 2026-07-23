import type { ReactNode } from 'react'

type ContentStateVariant = 'loading' | 'empty' | 'error'

interface ContentStateProps {
  variant: ContentStateVariant
  title?: string
  message?: string
  action?: ReactNode
}

const defaults: Record<
  ContentStateVariant,
  { title: string; message: string }
> = {
  loading: {
    title: 'Cargando información',
    message: 'Espera mientras consultamos los datos.',
  },
  empty: {
    title: 'Sin registros',
    message: 'No hay información disponible para mostrar.',
  },
  error: {
    title: 'No se pudo cargar la información',
    message: 'Verifica la conexión e inténtalo nuevamente.',
  },
}

export function ContentState({
  variant,
  title = defaults[variant].title,
  message = defaults[variant].message,
  action,
}: ContentStateProps) {
  return (
    <div
      className={`content-state content-state--${variant}`}
      role={variant === 'error' ? 'alert' : 'status'}
      aria-live="polite"
    >
      {variant === 'loading' && <span className="loading-indicator" />}
      {variant !== 'loading' && (
        <span className="content-state__symbol" aria-hidden="true">
          {variant === 'error' ? '!' : '—'}
        </span>
      )}
      <div className="content-state__copy">
        <strong>{title}</strong>
        <p>{message}</p>
      </div>
      {action && <div className="content-state__action">{action}</div>}
    </div>
  )
}
