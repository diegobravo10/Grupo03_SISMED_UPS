import { createApiService } from '@/api'
import type {
  ConsultaIngresosParams,
  TransaccionCajaCreate,
  TransaccionCajaResponse,
} from './types'

const administracionService = createApiService('/admin')

export function registrarIngresoCaja(payload: TransaccionCajaCreate) {
  return administracionService.post<TransaccionCajaResponse, TransaccionCajaCreate>(
    '/caja/ingresos',
    payload,
  )
}

export function registrarEgresoCaja(payload: TransaccionCajaCreate) {
  return administracionService.post<TransaccionCajaResponse, TransaccionCajaCreate>(
    '/caja/egresos',
    payload,
  )
}

export function consultarIngresosPorRango(params: ConsultaIngresosParams) {
  return administracionService.get<TransaccionCajaResponse[]>('/caja/ingresos', {
    query: {
      fecha_inicio: params.fecha_inicio,
      fecha_fin: params.fecha_fin,
    },
  })
}
