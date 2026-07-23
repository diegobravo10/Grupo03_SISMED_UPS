# Frontend SISMED

Base modular del cliente web construida con React, TypeScript y Vite.

## Inicio

```bash
cp .env.example .env
npm install
npm run dev
```

## Convenciones

- `src/modules`: módulos de negocio independientes.
- `src/components`: componentes reutilizables sin lógica de negocio.
- `src/pages`: páginas globales ajenas a un módulo.
- `src/api`: infraestructura compartida para comunicación HTTP.
- Cada módulo expone únicamente su API pública desde `index.ts`.
- Las dependencias entre módulos deben pasar por sus APIs públicas; no importar archivos internos.

## Consumo de la API

La URL del backend se configura en `.env`:

```env
VITE_API_URL=http://127.0.0.1:8000
```

El cliente compartido normaliza respuestas JSON, texto y respuestas vacías. Los
servicios de cada módulo ya incluyen su prefijo del backend:

```ts
import { pacientesService } from '@/modules/pacientes'
import { isHttpError, isNetworkError } from '@/api'

try {
  const pacientes = await pacientesService.get<PacienteResponse[]>()
} catch (error) {
  if (isHttpError(error)) {
    console.error(error.status, error.message)
  } else if (isNetworkError(error)) {
    console.error('API no disponible')
  }
}
```

Cada equipo debe definir sus tipos y operaciones concretas dentro de
`src/modules/<modulo>/api`; los componentes no deben construir URLs directamente.
