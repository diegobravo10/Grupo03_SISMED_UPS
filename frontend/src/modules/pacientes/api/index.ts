import { createApiService } from '@/api'
import type { Paciente, PacienteInput } from './types'

export const pacientesService = createApiService('/pacientes')

export const pacientesApi = {
  listar: () => pacientesService.get<Paciente[]>(),
  obtener: (id: number) => pacientesService.get<Paciente>(String(id)),
  crear: (payload: PacienteInput) => pacientesService.post<Paciente>('', payload),
  actualizar: (id: number, payload: PacienteInput) =>
    pacientesService.put<Paciente>(String(id), payload),
}

export type { Paciente, PacienteInput } from './types'
