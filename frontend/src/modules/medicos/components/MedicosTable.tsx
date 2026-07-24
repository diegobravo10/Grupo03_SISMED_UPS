import type { Medico } from '../api'

interface MedicosTableProps {
  medicos: Medico[]
  onView: (medico: Medico) => void
  onEdit: (medico: Medico) => void
}

export function MedicosTable({ medicos, onView, onEdit }: MedicosTableProps) {
  return <div className="data-table-wrapper"><table className="data-table management-table"><thead><tr><th>Médico</th><th>Especialidad</th><th aria-label="Acciones" /></tr></thead><tbody>
    {medicos.map((medico) => <tr key={medico.id}><td><span className="table-primary">{medico.nombres}</span><span className="table-secondary">ID #{medico.id}</span></td><td>{medico.especialidad}</td><td className="management-table__actions"><button className="table-action" onClick={() => onView(medico)} type="button">Ver</button><button className="table-action" onClick={() => onEdit(medico)} type="button">Editar</button></td></tr>)}
  </tbody></table></div>
}
