/**
 * El Observatorio de datos SOLO en el navegador (Qhawana): la cáscara mínima de Tiqsi con el módulo web del Observatorio, contra el
 * anfitrión mínimo del backend (qhawana/sola.py). No importa nada de Qillqa. Se construye desde la raíz con
 * `npm run web:construir`.
 */
import { createRoot } from 'react-dom/client'
import { CascaronMinimo } from '@qillqa/tiqsi/minimo'
import { QHAWANA } from './componentes/observatorio/modulo'

createRoot(document.getElementById('root')!).render(<CascaronMinimo modulo={QHAWANA} />)
