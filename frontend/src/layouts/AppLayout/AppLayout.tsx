import { useState } from 'react'
import { NavLink, Outlet, useLocation } from 'react-router-dom'
import { Icon, type IconName } from '@/components'

interface NavigationItem {
  to: string
  label: string
  icon: IconName
}

const mainNavigation: NavigationItem[] = [
  { to: '/', label: 'Dashboard', icon: 'dashboard' },
  { to: '/pacientes', label: 'Pacientes', icon: 'patient' },
  { to: '/medicos', label: 'Médicos', icon: 'doctor' },
  { to: '/citas', label: 'Citas', icon: 'calendar' },
]

const administrationNavigation: NavigationItem[] = [
  { to: '/administracion/caja', label: 'Caja', icon: 'cash' },
  {
    to: '/administracion/comprobantes',
    label: 'Comprobantes',
    icon: 'receipt',
  },
]

export function AppLayout() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const { pathname } = useLocation()
  const activeItem = [...mainNavigation, ...administrationNavigation].find(
    ({ to }) => (to === '/' ? pathname === '/' : pathname.startsWith(to)),
  )

  const closeSidebar = () => setIsSidebarOpen(false)

  return (
    <div className={`app-shell${isSidebarOpen ? ' app-shell--menu-open' : ''}`}>
      <aside className="sidebar" aria-label="Barra lateral">
        <div className="brand">
          <span className="brand__mark" aria-hidden="true">
            <span />
            <span />
          </span>
          <span>
            <strong>SISMED</strong>
            <small>Gestión médica</small>
          </span>
        </div>

        <nav className="sidebar__nav" aria-label="Navegación principal">
          <p className="sidebar__section-label">Principal</p>
          {mainNavigation.map(({ to, label, icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              onClick={closeSidebar}
              className={({ isActive }) =>
                `nav-link${isActive ? ' nav-link--active' : ''}`
              }
            >
              <Icon name={icon} />
              <span>{label}</span>
            </NavLink>
          ))}

          <p className="sidebar__section-label sidebar__section-label--spaced">
            Gestión interna
          </p>
          <NavLink
            to="/administracion"
            end
            onClick={closeSidebar}
            className={({ isActive }) =>
              `nav-link${isActive ? ' nav-link--active' : ''}`
            }
          >
            <Icon name="administracion" />
            <span>Administración</span>
          </NavLink>
          <div className="nav-children">
          {administrationNavigation.map(({ to, label, icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={closeSidebar}
              className={({ isActive }) =>
                `nav-link nav-link--nested${isActive ? ' nav-link--active' : ''}`
              }
            >
              <Icon name={icon} />
              <span>{label}</span>
            </NavLink>
          ))}
          </div>
        </nav>

        <div className="sidebar__footer">
          <span className="system-status" aria-hidden="true" />
          <span>
            <strong>Sistema disponible</strong>
            <small>Entorno local</small>
          </span>
        </div>
      </aside>

      <button
        className="sidebar-backdrop"
        aria-label="Cerrar menú"
        onClick={closeSidebar}
        type="button"
      />

      <div className="workspace">
        <header className="topbar">
          <div className="topbar__context">
            <button
              className="icon-button topbar__menu"
              aria-label="Abrir menú"
              onClick={() => setIsSidebarOpen(true)}
              type="button"
            >
              <Icon name="menu" />
            </button>
            <div>
              <span className="topbar__eyebrow">Sistema médico</span>
              <strong>{activeItem?.label ?? 'Administración'}</strong>
            </div>
          </div>

          <div className="topbar__actions">
            <label className="search-control">
              <Icon name="search" size={18} />
              <span className="sr-only">Buscar en SISMED</span>
              <input
                type="search"
                placeholder="Buscar paciente, cita..."
                aria-label="Buscar en SISMED"
              />
              <kbd>Ctrl K</kbd>
            </label>

            <div className="user-summary">
              <span className="user-summary__avatar">AU</span>
              <span className="user-summary__details">
                <strong>Administrador</strong>
                <small>Gestión general</small>
              </span>
            </div>
          </div>
        </header>

        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
