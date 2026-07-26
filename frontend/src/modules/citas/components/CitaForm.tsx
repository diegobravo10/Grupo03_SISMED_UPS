import { useEffect, useState, type FormEventHandler } from 'react'
import type { Cita, CitaInput } from '../api'
import { pacientesApi, type Paciente } from '@/modules/pacientes/api'
import { medicosApi, type Medico } from '@/modules/medicos/api'

interface CitaFormProps {
  cita?: Cita
  onCancel: () => void
  onSaved: (payload: CitaInput) => Promise<void>
}

const emptyForm: CitaInput = {
  paciente_id: 0,
  medico_id: 0,
  fecha: '',
  hora_inicio: '',
  hora_fin: '',
  motivo: '',
}

export function CitaForm({ cita, onCancel, onSaved }: CitaFormProps) {
  const [form, setForm] = useState<CitaInput>(
    cita
      ? {
          paciente_id: cita.paciente_id,
          medico_id: cita.medico_id,
          fecha: cita.fecha,
          hora_inicio: cita.hora_inicio,
          hora_fin: cita.hora_fin,
          motivo: cita.motivo ?? '',
        }
      : emptyForm,
  )
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [pacientes, setPacientes] = useState<Paciente[]>([])
  const [medicos, setMedicos] = useState<Medico[]>([])
  const isEditing = Boolean(cita)

  useEffect(() => {
    void pacientesApi.listar().then(setPacientes).catch(() => {})
    void medicosApi.listar().then(setMedicos).catch(() => {})
  }, [])

  const update = <K extends keyof CitaInput>(field: K, value: CitaInput[K]) =>
    setForm((current) => ({ ...current, [field]: value }))

  const submit: FormEventHandler<HTMLFormElement> = async (event) => {
    event.preventDefault()

    if (!form.paciente_id) return setError('Selecciona un paciente.')
    if (!form.medico_id) return setError('Selecciona un médico.')
    if (!form.fecha) return setError('Selecciona una fecha.')
    if (!form.hora_inicio) return setError('Selecciona la hora de inicio.')
    if (!form.hora_fin) return setError('Selecciona la hora de fin.')
    if (form.hora_inicio >= form.hora_fin)
      return setError('La hora de inicio debe ser anterior a la hora de fin.')

    setError(null)
    setIsSubmitting(true)
    try {
      await onSaved({
        paciente_id: form.paciente_id,
        medico_id: form.medico_id,
        fecha: form.fecha,
        hora_inicio: form.hora_inicio,
        hora_fin: form.hora_fin,
        motivo: form.motivo.trim(),
      })
    } catch (reason) {
      setError(
        reason instanceof Error ? reason.message : 'No se pudo guardar la cita.',
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form className="admin-form" onSubmit={submit} noValidate>
      <div className="admin-form-grid admin-form-grid--2">
        <label className="admin-field">
          <span>Paciente</span>
          <select
            value={form.paciente_id || ''}
            onChange={(e) => update('paciente_id', Number(e.target.value))}
            required
          >
            <option value="">Seleccionar paciente</option>
            {pacientes.map((p) => (
              <option key={p.id} value={p.id}>
                {p.nombres} {p.apellidos}
              </option>
            ))}
          </select>
        </label>
        <label className="admin-field">
          <span>Médico</span>
          <select
            value={form.medico_id || ''}
            onChange={(e) => update('medico_id', Number(e.target.value))}
            required
          >
            <option value="">Seleccionar médico</option>
            {medicos.map((m) => (
              <option key={m.id} value={m.id}>
                {m.nombres} - {m.especialidad}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div className="admin-form-grid admin-form-grid--3">
        <label className="admin-field">
          <span>Fecha</span>
          <input
            type="date"
            value={form.fecha}
            onChange={(e) => update('fecha', e.target.value)}
            required
          />
        </label>
        <label className="admin-field">
          <span>Hora inicio</span>
          <input
            type="time"
            value={form.hora_inicio}
            onChange={(e) => update('hora_inicio', e.target.value)}
            required
          />
        </label>
        <label className="admin-field">
          <span>Hora fin</span>
          <input
            type="time"
            value={form.hora_fin}
            onChange={(e) => update('hora_fin', e.target.value)}
            required
          />
        </label>
      </div>
      <div className="admin-form-grid">
        <label className="admin-field">
          <span>Motivo (opcional)</span>
          <input
            value={form.motivo}
            onChange={(e) => update('motivo', e.target.value)}
            placeholder="Motivo de la consulta"
          />
        </label>
      </div>
      {error && (
        <p className="admin-feedback admin-feedback--error" role="alert">
          {error}
        </p>
      )}
      <div className="admin-actions modal-actions">
        <button className="button" onClick={onCancel} type="button">
          Cancelar
        </button>
        <button
          className="button button--primary"
          disabled={isSubmitting}
          type="submit"
        >
          {isSubmitting
            ? 'Guardando...'
            : isEditing
              ? 'Guardar cambios'
              : 'Registrar cita'}
        </button>
      </div>
    </form>
  )
}
