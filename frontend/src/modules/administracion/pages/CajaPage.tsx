import { useMemo, useState } from 'react'
import { PageHeader } from '@/components'
import {
  consultarIngresosPorRango,
  registrarEgresoCaja,
  registrarIngresoCaja,
  type ConsultaIngresosParams,
  type TransaccionCajaCreate,
  type TransaccionCajaResponse,
} from '../api'
import {
  CajaMovimientoForm,
  IngresosRangoForm,
  IngresosTable,
} from '../components'

export function CajaPage() {
  const [ingresos, setIngresos] = useState<TransaccionCajaResponse[]>([])
  const [isLoadingIngresos, setIsLoadingIngresos] = useState(false)
  const [ingresosError, setIngresosError] = useState<string | null>(null)
  const [hasSearched, setHasSearched] = useState(false)

  const totalIngresos = useMemo(
    () => ingresos.reduce((total, item) => total + item.monto, 0),
    [ingresos],
  )

  const handleRegistrarIngreso = (payload: TransaccionCajaCreate) => {
    return registrarIngresoCaja({ ...payload, tipo: 'INGRESO' })
  }

  const handleRegistrarEgreso = (payload: TransaccionCajaCreate) => {
    return registrarEgresoCaja({ ...payload, tipo: 'EGRESO' })
  }

  const handleConsultarIngresos = async (params: ConsultaIngresosParams) => {
    setIsLoadingIngresos(true)
    setIngresosError(null)
    setHasSearched(true)
    try {
      const data = await consultarIngresosPorRango(params)
      setIngresos(data)
    } catch (error) {
      setIngresosError(
        error instanceof Error ? error.message : 'No se pudieron consultar los ingresos.',
      )
      setIngresos([])
      throw error
    } finally {
      setIsLoadingIngresos(false)
    }
  }

  return (
    <div className="page">
      <PageHeader
        eyebrow="Administración"
        title="Caja"
        description="Registro de movimientos y consulta de ingresos por fechas."
      />

      <div className="admin-grid admin-grid--2">
        <CajaMovimientoForm
          tipo="INGRESO"
          title="Registrar ingreso"
          description="Registra un movimiento tipo INGRESO."
          submitLabel="Registrar ingreso"
          onSubmitted={handleRegistrarIngreso}
        />

        <CajaMovimientoForm
          tipo="EGRESO"
          title="Registrar egreso"
          description="Registra un movimiento tipo EGRESO."
          submitLabel="Registrar egreso"
          onSubmitted={handleRegistrarEgreso}
        />
      </div>

      <div className="admin-stack">
        <IngresosRangoForm onSearch={handleConsultarIngresos} />
        <IngresosTable
          ingresos={ingresos}
          isLoading={isLoadingIngresos}
          errorMessage={ingresosError}
          hasSearched={hasSearched}
          totalIngresos={totalIngresos}
        />
      </div>
    </div>
  )
}
