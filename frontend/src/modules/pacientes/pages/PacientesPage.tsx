import { ContentState, PageHeader, SectionHeader } from '@/components'
import { useCallback, useEffect, useState } from 'react'
import { pacientesApi, type Paciente } from '../api'
import { PacientesTable } from '../components'

export function PacientesPage() {
  const [pacientes, setPacientes] = useState<Paciente[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

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

  return (
    <div className="page">
      <PageHeader eyebrow="Atención médica" title="Pacientes" description="Consulta y administra los pacientes registrados." />
      <section className="content-section">
        <SectionHeader title="Listado de pacientes" description="Registros disponibles en SISMED" />
        {isLoading && <ContentState variant="loading" />}
        {errorMessage && <ContentState variant="error" message={errorMessage} action={<button className="text-button" onClick={() => void loadPacientes()} type="button">Reintentar</button>} />}
        {!isLoading && !errorMessage && pacientes.length === 0 && <ContentState variant="empty" title="Aún no hay pacientes" message="Registra el primer paciente para verlo en este listado." />}
        {!isLoading && !errorMessage && pacientes.length > 0 && <PacientesTable pacientes={pacientes} onView={() => undefined} onEdit={() => undefined} />}
      </section>
    </div>
  )
}
