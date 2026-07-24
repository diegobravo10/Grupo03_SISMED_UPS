import { ContentState, SectionHeader } from '@/components'
import type { TransaccionCajaResponse } from '../api'

interface IngresosTableProps {
  ingresos: TransaccionCajaResponse[]
  isLoading: boolean
  errorMessage: string | null
  hasSearched: boolean
  totalIngresos: number
}

const currencyFormatter = new Intl.NumberFormat('es-EC', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})

export function IngresosTable({
  ingresos,
  isLoading,
  errorMessage,
  hasSearched,
  totalIngresos,
}: IngresosTableProps) {
  let content

  if (isLoading) {
    content = <ContentState variant="loading" message="Consultando ingresos de caja." />
  } else if (errorMessage) {
    content = <ContentState variant="error" message={errorMessage} />
  } else if (!hasSearched) {
    content = (
      <ContentState
        variant="empty"
        title="Aún no se realizó la consulta"
        message="Selecciona un rango de fechas para ver resultados."
      />
    )
  } else if (ingresos.length === 0) {
    content = (
      <ContentState
        variant="empty"
        title="Sin ingresos en el rango"
        message="No hay movimientos tipo INGRESO para las fechas seleccionadas."
      />
    )
  } else {
    content = (
      <div className="data-table-wrapper" role="region" aria-label="Ingresos por rango de fechas" tabIndex={0}>
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Fecha</th>
              <th>Concepto</th>
              <th>Tipo</th>
              <th>Comprobante</th>
              <th>Monto</th>
            </tr>
          </thead>
          <tbody>
            {ingresos.map((ingreso) => (
              <tr key={ingreso.id}>
                <td className="data-table__code">{ingreso.id}</td>
                <td>{ingreso.fecha}</td>
                <td>{ingreso.concepto}</td>
                <td>{ingreso.tipo}</td>
                <td>{ingreso.comprobante_id ?? '—'}</td>
                <td>
                  <strong className="table-primary">{currencyFormatter.format(ingreso.monto)}</strong>
                </td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr>
              <td colSpan={5} className="admin-table-total-label">
                Total de ingresos consultados
              </td>
              <td className="admin-table-total-value">{currencyFormatter.format(totalIngresos)}</td>
            </tr>
          </tfoot>
        </table>
      </div>
    )
  }

  return (
    <section className="content-section admin-card">
      <SectionHeader
        title="Resultados de ingresos"
        description="Detalle de ingresos dentro del rango consultado."
      />
      {content}
    </section>
  )
}
