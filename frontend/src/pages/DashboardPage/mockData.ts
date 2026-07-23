import type {
  DashboardSummary,
  QuickAction,
  RecentAppointment,
} from './types'

export const dashboardSummaryMock: DashboardSummary = {
  patients: 1284,
  doctors: 32,
  scheduledAppointments: 24,
}

export const recentAppointmentsMock: RecentAppointment[] = [
  {
    id: 'CIT-0248',
    date: '23 jul 2026',
    time: '08:30',
    patient: 'María González',
    doctor: 'Dra. Ana Torres',
    specialty: 'Medicina general',
    status: 'Confirmada',
  },
  {
    id: 'CIT-0249',
    date: '23 jul 2026',
    time: '09:15',
    patient: 'Carlos Vega',
    doctor: 'Dr. Luis Paredes',
    specialty: 'Cardiología',
    status: 'En espera',
  },
  {
    id: 'CIT-0245',
    date: '22 jul 2026',
    time: '16:40',
    patient: 'Lucía Herrera',
    doctor: 'Dra. Ana Torres',
    specialty: 'Medicina general',
    status: 'Completada',
  },
  {
    id: 'CIT-0243',
    date: '22 jul 2026',
    time: '14:00',
    patient: 'Jorge Salazar',
    doctor: 'Dr. Mateo Ruiz',
    specialty: 'Traumatología',
    status: 'Cancelada',
  },
]

export const quickActionsMock: QuickAction[] = [
  {
    label: 'Registrar paciente',
    description: 'Crear una nueva ficha clínica',
    to: '/pacientes',
    icon: 'patient',
  },
  {
    label: 'Crear cita',
    description: 'Programar una atención médica',
    to: '/citas',
    icon: 'calendar',
  },
  {
    label: 'Registrar ingreso',
    description: 'Añadir un movimiento de caja',
    to: '/administracion/caja',
    icon: 'cash',
  },
]
