import { request } from "./client";

export type BudgetItem = {
  row_number: number;
  item: number;
  codigo_apu: string;
  descripcion_apu: string;
  unidad: string;
  cantidad: string;
  material_formula: string | null;
  mano_obra_formula: string | null;
  valor_unitario_formula: string | null;
  valor_total_formula: string | null;
};

export type BudgetListResponse = {
  items: BudgetItem[];
  total: number;
};

export type BudgetAddApuResponse = {
  item: BudgetItem;
  row_number: number;
  backup_path: string;
  formula_integrity_ok: boolean;
};

export type BudgetSaveItemPayload = {
  codigo_apu: string;
  cantidad: string;
};

export type BudgetSaveResponse = {
  sheet_name: string;
  rows: number;
  backup_path: string;
  formula_integrity_ok: boolean;
};

export type BudgetExportResponse = {
  file_name: string;
  file_path: string;
  sheet_name: string;
  rows: number;
  apus: number;
  materials: number;
};

export function listBudgetItems(): Promise<BudgetListResponse> {
  return request<BudgetListResponse>("/budget");
}

export function addApuToBudget(
  codigo_apu: string,
  cantidad = "1",
): Promise<BudgetAddApuResponse> {
  return request<BudgetAddApuResponse>("/budget/apus", {
    method: "POST",
    body: JSON.stringify({ codigo_apu, cantidad }),
  });
}

export function saveBudget(
  items: BudgetSaveItemPayload[],
  sheetName = "PRESUPUESTO",
): Promise<BudgetSaveResponse> {
  return request<BudgetSaveResponse>("/budget/save", {
    method: "POST",
    body: JSON.stringify({ items, sheet_name: sheetName }),
  });
}

export function exportFilteredBudget(
  items: BudgetSaveItemPayload[],
  exportCode: string,
  sheetName = "PRESUPUESTO",
): Promise<BudgetExportResponse> {
  return request<BudgetExportResponse>("/budget/export", {
    method: "POST",
    body: JSON.stringify({
      items,
      sheet_name: sheetName,
      export_code: exportCode,
    }),
  });
}
