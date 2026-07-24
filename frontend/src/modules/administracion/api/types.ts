export interface ComprobanteVentaCreate {
  tipo_comprobante: string
  serie: string
  numero: string
  cliente_nombre: string
  cliente_documento: string
  fecha_emision: string
  subtotal: number
  igv: number
  total: number
}

export interface ComprobanteVentaResponse extends ComprobanteVentaCreate {
  id: number
  estado: string
  fecha_creacion: string
}

export interface TransaccionCajaCreate {
  tipo: string
  concepto: string
  monto: number
  fecha: string
  comprobante_id?: number | null
}

export interface TransaccionCajaResponse {
  id: number
  tipo: string
  concepto: string
  monto: number
  fecha: string
  comprobante_id?: number | null
  fecha_creacion: string
}

export interface ConsultaIngresosParams {
  fecha_inicio: string
  fecha_fin: string
}
