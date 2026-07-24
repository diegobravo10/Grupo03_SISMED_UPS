import { useState, type FormEventHandler } from 'react'
import { SectionHeader } from '@/components'
import type { TransaccionCajaCreate, TransaccionCajaResponse } from '../api'

type TipoMovimiento = 'INGRESO' | 'EGRESO'

interface CajaMovimientoFormProps {
  tipo: TipoMovimiento
  title: string
  description: string
  submitLabel: string
  onSubmitted: (payload: TransaccionCajaCreate) => Promise<TransaccionCajaResponse>
}

interface FormState {
  concepto: string
  monto: string
  fecha: string
  comprobante_id: string
}

const initialState: FormState = {
  concepto: '',
  monto: '',
  fecha: '',
  comprobante_id: '',
}

export function CajaMovimientoForm({
  tipo,
  title,
  description,
  submitLabel,
  onSubmitted,
}: CajaMovimientoFormProps) {
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

    const monto = Number(form.monto)
    if (Number.isNaN(monto) || monto <= 0) {
      setErrorMessage('El monto debe ser mayor que cero.')
      return
    }

    const rawComprobanteId = form.comprobante_id.trim()
    const comprobanteId = rawComprobanteId ? Number(rawComprobanteId) : null

    if (comprobanteId !== null && (!Number.isInteger(comprobanteId) || comprobanteId <= 0)) {
      setErrorMessage('El ID de comprobante debe ser un entero positivo.')
      return
    }

    const payload: TransaccionCajaCreate = {
      tipo,
      concepto: form.concepto.trim(),
      monto,
      fecha: form.fecha,
      comprobante_id: comprobanteId,
    }

    setIsSubmitting(true)
    try {
      await onSubmitted(payload)
      setSuccessMessage('Movimiento registrado correctamente.')
      setForm(initialState)
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : 'No se pudo registrar el movimiento.',
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <section className="content-section admin-card">
      <SectionHeader title={title} description={description} />

      <form className="admin-form" onSubmit={handleSubmit}>
        <div className="admin-form-grid admin-form-grid--2">
          <label className="admin-field">
            <span>Concepto</span>
            <input
              name="concepto"
              value={form.concepto}
              onChange={(event) => updateField('concepto', event.target.value)}
              placeholder="Detalle del movimiento"
              required
            />
          </label>

          <label className="admin-field">
            <span>Fecha</span>
            <input
              type="date"
              name="fecha"
              value={form.fecha}
              onChange={(event) => updateField('fecha', event.target.value)}
              required
            />
          </label>
        </div>

        <div className="admin-form-grid admin-form-grid--2">
          <label className="admin-field">
            <span>Monto</span>
            <input
              type="number"
              step="0.01"
              min="0.01"
              name="monto"
              value={form.monto}
              onChange={(event) => updateField('monto', event.target.value)}
              required
            />
          </label>

          <label className="admin-field">
            <span>ID de comprobante (opcional)</span>
            <input
              type="number"
              min="1"
              step="1"
              name="comprobante_id"
              value={form.comprobante_id}
              onChange={(event) => updateField('comprobante_id', event.target.value)}
              placeholder="Ej: 25"
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
            {isSubmitting ? 'Guardando...' : submitLabel}
          </button>
        </div>
      </form>
    </section>
  )
}
