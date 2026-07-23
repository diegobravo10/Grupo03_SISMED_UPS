import { Link } from 'react-router-dom'
import { ContentState, SectionHeader, StatusBadge } from '@/components'
import type { AppointmentStatus, RecentAppointment } from '../types'

interface RecentAppointmentsTableProps {
  appointments: RecentAppointment[]
  isLoading?: boolean
  error?: string
}

function getStatusTone(status: AppointmentStatus) {
  if (status === 'Confirmada' || status === 'Completada') return 'success'
  if (status === 'En espera') return 'warning'
  return 'neutral'
}

export function RecentAppointmentsTable({
  appointments,
  isLoading = false,
  error,
}: RecentAppointmentsTableProps) {
  let content

  if (isLoading) {
    content = <ContentState variant="loading" message="Consultando las citas recientes." />
  } else if (error) {
    content = <ContentState variant="error" message={error} />
  } else if (appointments.length === 0) {
    content = (
      <ContentState
        variant="empty"
        title="Sin citas recientes"
        message="Las citas registradas aparecerán en esta sección."
      />
    )
  } else {
    content = (
      <div
        className="data-table-wrapper"
        role="region"
        aria-label="Citas recientes"
        tabIndex={0}
      >
        <table className="data-table">
          <thead>
            <tr>
              <th>Código</th>
              <th>Fecha y hora</th>
              <th>Paciente</th>
              <th>Profesional</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            {appointments.map((appointment) => (
              <tr key={appointment.id}>
                <td className="data-table__code">{appointment.id}</td>
                <td>
                  <span className="appointment-date">{appointment.date}</span>
                  <span className="appointment-time">{appointment.time}</span>
                </td>
                <td>
                  <strong className="table-primary">
                    {appointment.patient}
                  </strong>
                </td>
                <td>
                  <strong className="table-primary">
                    {appointment.doctor}
                  </strong>
                  <span className="table-secondary">
                    {appointment.specialty}
                  </span>
                </td>
                <td>
                  <StatusBadge tone={getStatusTone(appointment.status)}>
                    {appointment.status}
                  </StatusBadge>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }

  return (
    <section className="content-section dashboard-appointments">
      <SectionHeader
        title="Citas recientes"
        description="Últimos registros de la agenda médica"
        action={
          <Link className="text-button" to="/citas">
            Ver todas las citas
          </Link>
        }
      />

      {content}
    </section>
  )
}
