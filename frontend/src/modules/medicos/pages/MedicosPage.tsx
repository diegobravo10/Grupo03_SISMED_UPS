import { ContentState, PageHeader, SectionHeader } from '@/components'
import { useCallback, useEffect, useState } from 'react'
import { medicosApi, type Medico } from '../api'
import { MedicoForm, MedicosTable } from '../components'

export function MedicosPage() {
  const [medicos, setMedicos] = useState<Medico[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [formMedico, setFormMedico] = useState<Medico | null | undefined>(undefined)
  const [viewMedico, setViewMedico] = useState<Medico | null>(null)
  const loadMedicos = useCallback(async () => {
    setIsLoading(true); setErrorMessage(null)
    try { setMedicos(await medicosApi.listar()) }
    catch (error) { setErrorMessage(error instanceof Error ? error.message : 'No se pudo cargar la lista.') }
    finally { setIsLoading(false) }
  }, [])
  useEffect(() => { void loadMedicos() }, [loadMedicos])
  const saveMedico = async (payload: Parameters<typeof medicosApi.crear>[0]) => {
    if (formMedico) await medicosApi.actualizar(formMedico.id, payload)
    else await medicosApi.crear(payload)
    setFormMedico(undefined); await loadMedicos()
  }
  const view = async (medico: Medico) => setViewMedico(await medicosApi.obtener(medico.id))
  return (
    <div className="page"><PageHeader eyebrow="Equipo médico" title="Médicos" description="Consulta y administra los profesionales médicos." />
      <section className="content-section"><SectionHeader title="Listado de médicos" description="Profesionales registrados en SISMED" action={<button className="button button--primary" onClick={() => setFormMedico(null)} type="button">Nuevo médico</button>} />
        {isLoading && <ContentState variant="loading" />}
        {errorMessage && <ContentState variant="error" message={errorMessage} action={<button className="text-button" onClick={() => void loadMedicos()} type="button">Reintentar</button>} />}
        {!isLoading && !errorMessage && medicos.length === 0 && <ContentState variant="empty" title="Aún no hay médicos" message="Registra el primer profesional para verlo en este listado." />}
        {!isLoading && !errorMessage && medicos.length > 0 && <MedicosTable medicos={medicos} onView={(medico) => void view(medico)} onEdit={setFormMedico} />}
      </section>
      {formMedico !== undefined && <div className="modal-backdrop" role="presentation"><section className="management-modal" aria-modal="true" role="dialog" aria-label={formMedico ? 'Editar médico' : 'Registrar médico'}><SectionHeader title={formMedico ? 'Editar médico' : 'Registrar médico'} /><MedicoForm medico={formMedico ?? undefined} onCancel={() => setFormMedico(undefined)} onSaved={saveMedico} /></section></div>}
      {viewMedico && <div className="modal-backdrop" role="presentation"><section className="management-modal" aria-modal="true" role="dialog" aria-label="Detalle del médico"><SectionHeader title="Detalle del médico" /><div className="detail-list"><p><span>Médico</span>{viewMedico.nombres}</p><p><span>Especialidad</span>{viewMedico.especialidad}</p><div className="admin-actions"><button className="button button--primary" onClick={() => setViewMedico(null)} type="button">Cerrar</button></div></div></section></div>}
    </div>
  )
}
