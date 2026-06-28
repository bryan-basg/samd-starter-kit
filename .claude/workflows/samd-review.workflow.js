export const meta = {
  name: 'samd-review',
  description: 'Revisión SaMD del diff de la rama: dimensiones de riesgo en paralelo + verificación adversarial de cada hallazgo',
  phases: [
    { title: 'Review', detail: 'una dimensión de riesgo por agente' },
    { title: 'Verify', detail: 'un escéptico independiente por hallazgo' },
  ],
}

// Dimensiones de riesgo SaMD. Adaptá los prompts a tu dominio clínico.
const DIMENSIONS = [
  {
    key: 'security',
    prompt:
      'Revisá el diff de la rama actual (git diff vs la rama principal) SOLO por vulnerabilidades de seguridad regulatoria: ' +
      'user_id aceptado desde body/query/header (escalada), tracebacks o internals filtrados al cliente, ' +
      'PII/PHI en logs, secretos hardcodeados, claves de cifrado reusadas, falta de validación de audience/issuer del token. ' +
      'Por cada hallazgo: archivo:línea, severidad CVSS, referencia regulatoria (GDPR Art.32 / HIPAA / OWASP).',
  },
  {
    key: 'failsafe',
    prompt:
      'Revisá el diff SOLO por fail-safe clínico (ISO 14971): módulos clínicos que al fallar (red/BD/IA) degradan en silencio, ' +
      'propagan 500 en vez de 503+Retry-After, o exponen el error al usuario en crisis. Por cada hallazgo: archivo:línea + el modo de fallo concreto.',
  },
  {
    key: 'traceability',
    prompt:
      'Revisá el diff SOLO por trazabilidad (IEC 62304 §5.1/§5.7): cambios en algoritmo clínico/schema/seguridad SIN entrada en ' +
      'TECHNICAL_DEBT_SUMMARY ni ISO_14971_RISK_MATRIX, REQ-XXX sin archivo:línea + test real, endpoints cambiados sin regenerar tipos del contrato. ' +
      'Por cada hallazgo: qué doc falta actualizar.',
  },
  {
    key: 'neuro-ux',
    prompt:
      'Revisá el diff SOLO por neuro-UX (WCAG 2.1 AA): contraste fg/bg insuficiente, animaciones que ignoran prefers-reduced-motion, ' +
      'emoji en aria-labels críticos, mensajes de error con jerga técnica, overlays fuera del modal canónico. Por cada hallazgo: archivo:línea.',
  },
]

const FINDINGS_SCHEMA = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          file: { type: 'string' },
          line: { type: 'string' },
          detail: { type: 'string' },
          severity: { type: 'string' },
        },
        required: ['title', 'file', 'detail'],
      },
    },
  },
  required: ['findings'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    isReal: { type: 'boolean' },
    reasoning: { type: 'string' },
  },
  required: ['isReal', 'reasoning'],
}

const results = await pipeline(
  DIMENSIONS,
  (d) => agent(d.prompt, { label: `review:${d.key}`, phase: 'Review', schema: FINDINGS_SCHEMA }),
  (review, dim) =>
    parallel(
      (review?.findings || []).map((f) => () =>
        agent(
          `Intentá REFUTAR este hallazgo de la dimensión "${dim.key}". Default a isReal=false si no podés confirmarlo leyendo el código real. ` +
            `Hallazgo: ${f.title} — ${f.file}:${f.line || '?'} — ${f.detail}`,
          { label: `verify:${f.file}`, phase: 'Verify', schema: VERDICT_SCHEMA }
        ).then((v) => ({ ...f, dimension: dim.key, verdict: v }))
      )
    )
)

const confirmed = results
  .flat()
  .filter(Boolean)
  .filter((f) => f.verdict?.isReal)

log(`Hallazgos confirmados tras verificación adversarial: ${confirmed.length}`)
return { confirmed }
