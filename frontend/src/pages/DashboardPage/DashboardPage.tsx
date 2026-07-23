import { PageHeader, SectionHeader, StatusBadge } from '@/components'

const agenda = [
  { time: '08:30', patient: 'María González', doctor: 'Dra. Ana Torres', status: 'Confirmada' },
  { time: '09:15', patient: 'Carlos Vega', doctor: 'Dr. Luis Paredes', status: 'En espera' },
  { time: '10:00', patient: 'Lucía Herrera', doctor: 'Dra. Ana Torres', status: 'Confirmada' },
]

export function DashboardPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Resumen operativo"
        title="Dashboard"
        description="Jueves, 23 de julio de 2026"
      />

      <section className="metrics-strip" aria-label="Resumen del día">
        <div className="metric">
          <span>Citas programadas</span>
          <strong>24</strong>
          <small>6 pendientes de confirmar</small>
        </div>
        <div className="metric">
          <span>Pacientes atendidos</span>
          <strong>11</strong>
          <small>Última atención: 11:42</small>
        </div>
        <div className="metric">
          <span>Médicos disponibles</span>
          <strong>7</strong>
          <small>2 consultorios libres</small>
        </div>
        <div className="metric">
          <span>Estado de caja</span>
          <strong>Abierta</strong>
          <small>Desde las 08:02</small>
        </div>
      </section>

      <section className="content-section">
        <SectionHeader
          title="Próximas citas"
          description="Agenda inmediata de atención"
          action={<button className="text-button" type="button">Ver agenda completa</button>}
        />
        <div className="data-table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Hora</th>
                <th>Paciente</th>
                <th>Profesional</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {agenda.map((appointment) => (
                <tr key={`${appointment.time}-${appointment.patient}`}>
                  <td className="data-table__time">{appointment.time}</td>
                  <td>{appointment.patient}</td>
                  <td>{appointment.doctor}</td>
                  <td>
                    <StatusBadge
                      tone={appointment.status === 'Confirmada' ? 'success' : 'warning'}
                    >
                      {appointment.status}
                    </StatusBadge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}
