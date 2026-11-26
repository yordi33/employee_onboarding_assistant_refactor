# Employee Onboarding Assistant — Bridge SA

Copiloto que acompaña a los empleados nuevos de **Bridge SA** (empresa ficticia) durante sus primeros días. Responde dudas apoyándose en documentación interna, genera checklists diarias en JSON y sabe cuándo derivar a People, IT o al manager/buddy del empleado.

Proyecto desarrollado como parte del bootcamp, integrando: Prompt & Context Engineering, Assistant Engineering & Robustez, y evaluación/benchmark de modelos.

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Arquitectura](#-arquitectura)
- [Instalación y configuración](#-instalación-y-configuración)
- [Ejecución de las demos](#-ejecución-de-las-demos)
- [Estrategia de selección de contexto](#-estrategia-de-selección-de-contexto)
- [Robustez y seguridad](#-robustez-y-seguridad)
- [Benchmark y elección de modelo](#-benchmark-y-elección-de-modelo)
- [Flujo de trabajo del equipo](#-flujo-de-trabajo-del-equipo)

## 🎯 Funcionalidades

1. **Conversación (chat)**: el empleado pregunta libremente y el asistente responde en texto, citando documentación relevante y manteniendo hasta 4 turnos de historial.
2. **Checklist de la semana 1 (JSON)**: dado un empleado y un día de onboarding (1–5), el asistente devuelve un plan estructurado de tareas, cada una justificada con su documento fuente.

Ambas funcionalidades tienen en cuenta el **día de onboarding** (1–5) y el **perfil del empleado** (dev junior, comercial, remoto UE) para ajustar tono y contenido.

## 🏗 Arquitectura

Arquitectura modular por responsabilidades, sin script monolítico. Cada fichero tiene una única responsabilidad:

| Fichero | Responsabilidad |
|---|---|
| `config.py` | Centralización de constantes, límites, mensajes de error y rutas globales |
| `gemini_auth.py` | Carga y validación de credenciales (`GEMINI_API_KEY`) |
| `gemini_client.py` | Cliente del LLM: llamadas a la API, parámetros del modelo |
| `context.py` | Selección de contexto: filtrado de docs/FAQ, truncado, historial acotado |
| `prompts.py` | Construcción de prompts dinámicos (system prompt, delimitadores) |
| `validators.py` | Validación de entrada y reglas fail-closed (Parte 3) |
| `logic.py` | Lógica de negocio: orquesta chat y generación del checklist JSON |
| `state.py` | Estado del empleado (perfil, día de onboarding, historial) |
| `benchmark.py` | Ejecución del benchmark comparando modelos (Parte 4) |
| `main.py` | Demos ejecutables de principio a fin |

El flujo de ejecución está orquestado por `logic.py`. Cuando entra una solicitud, se valida primero en `validators.py`; si pasa la validación, `context.py` recupera los datos necesarios que luego se formatean en `prompts.py` para finalmente invocar al LLM mediante `gemini_client.py`.

.├── data/                     # Datos de partida (lore, docs, FAQ, empleados, casos trampa)├── docs/                     # Documentación adicional (política de escalado, etc.)│   └── politica-escalado.md├── entregables/               # Plantillas de entrega (matriz de decisión, rúbrica, recomendación)├── output/                    # Resultados del benchmark (CSV, informe) — Parte 4├── config.py                  # Variables globales del sistema├── gemini_auth.py├── gemini_client.py├── context.py├── prompts.py├── validators.py├── logic.py├── state.py├── benchmark.py├── main.py                    # Demos ejecutables├── requirements.txt├── .env.example└── README.md
## ⚙️ Instalación y configuración

### Requisitos previos

- Python 3.10+
- Una API key de Google AI Studio (`GEMINI_API_KEY`)

### Pasos

```bash
# 1. Clonar el repositorio
git clone [https://github.com/Mariamd30/employee_onboarding_assistant](https://github.com/Mariamd30/employee_onboarding_assistant)
cd employee-onboarding-assistant

# 2. Crear y activar entorno virtual
py -m venv .venv
source .venv/bin/activate       # Mac/Linux
.venv\Scripts\activate          # Windows
source .venv/Scripts/activate   # Windows (Git Bash)

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env y añadir vuestra GEMINI_API_KEY real
Nunca subáis vuestro .env con claves reales al repositorio. Está incluido en .gitignore.▶️ Ejecución de las demosBashpython main.py
El script ejecuta de forma secuencial:Demo 1: conversación de 1 turno (empleado dev junior).Demo 2: checklist JSON para el día 1.Demo 3: mismo mensaje con empleado comercial vs remoto UE (respuestas distintas).Demo 4: comparación interactiva entre el modo vulnerable y seguro (casos trampa).🧠 Estrategia de selección de contextoEstrategia de recuperación de contexto:Máximo 3 documentos por turno.Máximo 2 FAQ por turno.Filtrado y priorización por departamento del empleado.Coincidencia y puntuación por palabras clave y tags relevantes.Historial limitado a los últimos 4 turnos de conversación.🔒 Robustez y seguridadPrincipio rector: fail-closed — si la validación de entrada falla, se rechaza la petición de inmediato sin consumir tokens ni llamar al modelo.El asistente SÍ ayuda con:Herramientas corporativas y primeros pasosCultura de Bridge SAVacaciones según documentaciónA quién contactar / cómo escalarEl asistente NO debe:Inventar políticas, plazos o cifras no documentadasResponder sobre salarios o datos de otros empleadosAtender a participantes externos de los programas formativosPara evaluar la seguridad, implementamos una comparativa ejecutable entre la lógica vulnerable y la lógica segura (fail-closed) utilizando el set de pruebas almacenado en data/casos_trampa.json. Puedes ver los detalles sobre la política de escalado acordada en docs/politica-escalado.md.📊 Benchmark y elección de modeloEl sistema incluye un motor de evaluación automatizado (benchmark.py) que compara el comportamiento y rendimiento de los modelos definidos. Al ejecutar las pruebas, los datos brutos se exportan en formato CSV y se genera un reporte resumido en Markdown dentro del directorio output/.Las decisiones de ingeniería resultantes y la justificación del modelo seleccionado están detalladas en los documentos de la carpeta entregables/.👥 EquipoDesarrollador/aMaría Muriel DelgadoJavier CorchadoYordanos Lopez DiazAlejandro Dietta Martin🔀 Flujo de trabajo del equipoRamas: main (estable) ← develop (integración) ← feature/* (trabajo individual)Commits siguiendo Conventional Commits (feat:, fix:, docs:, refactor:, chore:)Toda PR requiere al menos 1 revisión aprobada antes de mergearReparto de partes:ParteResponsableSetup + Parte 1 (contexto y datos)Alejandro Dietta / Maria MurielParte 2 · Track A — Cliente y estado (gemini_auth.py, gemini_client.py, state.py)Alejandro DiettaParte 2 · Track B — Contenido y reglas (context.py, prompts.py, validators.py)Maria MurielParte 2 · Integración (logic.py, main.py)Alejandro Dietta / Maria MurielParte 3 (robustez)Javier CorchadoParte 4 (benchmark)Maria Muriel
---

Guarda los cambios en el `README.md` y ¡listo! Ya habremos terminado con los cambios en los archiv