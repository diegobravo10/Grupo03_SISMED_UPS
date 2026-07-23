import { PageHeader } from '@/components'
import {
  QuickActions,
  RecentAppointmentsTable,
  SummaryMetrics,
} from './components'
import {
  dashboardSummaryMock,
  quickActionsMock,
  recentAppointmentsMock,
} from './mockData'

export function DashboardPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Resumen operativo"
        title="Dashboard"
        description="Información general y actividad reciente de SISMED"
      />

      <SummaryMetrics summary={dashboardSummaryMock} />

      <div className="dashboard-grid">
        <RecentAppointmentsTable appointments={recentAppointmentsMock} />
        <QuickActions actions={quickActionsMock} />
      </div>
    </div>
  )
}
