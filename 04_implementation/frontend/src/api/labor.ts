import { request } from "./client";

export type Labor = {
  row_number: number;
  codigo: string;
  descripcion: string;
  valor_dia: string;
  und: string;
  valor_hora_formula: string | null;
};

export type LaborSearchResponse = {
  items: Labor[];
  total: number;
  search: string;
  can_create: boolean;
};

export type LaborCreatePayload = {
  codigo: string;
  descripcion: string;
  valor_dia: string;
  und: string;
};

export function searchLabor(search: string): Promise<LaborSearchResponse> {
  const query = new URLSearchParams({ search, limit: "8" });
  return request<LaborSearchResponse>(`/labor?${query.toString()}`);
}

export function createLabor(payload: LaborCreatePayload): Promise<void> {
  return request<void>("/labor", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
