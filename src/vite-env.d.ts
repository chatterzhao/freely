/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_FREELY_PROBE_VALIDATION_MODE?: "tauri-smoke";
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
