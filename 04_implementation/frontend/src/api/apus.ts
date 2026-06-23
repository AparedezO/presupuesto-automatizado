import { request } from "./client";

export type Apu = {
  row_number: number;
  codigo_apu: string;
  descripcion_apu: string;
  unidad: string;
  costo_total_formula: string | null;
};

export type ApuSearchResponse = {
  items: Apu[];
  total: number;
  search: string;
  can_create: boolean;
  suggested_code: string | null;
};

export type ApuItemType = "MATERIAL" | "LABOR" | "CUADRILLA";

export type ApuDetailPayload = {
  tipo_item: ApuItemType;
  codigo_item: string;
  cantidad: string;
  source_row_number?: number | null;
  cantidad_formula?: string | null;
};

export type ApuDraftDetail = ApuDetailPayload & {
  row_number: number;
  source_row_number: number;
  cantidad_formula: string | null;
  descripcion: string | null;
  und: string | null;
  costo: string | null;
};

export type ApuDraftFromBase = {
  base_row_number: number;
  base_codigo_apu: string;
  codigo_apu: string;
  descripcion_apu: string;
  unidad: string;
  detalles: ApuDraftDetail[];
};

export type ApuCreatePayload = {
  codigo_apu: string;
  descripcion_apu: string;
  unidad: string;
  detalles: ApuDetailPayload[];
};

export type ApuCreateResponse = {
  header_row: number;
  detail_rows: number;
  backup_path: string;
  formula_integrity_ok: boolean;
};

export function searchApus(search: string): Promise<ApuSearchResponse> {
  const query = new URLSearchParams({ search, limit: "80" });
  return request<ApuSearchResponse>(`/apus?${query.toString()}`);
}

export function suggestApuCode(description: string): Promise<string> {
  const query = new URLSearchParams({ description });
  return request<{ suggested_code: string }>(
    `/apus/suggest-code?${query.toString()}`,
  ).then((response) => response.suggested_code);
}

export function createApu(payload: ApuCreatePayload): Promise<ApuCreateResponse> {
  return request<ApuCreateResponse>("/apus", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getApuDraft(rowNumber: number): Promise<ApuDraftFromBase> {
  return request<ApuDraftFromBase>(`/apus/${rowNumber}/draft`);
}
