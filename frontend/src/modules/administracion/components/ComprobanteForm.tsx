import { useState, type FormEventHandler } from 'react'
import { SectionHeader } from '@/components'
import type {
  ComprobanteVentaCreate,
  ComprobanteVentaResponse,
} from '../api'

interface ComprobanteFormProps {
  onCreated: (payload: ComprobanteVentaCreate) => Promise<ComprobanteVentaResponse>
}

interface FormState {
  tipo_comprobante: string
  serie: string
  numero: string
  cliente_nombre: string
  cliente_documento: string
  fecha_emision: string
  subtotal: string
  igv: string
  total: string
}

const initialState: FormState = {
  tipo_comprobante: '',
  serie: '',
  numero: '',
  cliente_nombre: '',
  cliente_documento: '',
  fecha_emision: '',
  subtotal: '',
  igv: '',
  total: '',
}

function roundTwo(value: number) {
  return Math.round(value * 100) / 100
}

export function ComprobanteForm({ onCreated }: ComprobanteFormProps) {
  const [form, setForm] = useState<FormState>(initialState)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  const updateField = (name: keyof FormState, value: string) => {
    setForm((current) => ({ ...current, [name]: value }))
  }

  const handleSubmit: FormEventHandler<HTMLFormElement> = async (event) => {
    event.preventDefault()
    setErrorMessage(null)
    setSuccessMessage(null)

    const subtotal = Number(form.subtotal)
    const igv = Number(form.igv)
    const total = Number(form.total)

    if ([subtotal, igv, total].some((value) => Number.isNaN(value))) {
      setErrorMessage('Subtotal, IGV y total deben ser valores numéricos válidos.')
      return
    }

    const expectedTotal = roundTwo(subtotal + igv)
    if (roundTwo(total) !== expectedTotal) {
      setErrorMessage('El total debe ser igual a subtotal + IGV (con dos decimales).')
      return
    }

    const payload: ComprobanteVentaCreate = {
      tipo_comprobante: form.tipo_comprobante.trim(),
      serie: form.serie.trim(),
      numero: form.numero.trim(),
      cliente_nombre: form.cliente_nombre.trim(),
      cliente_documento: form.cliente_documento.trim(),
      fecha_emision: form.fecha_emision,
      subtotal,
      igv,
      total,
    }

    setIsSubmitting(true)
    try {
      await onCreated(payload)
      setSuccessMessage('Comprobante registrado correctamente.')
      setForm(initialState)
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : 'No se pudo registrar el comprobante.',
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <section className="content-section admin-card">
      <SectionHeader
        title="Registrar comprobante"
        description="Ingresa los datos del comprobante de venta."
      />

      <form className="admin-form" onSubmit={handleSubmit}>
        <div className="admin-form-grid admin-form-grid--3">
          <label className="admin-field">
            <span>Tipo de comprobante</span>
            <input
              name="tipo_comprobante"
              value={form.tipo_comprobante}
              onChange={(event) => updateField('tipo_comprobante', event.target.value)}
              placeholder="FACTURA"
              required
            />
          </label>

          <label className="admin-field">
            <span>Serie</span>
            <input
              name="serie"
              value={form.serie}
              onChange={(event) => updateField('serie', event.target.value)}
              placeholder="F001"
              required
            />
          </label>

          <label className="admin-field">
            <span>Número</span>
            <input
              name="numero"
              value={form.numero}
              onChange={(event) => updateField('numero', event.target.value)}
              placeholder="000123"
              required
            />
          </label>
        </div>

        <div className="admin-form-grid admin-form-grid--2">
          <label className="admin-field">
            <span>Cliente</span>
            <input
              name="cliente_nombre"
              value={form.cliente_nombre}
              onChange={(event) => updateField('cliente_nombre', event.target.value)}
              placeholder="Nombre del cliente"
              required
            />
          </label>

          <label className="admin-field">
            <span>Documento del cliente</span>
            <input
              name="cliente_documento"
              value={form.cliente_documento}
              onChange={(event) => updateField('cliente_documento', event.target.value)}
              placeholder="Cédula o RUC"
              required
            />
          </label>
        </div>

        <div className="admin-form-grid admin-form-grid--4">
          <label className="admin-field">
            <span>Fecha de emisión</span>
            <input
              type="date"
              name="fecha_emision"
              value={form.fecha_emision}
              onChange={(event) => updateField('fecha_emision', event.target.value)}
              required
            />
          </label>

          <label className="admin-field">
            <span>Subtotal</span>
            <input
              type="number"
              step="0.01"
              name="subtotal"
              value={form.subtotal}
              onChange={(event) => updateField('subtotal', event.target.value)}
              required
            />
          </label>

          <label className="admin-field">
            <span>IGV</span>
            <input
              type="number"
              step="0.01"
              name="igv"
              value={form.igv}
              onChange={(event) => updateField('igv', event.target.value)}
              required
            />
          </label>

          <label className="admin-field">
            <span>Total</span>
            <input
              type="number"
              step="0.01"
              name="total"
              value={form.total}
              onChange={(event) => updateField('total', event.target.value)}
              required
            />
          </label>
        </div>

        {(errorMessage || successMessage) && (
          <p
            className={`admin-feedback${errorMessage ? ' admin-feedback--error' : ' admin-feedback--success'}`}
            role={errorMessage ? 'alert' : 'status'}
          >
            {errorMessage ?? successMessage}
          </p>
        )}

        <div className="admin-actions">
          <button className="button button--primary" disabled={isSubmitting} type="submit">
            {isSubmitting ? 'Guardando...' : 'Registrar comprobante'}
          </button>
        </div>
      </form>
    </section>
  )
}
