import { ContentState, PageHeader, SectionHeader, StatusBadge } from '@/components'
import { useCallback, useEffect, useState } from 'react'
import { citasApi, type Cita, type CitaInput, type EstadoCita } from '../api'
import { LABELS_ESTADO, TONO_ESTADO } from '../api'
import { pacientesApi, type Paciente } from '@/modules/pacientes/api'
import { medicosApi, type Medico } from '@/modules/medicos/api'
import { CitaForm, CitasTable } from '../components'

export function CitasPage() {
  const [citas, setCitas] = useState<Cita[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [formCita, setFormCita] = useState<Cita | null | undefined>(undefined)
  const [viewCita, setViewCita] = useState<Cita | null>(null)
  const [estadoCita, setEstadoCita] = useState<Cita | null>(null)
  const [pacientes, setPacientes] = useState<Paciente[]>([])
  const [medicos, setMedicos] = useState<Medico[]>([])

  const nombresPacientes: Record<number, string> = {}
  for (const p of pacientes) {
    nombresPacientes[p.id] = `${p.nombres} ${p.apellidos}`
  }

  const nombresMedicos: Record<number, string> = {}
  for (const m of medicos) {
    nombresMedicos[m.id] = `${m.nombres} - ${m.especialidad}`
  }

  const loadCitas = useCallback(async () => {
    setIsLoading(true)
    setErrorMessage(null)
    try {
      setCitas(await citasApi.listar())
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : 'No se pudo cargar la lista de citas.',
      )
    } finally {
      setIsLoading(false)
    }
  }, [])

  const loadLookups = useCallback(async () => {
    try {
      const [p, m] = await Promise.all([
        pacientesApi.listar(),
        medicosApi.listar(),
      ])
      setPacientes(p)
      setMedicos(m)
    } catch {
      // lookups are best-effort; table will show IDs as fallback
    }
  }, [])

  useEffect(() => {
    void loadCitas()
    void loadLookups()
  }, [loadCitas, loadLookups])

  const saveCita = async (payload: CitaInput) => {
    if (formCita) await citasApi.actualizar(formCita.id, payload)
    else await citasApi.crear(payload)
    setFormCita(undefined)
    await loadCitas()
  }

  const view = async (cita: Cita) => setViewCita(await citasApi.obtener(cita.id))

  const cambiarEstado = async (cita: Cita, nuevoEstado: EstadoCita) => {
    try {
      await citasApi.cambiarEstado(cita.id, nuevoEstado)
      await loadCitas()
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : 'No se pudo cambiar el estado.',
      )
    }
  }

  return (
    <div className="page">
      <PageHeader
        eyebrow="Agenda médica"
        title="Citas"
        description="Consulta y administra las citas médicas registradas."
      />
      <section className="content-section">
        <SectionHeader
          title="Listado de citas"
          description="Citas programadas en SISMED"
          action={
            <button
              className="button button--primary"
              onClick={() => setFormCita(null)}
              type="button"
            >
              Nueva cita
            </button>
          }
        />
        {isLoading && <ContentState variant="loading" />}
        {errorMessage && (
          <ContentState
            variant="error"
            message={errorMessage}
            action={
              <button
                className="text-button"
                onClick={() => void loadCitas()}
                type="button"
              >
                Reintentar
              </button>
            }
          />
        )}
        {!isLoading && !errorMessage && citas.length === 0 && (
          <ContentState
            variant="empty"
            title="Aún no hay citas"
            message="Registra la primera cita para verla en este listado."
          />
        )}
        {!isLoading && !errorMessage && citas.length > 0 && (
          <CitasTable
            citas={citas}
            nombresPacientes={nombresPacientes}
            nombresMedicos={nombresMedicos}
            onView={(cita) => void view(cita)}
            onEdit={setFormCita}
            onCambiarEstado={cambiarEstado}
          />
        )}
      </section>

      {formCita !== undefined && (
        <div className="modal-backdrop" role="presentation">
          <section
            className="management-modal"
            aria-modal="true"
            role="dialog"
            aria-label={formCita ? 'Editar cita' : 'Registrar cita'}
          >
            <SectionHeader
              title={formCita ? 'Editar cita' : 'Registrar cita'}
            />
            <CitaForm
              cita={formCita ?? undefined}
              onCancel={() => setFormCita(undefined)}
              onSaved={saveCita}
            />
          </section>
        </div>
      )}

      {viewCita && (
        <div className="modal-backdrop" role="presentation">
          <section
            className="management-modal"
            aria-modal="true"
            role="dialog"
            aria-label="Detalle de la cita"
          >
            <SectionHeader title="Detalle de la cita" />
            <div className="detail-list">
              <p>
                <span>Paciente</span>
                {nombresPacientes[viewCita.paciente_id] ??
                  `Paciente #${viewCita.paciente_id}`}
              </p>
              <p>
                <span>Médico</span>
                {nombresMedicos[viewCita.medico_id] ??
                  `Médico #${viewCita.medico_id}`}
              </p>
              <p>
                <span>Fecha</span>
                {viewCita.fecha}
              </p>
              <p>
                <span>Horario</span>
                {viewCita.hora_inicio} - {viewCita.hora_fin}
              </p>
              <p>
                <span>Estado</span>
                <StatusBadge tone={TONO_ESTADO[viewCita.estado]}>
                  {LABELS_ESTADO[viewCita.estado]}
                </StatusBadge>
              </p>
              {viewCita.motivo && (
                <p>
                  <span>Motivo</span>
                  {viewCita.motivo}
                </p>
              )}
              <p>
                <span>Registro</span>
                {new Date(viewCita.fecha_creacion).toLocaleString()}
              </p>
              <div className="admin-actions">
                <button
                  className="button button--primary"
                  onClick={() => setViewCita(null)}
                  type="button"
                >
                  Cerrar
                </button>
              </div>
            </div>
          </section>
        </div>
      )}

      {estadoCita && (
        <div className="modal-backdrop" role="presentation">
          <section
            className="management-modal"
            aria-modal="true"
            role="dialog"
            aria-label="Cambiar estado"
          >
            <SectionHeader title="Cambiar estado de la cita" />
            <div className="admin-form">
              <div className="admin-form-grid">
                <label className="admin-field">
                  <span>Estado actual</span>
                  <StatusBadge tone={TONO_ESTADO[estadoCita.estado]}>
                    {LABELS_ESTADO[estadoCita.estado]}
                  </StatusBadge>
                </label>
              </div>
              <div className="admin-actions modal-actions">
                <button
                  className="button"
                  onClick={() => setEstadoCita(null)}
                  type="button"
                >
                  Cancelar
                </button>
              </div>
            </div>
          </section>
        </div>
      )}
    </div>
  )
}
