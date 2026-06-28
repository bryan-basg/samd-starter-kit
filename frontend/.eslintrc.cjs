// ============================================================================
// ESLint — {{PROJECT_NAME}} frontend (SaMD {{SAMD_CLASS}})
// IEC 62304 §5.7 — mantenibilidad verificable. Prohibido `any`; archivos y
// funciones acotados; imports canónicos forzados.
// ============================================================================
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', 'build', 'node_modules', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: [],
  rules: {
    // --- Tipado: prohibido `any` en producción ------------------------------
    '@typescript-eslint/no-explicit-any': 'error',

    // --- Vars sin usar: prefijo `_` = descarte intencional -------------------
    'no-unused-vars': 'off',
    '@typescript-eslint/no-unused-vars': ['warn', {
      argsIgnorePattern: '^_',
      varsIgnorePattern: '^_',
      caughtErrorsIgnorePattern: '^_',
      destructuredArrayIgnorePattern: '^_',
    }],
    '@typescript-eslint/ban-ts-comment': 'off',

    // --- Mantenibilidad (§5.7): tamaño y complejidad acotados ----------------
    // `warn` (no `error`) a propósito: deuda legacy se baja incremental sin
    // romper el build de golpe. Subir a `error` cuando esté saldada.
    'max-lines': ['warn', { max: 500, skipBlankLines: true, skipComments: true }],
    'max-lines-per-function': ['warn', { max: 80, skipBlankLines: true, skipComments: true }],
    'complexity': ['warn', 15],

    // --- Imports canónicos: forzar el wrapper del proyecto -------------------
    // Patrón: una librería se usa SOLO a través de un wrapper interno (anti-flood,
    // anti-drift, consentimiento, etc.). Reemplazar el placeholder por el real.
    'no-restricted-imports': ['error', {
      paths: [{
        name: '<some-third-party-lib>',
        importNames: ['default', '<bannedExport>'],
        message: 'Importá desde "@/<services/canonicalWrapper>" en su lugar (wrapper canónico del proyecto).',
      }],
    }],
  },
  overrides: [
    {
      // Tests/stories/scripts: `any` deliberado en mocks; imports directos
      // legítimos (vi.mock del módulo real). Se relajan SOLO aquí; producción
      // mantiene la protección de los rules de arriba.
      files: [
        '**/__tests__/**/*.{ts,tsx}',
        '**/*.test.{ts,tsx}',
        '**/*.stories.{ts,tsx}',
        'src/setupTests.{ts,tsx}',
        'e2e/**/*.{ts,tsx}',
        'scripts/**/*.ts',
      ],
      rules: {
        '@typescript-eslint/no-explicit-any': 'off',
        'no-restricted-imports': 'off',
        'max-lines': 'off',
        'max-lines-per-function': 'off',
      },
    },
  ],
};
