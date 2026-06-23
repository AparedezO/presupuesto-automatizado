import { request } from "./client";

export type Material = {
  row_number: number;
  codigo: string;
  descripcion: string;
  marca: string | null;
  und: string;
  factor: string;
  valor_costo_incluido_iva: string;
  valor_presupuesto_formula: string | null;
};

export type MaterialsSearchResponse = {
  items: Material[];
  total: number;
  search: string;
  can_create: boolean;
  suggested_code: string | null;
};

export type MaterialCreatePayload = {
  codigo: string;
  descripcion: string;
  marca?: string | null;
  und: string;
  factor: string;
  valor_costo_incluido_iva: string;
};

export type MaterialCreateResponse = {
  material: Material;
  row_number: number;
  backup_path: string;
  added_formulas: number;
  formula_integrity_ok: boolean;
};

export function searchMaterials(search: string): Promise<MaterialsSearchResponse> {
  const query = new URLSearchParams({ search, limit: "80" });
  return request<MaterialsSearchResponse>(`/materials?${query.toString()}`);
}

export function suggestMaterialCode(description: string): Promise<string> {
  const query = new URLSearchParams({ description });
  return request<{ suggested_code: string }>(
    `/materials/suggest-code?${query.toString()}`,
  ).then((response) => response.suggested_code);
}

export function createMaterial(
  payload: MaterialCreatePayload,
): Promise<MaterialCreateResponse> {
  return request<MaterialCreateResponse>("/materials", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
