import type { IconName } from '@/components'

export interface DashboardSummary {
  patients: number
  doctors: number
  scheduledAppointments: number
}

export type AppointmentStatus =
  | 'Confirmada'
  | 'En espera'
  | 'Completada'
  | 'Cancelada'

export interface RecentAppointment {
  id: string
  date: string
  time: string
  patient: string
  doctor: string
  specialty: string
  status: AppointmentStatus
}

export interface QuickAction {
  label: string
  description: string
  to: string
  icon: IconName
}
