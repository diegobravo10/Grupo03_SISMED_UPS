import type { DashboardSummary } from '../types'

interface SummaryMetricsProps {
  summary: DashboardSummary
}

const numberFormatter = new Intl.NumberFormat('es-EC')

export function SummaryMetrics({ summary }: SummaryMetricsProps) {
  const metrics = [
    {
      label: 'Pacientes registrados',
      value: summary.patients,
      detail: 'Historias clínicas activas',
    },
    {
      label: 'Médicos registrados',
      value: summary.doctors,
      detail: 'Profesionales en el sistema',
    },
    {
      label: 'Citas programadas',
      value: summary.scheduledAppointments,
      detail: 'Agenda del día',
    },
  ]

  return (
    <section className="metrics-strip" aria-label="Resumen general">
      {metrics.map((metric) => (
        <div className="metric" key={metric.label}>
          <span>{metric.label}</span>
          <strong>{numberFormatter.format(metric.value)}</strong>
          <small>{metric.detail}</small>
        </div>
      ))}
    </section>
  )
}
