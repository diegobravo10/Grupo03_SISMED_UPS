import { StatusBadge } from '@/components'
import type { Cita, EstadoCita } from '../api'
import { LABELS_ESTADO, TONO_ESTADO, TRANSICIONES_PERMITIDAS } from '../api'

interface CitasTableProps {
  citas: Cita[]
  nombresPacientes: Record<number, string>
  nombresMedicos: Record<number, string>
  onView: (cita: Cita) => void
  onEdit: (cita: Cita) => void
  onCambiarEstado: (cita: Cita, nuevoEstado: EstadoCita) => void
}

export function CitasTable({
  citas,
  nombresPacientes,
  nombresMedicos,
  onView,
  onEdit,
  onCambiarEstado,
}: CitasTableProps) {
  return (
    <div className="data-table-wrapper">
      <table className="data-table management-table">
        <thead>
          <tr>
            <th>Paciente</th>
            <th>Médico</th>
            <th>Fecha</th>
            <th>Horario</th>
            <th>Estado</th>
            <th aria-label="Acciones" />
          </tr>
        </thead>
        <tbody>
          {citas.map((cita) => {
            const transiciones = TRANSICIONES_PERMITIDAS[cita.estado]
            return (
              <tr key={cita.id}>
                <td>
                  <span className="table-primary">
                    {nombresPacientes[cita.paciente_id] ?? `Paciente #${cita.paciente_id}`}
                  </span>
                  <span className="table-secondary">ID #{cita.id}</span>
                </td>
                <td>
                  <span className="table-primary">
                    {nombresMedicos[cita.medico_id] ?? `Médico #${cita.medico_id}`}
                  </span>
                </td>
                <td>
                  <span className="appointment-date">{cita.fecha}</span>
                </td>
                <td>
                  <span className="data-table__time">
                    {cita.hora_inicio} - {cita.hora_fin}
                  </span>
                </td>
                <td>
                  <StatusBadge tone={TONO_ESTADO[cita.estado]}>
                    {LABELS_ESTADO[cita.estado]}
                  </StatusBadge>
                </td>
                <td className="management-table__actions">
                  <button
                    className="table-action"
                    onClick={() => onView(cita)}
                    type="button"
                  >
                    Ver
                  </button>
                  {cita.estado !== 'ATENDIDA' &&
                    cita.estado !== 'CANCELADA' && (
                      <button
                        className="table-action"
                        onClick={() => onEdit(cita)}
                        type="button"
                      >
                        Editar
                      </button>
                    )}
                  {transiciones.length > 0 && (
                    <select
                      className="estado-select"
                      value=""
                      onChange={(e) => {
                        if (e.target.value) {
                          onCambiarEstado(
                            cita,
                            e.target.value as EstadoCita,
                          )
                        }
                      }}
                    >
                      <option value="">Estado...</option>
                      {transiciones.map((est) => (
                        <option key={est} value={est}>
                          {LABELS_ESTADO[est]}
                        </option>
                      ))}
                    </select>
                  )}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
