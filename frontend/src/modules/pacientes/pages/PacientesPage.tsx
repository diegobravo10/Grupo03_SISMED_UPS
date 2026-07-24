import { ContentState, PageHeader, SectionHeader } from '@/components'
import { useCallback, useEffect, useState } from 'react'
import { pacientesApi, type Paciente } from '../api'
import { PacienteForm, PacientesTable } from '../components'

export function PacientesPage() {
  const [pacientes, setPacientes] = useState<Paciente[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [formPaciente, setFormPaciente] = useState<Paciente | null | undefined>(undefined)
  const [viewPaciente, setViewPaciente] = useState<Paciente | null>(null)

  const loadPacientes = useCallback(async () => {
    setIsLoading(true)
    setErrorMessage(null)
    try {
      setPacientes(await pacientesApi.listar())
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'No se pudo cargar la lista.')
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => { void loadPacientes() }, [loadPacientes])

  const savePaciente = async (payload: Parameters<typeof pacientesApi.crear>[0]) => {
    if (formPaciente) await pacientesApi.actualizar(formPaciente.id, payload)
    else await pacientesApi.crear(payload)
    setFormPaciente(undefined)
    await loadPacientes()
  }

  const view = async (paciente: Paciente) => setViewPaciente(await pacientesApi.obtener(paciente.id))

  return (
    <div className="page">
      <PageHeader eyebrow="Atención médica" title="Pacientes" description="Consulta y administra los pacientes registrados." />
      <section className="content-section">
        <SectionHeader title="Listado de pacientes" description="Registros disponibles en SISMED" action={<button className="button button--primary" onClick={() => setFormPaciente(null)} type="button">Nuevo paciente</button>} />
        {isLoading && <ContentState variant="loading" />}
        {errorMessage && <ContentState variant="error" message={errorMessage} action={<button className="text-button" onClick={() => void loadPacientes()} type="button">Reintentar</button>} />}
        {!isLoading && !errorMessage && pacientes.length === 0 && <ContentState variant="empty" title="Aún no hay pacientes" message="Registra el primer paciente para verlo en este listado." />}
        {!isLoading && !errorMessage && pacientes.length > 0 && <PacientesTable pacientes={pacientes} onView={(paciente) => void view(paciente)} onEdit={setFormPaciente} />}
      </section>
      {formPaciente !== undefined && <div className="modal-backdrop" role="presentation"><section className="management-modal" aria-modal="true" role="dialog" aria-label={formPaciente ? 'Editar paciente' : 'Registrar paciente'}><SectionHeader title={formPaciente ? 'Editar paciente' : 'Registrar paciente'} /><PacienteForm paciente={formPaciente ?? undefined} onCancel={() => setFormPaciente(undefined)} onSaved={savePaciente} /></section></div>}
      {viewPaciente && <div className="modal-backdrop" role="presentation"><section className="management-modal" aria-modal="true" role="dialog" aria-label="Detalle del paciente"><SectionHeader title="Detalle del paciente" /><div className="detail-list"><p><span>Nombres</span>{viewPaciente.nombres} {viewPaciente.apellidos}</p><p><span>Cédula</span>{viewPaciente.cedula}</p><p><span>Teléfono</span>{viewPaciente.telefono}</p><div className="admin-actions"><button className="button button--primary" onClick={() => setViewPaciente(null)} type="button">Cerrar</button></div></div></section></div>}
    </div>
  )
}
