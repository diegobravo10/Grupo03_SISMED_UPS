export interface PacienteInput {
  cedula: string
  nombres: string
  apellidos: string
  telefono: string
}

export interface Paciente extends PacienteInput {
  id: number
}
