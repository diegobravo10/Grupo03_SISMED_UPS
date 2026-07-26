export type EstadoCita =
  | 'SEPARADA'
  | 'CONFIRMADA'
  | 'EN_SALA_ESPERA'
  | 'ATENDIDA'
  | 'CANCELADA'
  | 'NO_ASISTIO'

export interface CitaInput {
  paciente_id: number
  medico_id: number
  fecha: string
  hora_inicio: string
  hora_fin: string
  motivo: string
}

export interface Cita extends CitaInput {
  id: number
  estado: EstadoCita
  fecha_creacion: string
}

export const ESTADOS_CITA: EstadoCita[] = [
  'SEPARADA',
  'CONFIRMADA',
  'EN_SALA_ESPERA',
  'ATENDIDA',
  'CANCELADA',
  'NO_ASISTIO',
]

export const TRANSICIONES_PERMITIDAS: Record<EstadoCita, EstadoCita[]> = {
  SEPARADA: ['CONFIRMADA', 'CANCELADA', 'NO_ASISTIO'],
  CONFIRMADA: ['EN_SALA_ESPERA', 'CANCELADA', 'NO_ASISTIO'],
  EN_SALA_ESPERA: ['ATENDIDA', 'NO_ASISTIO'],
  ATENDIDA: [],
  CANCELADA: [],
  NO_ASISTIO: [],
}

export const LABELS_ESTADO: Record<EstadoCita, string> = {
  SEPARADA: 'Separada',
  CONFIRMADA: 'Confirmada',
  EN_SALA_ESPERA: 'En sala de espera',
  ATENDIDA: 'Atendida',
  CANCELADA: 'Cancelada',
  NO_ASISTIO: 'No asistió',
}

export const TONO_ESTADO: Record<EstadoCita, 'neutral' | 'success' | 'warning'> = {
  SEPARADA: 'neutral',
  CONFIRMADA: 'success',
  EN_SALA_ESPERA: 'warning',
  ATENDIDA: 'success',
  CANCELADA: 'neutral',
  NO_ASISTIO: 'warning',
}
