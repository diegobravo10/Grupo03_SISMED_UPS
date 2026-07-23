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
