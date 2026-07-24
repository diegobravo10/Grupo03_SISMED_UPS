import { useState, type FormEventHandler } from 'react'
import { SectionHeader } from '@/components'
import type { ConsultaIngresosParams } from '../api'

interface IngresosRangoFormProps {
  onSearch: (params: ConsultaIngresosParams) => Promise<void>
}

interface FormState {
  fecha_inicio: string
  fecha_fin: string
}

const initialState: FormState = {
  fecha_inicio: '',
  fecha_fin: '',
}

export function IngresosRangoForm({ onSearch }: IngresosRangoFormProps) {
  const [form, setForm] = useState<FormState>(initialState)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  const updateField = (name: keyof FormState, value: string) => {
    setForm((current) => ({ ...current, [name]: value }))
  }

  const handleSubmit: FormEventHandler<HTMLFormElement> = async (event) => {
    event.preventDefault()
    setErrorMessage(null)

    if (form.fecha_inicio > form.fecha_fin) {
      setErrorMessage('La fecha de inicio no puede ser mayor que la fecha de fin.')
      return
    }

    setIsSubmitting(true)
    try {
      await onSearch(form)
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'No se pudo consultar los ingresos.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <section className="content-section admin-card">
      <SectionHeader
        title="Consultar ingresos por fechas"
        description="Filtra ingresos de caja por rango de fechas."
      />

      <form className="admin-form" onSubmit={handleSubmit}>
        <div className="admin-form-grid admin-form-grid--2">
          <label className="admin-field">
            <span>Fecha inicio</span>
            <input
              type="date"
              name="fecha_inicio"
              value={form.fecha_inicio}
              onChange={(event) => updateField('fecha_inicio', event.target.value)}
              required
            />
          </label>

          <label className="admin-field">
            <span>Fecha fin</span>
            <input
              type="date"
              name="fecha_fin"
              value={form.fecha_fin}
              onChange={(event) => updateField('fecha_fin', event.target.value)}
              required
            />
          </label>
        </div>

        {errorMessage && (
          <p className="admin-feedback admin-feedback--error" role="alert">
            {errorMessage}
          </p>
        )}

        <div className="admin-actions">
          <button className="button button--primary" disabled={isSubmitting} type="submit">
            {isSubmitting ? 'Consultando...' : 'Consultar ingresos'}
          </button>
        </div>
      </form>
    </section>
  )
}
