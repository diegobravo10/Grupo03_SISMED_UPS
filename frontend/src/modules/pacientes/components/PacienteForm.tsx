import { useState, type FormEventHandler } from 'react'
import type { Paciente, PacienteInput } from '../api'

interface PacienteFormProps {
  paciente?: Paciente
  onCancel: () => void
  onSaved: (payload: PacienteInput) => Promise<void>
}

const emptyForm: PacienteInput = { cedula: '', nombres: '', apellidos: '', telefono: '' }

export function PacienteForm({ paciente, onCancel, onSaved }: PacienteFormProps) {
  const [form, setForm] = useState<PacienteInput>(paciente ?? emptyForm)
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const isEditing = Boolean(paciente)

  const update = (field: keyof PacienteInput, value: string) => setForm((current) => ({ ...current, [field]: value }))
  const submit: FormEventHandler<HTMLFormElement> = async (event) => {
    event.preventDefault()
    const payload = Object.fromEntries(Object.entries(form).map(([key, value]) => [key, value.trim()])) as PacienteInput
    if (!/^\d{10}$/.test(payload.cedula)) return setError('La cédula debe contener exactamente 10 dígitos.')
    if (payload.nombres.length < 2 || payload.apellidos.length < 2) return setError('Ingresa nombres y apellidos válidos.')
    if (payload.telefono.length < 7) return setError('Ingresa un teléfono válido.')
    setError(null)
    setIsSubmitting(true)
    try { await onSaved(payload) } catch (reason) { setError(reason instanceof Error ? reason.message : 'No se pudo guardar el paciente.') } finally { setIsSubmitting(false) }
  }

  return <form className="admin-form" onSubmit={submit} noValidate>
    <div className="admin-form-grid admin-form-grid--2">
      <label className="admin-field"><span>Nombres</span><input autoFocus value={form.nombres} onChange={(event) => update('nombres', event.target.value)} required /></label>
      <label className="admin-field"><span>Apellidos</span><input value={form.apellidos} onChange={(event) => update('apellidos', event.target.value)} required /></label>
    </div>
    <div className="admin-form-grid admin-form-grid--2">
      <label className="admin-field"><span>Cédula</span><input inputMode="numeric" maxLength={10} value={form.cedula} onChange={(event) => update('cedula', event.target.value.replace(/\D/g, ''))} required /></label>
      <label className="admin-field"><span>Teléfono</span><input inputMode="tel" value={form.telefono} onChange={(event) => update('telefono', event.target.value)} required /></label>
    </div>
    {error && <p className="admin-feedback admin-feedback--error" role="alert">{error}</p>}
    <div className="admin-actions modal-actions"><button className="button" onClick={onCancel} type="button">Cancelar</button><button className="button button--primary" disabled={isSubmitting} type="submit">{isSubmitting ? 'Guardando...' : isEditing ? 'Guardar cambios' : 'Registrar paciente'}</button></div>
  </form>
}
