import { createApiService } from '@/api'
import type {
  ComprobanteVentaCreate,
  ComprobanteVentaResponse,
} from './types'

const administracionService = createApiService('/admin')

export function listarComprobantes() {
  return administracionService.get<ComprobanteVentaResponse[]>('/comprobantes/')
}

export function registrarComprobante(payload: ComprobanteVentaCreate) {
  return administracionService.post<ComprobanteVentaResponse, ComprobanteVentaCreate>(
    '/comprobantes/',
    payload,
  )
}
