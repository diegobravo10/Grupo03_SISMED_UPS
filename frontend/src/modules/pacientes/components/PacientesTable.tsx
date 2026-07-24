import type { Paciente } from '../api'

interface PacientesTableProps {
  pacientes: Paciente[]
  onView: (paciente: Paciente) => void
  onEdit: (paciente: Paciente) => void
}

export function PacientesTable({ pacientes, onView, onEdit }: PacientesTableProps) {
  return (
    <div className="data-table-wrapper">
      <table className="data-table management-table">
        <thead>
          <tr>
            <th>Paciente</th>
            <th>Cédula</th>
            <th>Teléfono</th>
            <th aria-label="Acciones" />
          </tr>
        </thead>
        <tbody>
          {pacientes.map((paciente) => (
            <tr key={paciente.id}>
              <td>
                <span className="table-primary">{paciente.nombres} {paciente.apellidos}</span>
                <span className="table-secondary">ID #{paciente.id}</span>
              </td>
              <td className="data-table__code">{paciente.cedula}</td>
              <td>{paciente.telefono}</td>
              <td className="management-table__actions">
                <button className="table-action" onClick={() => onView(paciente)} type="button">Ver</button>
                <button className="table-action" onClick={() => onEdit(paciente)} type="button">Editar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
