import { ContentState, PageHeader, SectionHeader } from '@/components'
import { useCallback, useEffect, useState } from 'react'
import { medicosApi, type Medico } from '../api'
import { MedicosTable } from '../components'

export function MedicosPage() {
  const [medicos, setMedicos] = useState<Medico[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const loadMedicos = useCallback(async () => {
    setIsLoading(true); setErrorMessage(null)
    try { setMedicos(await medicosApi.listar()) }
    catch (error) { setErrorMessage(error instanceof Error ? error.message : 'No se pudo cargar la lista.') }
    finally { setIsLoading(false) }
  }, [])
  useEffect(() => { void loadMedicos() }, [loadMedicos])
  return (
    <div className="page"><PageHeader eyebrow="Equipo médico" title="Médicos" description="Consulta y administra los profesionales médicos." />
      <section className="content-section"><SectionHeader title="Listado de médicos" description="Profesionales registrados en SISMED" />
        {isLoading && <ContentState variant="loading" />}
        {errorMessage && <ContentState variant="error" message={errorMessage} action={<button className="text-button" onClick={() => void loadMedicos()} type="button">Reintentar</button>} />}
        {!isLoading && !errorMessage && medicos.length === 0 && <ContentState variant="empty" title="Aún no hay médicos" message="Registra el primer profesional para verlo en este listado." />}
        {!isLoading && !errorMessage && medicos.length > 0 && <MedicosTable medicos={medicos} onView={() => undefined} onEdit={() => undefined} />}
      </section>
    </div>
  )
}
