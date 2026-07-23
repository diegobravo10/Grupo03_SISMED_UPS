# SISMED Frontend

Aplicación web del Sistema de Gestión Médica SISMED, desarrollada como cliente
del backend académico construido con FastAPI. El frontend proporciona una
interfaz administrativa responsive, navegación por módulos y una infraestructura
común para consumir la API REST.

## Objetivo

Ofrecer una base modular y mantenible para la interfaz de SISMED, de modo que el
equipo pueda desarrollar en paralelo los módulos de pacientes, médicos, citas y
administración sin duplicar componentes, configuración HTTP ni reglas de
navegación.

Actualmente están implementados:

- Layout principal con sidebar y encabezado superior.
- Navegación responsive y señalización de la ruta activa.
- Dashboard con datos temporales de resumen, citas recientes y accesos rápidos.
- Páginas base para los módulos principales.
- Cliente HTTP reutilizable y servicios API separados por módulo.
- Estados visuales reutilizables de carga, vacío y error.
- Página 404 integrada en el layout.

Los formularios y operaciones CRUD de los módulos todavía no están
implementados.

## Integrantes

| Integrante | Rol |
|---|---|
| Diego Bravo | Desarrollador |
| Rafael Serrano | Desarrollador |
| Ariel Paltan | Desarrollador |
| Sebastian Machado | Desarrollador |

## Tecnologías utilizadas

- React 19.
- TypeScript 5.
- Vite 6.
- React Router 7.
- Fetch API para comunicación HTTP.
- CSS modularizado mediante estilos globales, tokens y clases de componentes.
- ESLint 9 para análisis estático.
- npm para gestión de dependencias y scripts.

## Requisitos previos

- Node.js 18 o superior.
- npm, incluido con Node.js.
- Git.
- Backend SISMED disponible si se desea realizar peticiones reales a la API.

## Repositorio del backend

El frontend y el backend forman parte del mismo repositorio:

[Grupo03 SISMED UPS en GitHub](https://github.com/diegobravo10/Grupo03_SISMED_UPS)

El backend se encuentra en la carpeta `app/` de la raíz del repositorio y se
ejecuta con FastAPI. Su configuración e instrucciones están documentadas en el
`README.md` principal.

## Instalación

Desde la raíz del repositorio:

```bash
cd frontend
npm install
```

Luego se debe crear el archivo local de variables de entorno a partir de la
plantilla.

En Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

En Linux o macOS:

```bash
cp .env.example .env
```

El archivo `.env` contiene configuración local y está excluido de Git.

## Variables de entorno y conexión con el backend

La aplicación requiere la variable `VITE_API_URL`:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Esta dirección debe corresponder al servidor FastAPI en ejecución. Si se utiliza
otro puerto o una API desplegada, se debe actualizar el valor sin incluir una
barra final.

El frontend no construye direcciones del backend dentro de los componentes. La
configuración se centraliza en `src/api/config.ts`, mientras que el cliente HTTP
se encuentra en `src/api/httpClient.ts`.

Los servicios ya definidos usan estos prefijos:

| Servicio frontend | Prefijo de la API |
|---|---|
| `pacientesService` | `/pacientes` |
| `medicosService` | `/medicos` |
| `citasService` | `/citas` |
| `administracionService` | `/admin` |

El cliente procesa respuestas JSON, texto y respuestas sin contenido. También
distingue errores HTTP mediante `HttpError` y errores de conexión mediante
`NetworkError`.

## Comandos disponibles

Todos los comandos se ejecutan desde `frontend/`.

| Comando | Descripción |
|---|---|
| `npm run dev` | Inicia el servidor de desarrollo de Vite. |
| `npm run build` | Valida TypeScript y genera el build de producción en `dist/`. |
| `npm run lint` | Ejecuta ESLint sobre el código fuente. |
| `npm run preview` | Sirve localmente el build generado. |

## Ejecución en desarrollo

1. Iniciar el backend desde la raíz del repositorio:

   ```bash
   uvicorn app.main:app --reload
   ```

2. En otra terminal, iniciar el frontend:

   ```bash
   cd frontend
   npm run dev
   ```

3. Abrir en el navegador la dirección mostrada por Vite, normalmente
   `http://localhost:5173`.

## Estructura de carpetas

```text
frontend/
├── src/
│   ├── api/                 # Cliente HTTP, configuración y errores comunes
│   ├── assets/              # Imágenes, iconos y fuentes compartidas
│   ├── components/          # Componentes visuales reutilizables
│   ├── layouts/             # Layout principal de la aplicación
│   ├── modules/             # Módulos independientes del dominio
│   │   ├── administracion/
│   │   ├── citas/
│   │   ├── medicos/
│   │   └── pacientes/
│   ├── pages/               # Dashboard y páginas globales
│   ├── router/              # Configuración central de rutas
│   ├── styles/              # Reset, tokens y estilos globales
│   ├── main.tsx             # Punto de entrada de React
│   └── vite-env.d.ts        # Tipos de variables de entorno
├── .env.example             # Plantilla de configuración local
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

Cada módulo contiene sus propias carpetas `api`, `components` y `pages`, además
de su archivo de rutas. La API pública de cada módulo se expone desde `index.ts`;
no se deben importar directamente archivos internos de otro módulo.

## Módulos y rutas

| Módulo | Ruta | Estado actual |
|---|---|---|
| Dashboard | `/dashboard` | Resumen y tabla con datos mock. |
| Pacientes | `/pacientes` | Página base; CRUD pendiente. |
| Médicos | `/medicos` | Página base; CRUD pendiente. |
| Citas | `/citas` | Página base; CRUD pendiente. |
| Caja | `/administracion/caja` | Página base; operaciones pendientes. |
| Comprobantes | `/administracion/comprobantes` | Página base; operaciones pendientes. |

La ruta `/` redirige al Dashboard y las rutas no reconocidas muestran la página
404 sin ocultar el layout principal.

## Distribución de responsabilidades

Para facilitar el trabajo paralelo, se recomienda la siguiente distribución
modular. Las integraciones compartidas deben revisarse entre todos los
integrantes.

| Integrante | Responsabilidad principal |
|---|---|
| Diego Bravo | Módulo de pacientes y coordinación de contratos compartidos. |
| Rafael Serrano | Módulo de médicos. |
| Ariel Paltan | Módulo de citas. |
| Sebastian Machado | Módulo de administración: caja y comprobantes. |
| Todo el equipo | Layout, componentes reutilizables, router, estilos y cliente HTTP. |

Cada responsable debe trabajar dentro de `src/modules/<modulo>` y consumir las
utilidades compartidas desde `src/api` y `src/components`.

## Uso básico

1. Ingresar a `/dashboard` para visualizar el resumen general de ejemplo.
2. Utilizar el sidebar para navegar entre los módulos.
3. En pantallas pequeñas, abrir el sidebar desde el botón del encabezado; puede
   cerrarse seleccionando una opción, tocando fuera del menú o presionando
   `Escape`.
4. Los accesos rápidos del Dashboard dirigen a las páginas base correspondientes.
5. Las páginas de módulos indican que su implementación funcional está
   pendiente.

Los valores mostrados actualmente en el Dashboard proceden de
`src/pages/DashboardPage/mockData.ts`; todavía no representan información
obtenida del backend.

## Convenciones de desarrollo

- Mantener la lógica específica dentro de su módulo.
- Reutilizar los componentes de `src/components`.
- No escribir URLs del backend dentro de páginas o componentes.
- Definir tipos y operaciones concretas en `src/modules/<modulo>/api`.
- Ejecutar `npm run lint` y `npm run build` antes de integrar cambios.
- No versionar archivos `.env`, `node_modules/` ni `dist/`.
