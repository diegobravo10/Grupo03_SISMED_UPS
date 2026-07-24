import { useState, type FormEventHandler } from 'react'
import type { Medico, MedicoInput } from '../api'

interface MedicoFormProps { medico?: Medico; onCancel: () => void; onSaved: (payload: MedicoInput) => Promise<void> }
const emptyForm: MedicoInput = { nombres: '', especialidad: '' }

export function MedicoForm({ medico, onCancel, onSaved }: MedicoFormProps) {
  const [form, setForm] = useState<MedicoInput>(medico ?? emptyForm)
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const update = (field: keyof MedicoInput, value: string) => setForm((current) => ({ ...current, [field]: value }))
  const submit: FormEventHandler<HTMLFormElement> = async (event) => {
    event.preventDefault()
    const payload: MedicoInput = { nombres: form.nombres.trim(), especialidad: form.especialidad.trim() }
    if (payload.nombres.length < 3) return setError('Ingresa el nombre completo del médico.')
    if (payload.especialidad.length < 3) return setError('Ingresa una especialidad válida.')
    setError(null); setIsSubmitting(true)
    try { await onSaved(payload) } catch (reason) { setError(reason instanceof Error ? reason.message : 'No se pudo guardar el médico.') } finally { setIsSubmitting(false) }
  }
  return <form className="admin-form" onSubmit={submit} noValidate>
    <div className="admin-form-grid admin-form-grid--2">
      <label className="admin-field"><span>Nombres completos</span><input autoFocus value={form.nombres} onChange={(event) => update('nombres', event.target.value)} required /></label>
      <label className="admin-field"><span>Especialidad</span><input value={form.especialidad} onChange={(event) => update('especialidad', event.target.value)} placeholder="Ej. Medicina general" required /></label>
    </div>
    {error && <p className="admin-feedback admin-feedback--error" role="alert">{error}</p>}
    <div className="admin-actions modal-actions"><button className="button" onClick={onCancel} type="button">Cancelar</button><button className="button button--primary" disabled={isSubmitting} type="submit">{isSubmitting ? 'Guardando...' : medico ? 'Guardar cambios' : 'Registrar médico'}</button></div>
  </form>
}
