import { useCallback, useEffect, useState } from 'react'
import { PageHeader } from '@/components'
import {
  listarComprobantes,
  registrarComprobante,
  type ComprobanteVentaCreate,
  type ComprobanteVentaResponse,
} from '../api'
import {
  ComprobanteForm,
  ComprobantesTable,
} from '../components'

export function ComprobantesPage() {
  const [comprobantes, setComprobantes] = useState<ComprobanteVentaResponse[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  const cargarComprobantes = useCallback(async () => {
    setIsLoading(true)
    setErrorMessage(null)
    try {
      const data = await listarComprobantes()
      setComprobantes(data)
    } catch (error) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : 'No se pudieron cargar los comprobantes.',
      )
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    void cargarComprobantes()
  }, [cargarComprobantes])

  const handleCreate = async (payload: ComprobanteVentaCreate) => {
    const created = await registrarComprobante(payload)
    await cargarComprobantes()
    return created
  }

  return (
    <div className="page">
      <PageHeader
        eyebrow="Administración"
        title="Comprobantes"
        description="Registro y consulta de comprobantes de venta."
      />

      <div className="admin-stack">
        <ComprobanteForm onCreated={handleCreate} />
        <ComprobantesTable
          comprobantes={comprobantes}
          isLoading={isLoading}
          errorMessage={errorMessage}
          onReload={() => {
            void cargarComprobantes()
          }}
        />
      </div>
    </div>
  )
}
