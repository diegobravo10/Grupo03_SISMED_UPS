import { ContentState, SectionHeader, StatusBadge } from '@/components'
import type { ComprobanteVentaResponse } from '../api'

interface ComprobantesTableProps {
  comprobantes: ComprobanteVentaResponse[]
  isLoading: boolean
  errorMessage: string | null
  onReload: () => void
}

const currencyFormatter = new Intl.NumberFormat('es-EC', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})

export function ComprobantesTable({
  comprobantes,
  isLoading,
  errorMessage,
  onReload,
}: ComprobantesTableProps) {
  let content

  if (isLoading) {
    content = <ContentState variant="loading" message="Consultando comprobantes registrados." />
  } else if (errorMessage) {
    content = (
      <ContentState
        variant="error"
        message={errorMessage}
        action={
          <button className="text-button" type="button" onClick={onReload}>
            Reintentar
          </button>
        }
      />
    )
  } else if (comprobantes.length === 0) {
    content = (
      <ContentState
        variant="empty"
        title="Sin comprobantes"
        message="Aún no existen comprobantes registrados."
      />
    )
  } else {
    content = (
      <div className="data-table-wrapper" role="region" aria-label="Listado de comprobantes" tabIndex={0}>
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Comprobante</th>
              <th>Cliente</th>
              <th>Emisión</th>
              <th>Subtotal</th>
              <th>IGV</th>
              <th>Total</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            {comprobantes.map((comprobante) => (
              <tr key={comprobante.id}>
                <td className="data-table__code">{comprobante.id}</td>
                <td>
                  <strong className="table-primary">
                    {comprobante.tipo_comprobante} {comprobante.serie}-{comprobante.numero}
                  </strong>
                  <span className="table-secondary">{comprobante.fecha_creacion}</span>
                </td>
                <td>
                  <strong className="table-primary">{comprobante.cliente_nombre}</strong>
                  <span className="table-secondary">{comprobante.cliente_documento}</span>
                </td>
                <td>{comprobante.fecha_emision}</td>
                <td>{currencyFormatter.format(comprobante.subtotal)}</td>
                <td>{currencyFormatter.format(comprobante.igv)}</td>
                <td>
                  <strong className="table-primary">{currencyFormatter.format(comprobante.total)}</strong>
                </td>
                <td>
                  <StatusBadge tone="success">{comprobante.estado}</StatusBadge>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }

  return (
    <section className="content-section admin-card">
      <SectionHeader
        title="Listado de comprobantes"
        description="Comprobantes emitidos y su información fiscal."
        action={
          <button className="text-button" type="button" onClick={onReload}>
            Actualizar
          </button>
        }
      />
      {content}
    </section>
  )
}
