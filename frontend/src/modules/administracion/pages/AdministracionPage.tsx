import { PageHeader } from '@/components'

interface AdministracionPageProps {
  section?: 'Administración' | 'Caja' | 'Comprobantes'
}

export function AdministracionPage({
  section = 'Administración',
}: AdministracionPageProps) {
  return (
    <PageHeader
      eyebrow="Administración"
      title={section}
      description={`Espacio reservado para la gestión de ${section.toLowerCase()}.`}
    />
  )
}
