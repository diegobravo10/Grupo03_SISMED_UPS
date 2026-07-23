import { Link } from 'react-router-dom'
import { Icon, SectionHeader } from '@/components'
import type { QuickAction } from '../types'

interface QuickActionsProps {
  actions: QuickAction[]
}

export function QuickActions({ actions }: QuickActionsProps) {
  return (
    <aside className="content-section quick-actions">
      <SectionHeader
        title="Accesos rápidos"
        description="Operaciones frecuentes"
      />
      <div className="quick-actions__list">
        {actions.map((action) => (
          <Link className="quick-action" key={action.label} to={action.to}>
            <span className="quick-action__icon">
              <Icon name={action.icon} />
            </span>
            <span className="quick-action__content">
              <strong>{action.label}</strong>
              <small>{action.description}</small>
            </span>
            <Icon className="quick-action__chevron" name="chevron" size={17} />
          </Link>
        ))}
      </div>
    </aside>
  )
}
