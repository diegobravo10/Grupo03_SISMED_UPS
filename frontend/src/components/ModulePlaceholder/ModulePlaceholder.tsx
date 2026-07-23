import { PageHeader } from '@/components/PageHeader'

interface ModulePlaceholderProps {
  eyebrow: string
  title: string
  description: string
}

export function ModulePlaceholder({
  eyebrow,
  title,
  description,
}: ModulePlaceholderProps) {
  return (
    <div className="page">
      <PageHeader
        eyebrow={eyebrow}
        title={title}
        description={description}
      />
      <div className="module-placeholder" aria-label={`${title}: próximamente`}>
        <span className="module-placeholder__line" aria-hidden="true" />
        <div>
          <strong>Módulo preparado</strong>
          <p>Las funciones de gestión se incorporarán en esta sección.</p>
        </div>
      </div>
    </div>
  )
}
