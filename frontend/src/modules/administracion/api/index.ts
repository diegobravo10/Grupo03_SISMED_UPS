import { createApiService } from '@/api'

export const administracionService = createApiService('/admin')

export {
	listarComprobantes,
	registrarComprobante,
} from './comprobantes'
export {
	consultarIngresosPorRango,
	registrarEgresoCaja,
	registrarIngresoCaja,
} from './caja'
export type {
	ComprobanteVentaCreate,
	ComprobanteVentaResponse,
	ConsultaIngresosParams,
	TransaccionCajaCreate,
	TransaccionCajaResponse,
} from './types'
