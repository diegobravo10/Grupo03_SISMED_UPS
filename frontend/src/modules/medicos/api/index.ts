import { createApiService } from '@/api'
import type { Medico, MedicoInput } from './types'

export const medicosService = createApiService('/medicos')

export const medicosApi = {
  listar: () => medicosService.get<Medico[]>(),
  obtener: (id: number) => medicosService.get<Medico>(String(id)),
  crear: (payload: MedicoInput) => medicosService.post<Medico>('', payload),
  actualizar: (id: number, payload: MedicoInput) =>
    medicosService.put<Medico>(String(id), payload),
}

export type { Medico, MedicoInput } from './types'
