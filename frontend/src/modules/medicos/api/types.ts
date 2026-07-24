export interface MedicoInput {
  nombres: string
  especialidad: string
}

export interface Medico extends MedicoInput {
  id: number
}
