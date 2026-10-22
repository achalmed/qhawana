/**
 * El módulo web del Observatorio de datos (proyecto Qhawana; fase 10.2b Q2 del contrato de Tiqsi, 2026-10-20): su
 * pantalla, su ruta y cómo entra al menú del anfitrión. Qillqa arma con esto su entrada en el menú (navegacion.ts) y su
 * ruta (App.tsx); la página del Observatorio SOLO (src/qhawana_sola.tsx), su cáscara mínima.
 *
 * El mismo observatorio de la web (Edison 2026-10-01: «no creemos dos observatorios diferentes»). Sus vistas son las
 * opciones del módulo (una sola navegación, Edison 2026-10-06): la barra propia del observatorio se oculta dentro del
 * marco y la página traduce `?vista=` al enlace interno (#catalogo, #comparar…).
 */
import InsightsOutlinedIcon from '@mui/icons-material/InsightsOutlined'
import SpaceDashboardOutlinedIcon from '@mui/icons-material/SpaceDashboardOutlined'
import ViewListOutlinedIcon from '@mui/icons-material/ViewListOutlined'
import StackedLineChartOutlinedIcon from '@mui/icons-material/StackedLineChartOutlined'
import SourceOutlinedIcon from '@mui/icons-material/SourceOutlined'
import ScienceOutlinedIcon from '@mui/icons-material/ScienceOutlined'
import { definirModuloWeb } from '@qillqa/tiqsi'

export const QHAWANA = definirModuloWeb({
  id: 'observatorio',
  nombre: 'Observatorio de datos',
  corto: 'Observatorio',
  ruta: '/observatorio',
  icono: InsightsOutlinedIcon,
  descripcion: 'Indicadores de fuentes oficiales con su serie, su método y su fuente, para sustentar los proyectos.',
  opciones: [
    { etiqueta: 'Panorama', ruta: '/observatorio', icono: SpaceDashboardOutlinedIcon, ayuda: 'Qué hay en el acervo, por tema, y quién produce cada cifra' },
    { etiqueta: 'Catálogo', ruta: '/observatorio?vista=catalogo', icono: ViewListOutlinedIcon, ayuda: 'Todos los indicadores, filtrables por tema, institución y territorio' },
    { etiqueta: 'Comparar', ruta: '/observatorio?vista=comparar', icono: StackedLineChartOutlinedIcon, ayuda: 'Hasta seis series en un mismo eje' },
    { etiqueta: 'Fuentes', ruta: '/observatorio?vista=fuentes', icono: SourceOutlinedIcon, ayuda: 'Las instituciones que publican los datos y los estudios que las citan' },
    { etiqueta: 'Método', ruta: '/observatorio?vista=metodo', icono: ScienceOutlinedIcon, ayuda: 'Cómo llega una cifra al observatorio y qué no se le puede pedir' },
  ],
  cargar: () => import('../../paginas/Observatorio'),
})
