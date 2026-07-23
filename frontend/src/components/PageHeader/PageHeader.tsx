interface PageHeaderProps {
  title: string
  description?: string
  eyebrow?: string
}

export function PageHeader({
  title,
  description,
  eyebrow = 'SISMED',
}: PageHeaderProps) {
  return (
    <header className="page-header">
      <p className="page-header__eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      {description && <p className="page-header__description">{description}</p>}
    </header>
  )
}
