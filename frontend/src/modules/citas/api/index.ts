import { createApiService } from '@/api'
import type { Cita, CitaInput } from './types'

export const citasService = createApiService('/citas')

export const citasApi = {
  listar: () => citasService.get<Cita[]>(),
  obtener: (id: number) => citasService.get<Cita>(String(id)),
  crear: (payload: CitaInput) => citasService.post<Cita>('', payload),
  actualizar: (id: number, payload: CitaInput) =>
    citasService.put<Cita>(String(id), payload),
  cambiarEstado: (id: number, estado: string) =>
    citasService.put<Cita>(`${id}/estado`, { estado }),
  listarPorMedico: (medicoId: number) =>
    citasService.get<Cita[]>(`medico/${medicoId}`),
  listarPorPaciente: (pacienteId: number) =>
    citasService.get<Cita[]>(`paciente/${pacienteId}`),
}

export type { Cita, CitaInput, EstadoCita } from './types'
export { ESTADOS_CITA, TRANSICIONES_PERMITIDAS, LABELS_ESTADO, TONO_ESTADO } from './types'
