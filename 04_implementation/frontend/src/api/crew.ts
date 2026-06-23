import { request } from "./client";

export type Crew = {
  row_number: number;
  codigo: string;
  descripcion: string;
  valor_dia: string;
  disponibilidad: string | null;
  valor_hora_formula: string | null;
};

export type CrewSearchResponse = {
  items: Crew[];
  total: number;
  search: string;
  can_create: boolean;
};

export function searchCrew(search: string): Promise<CrewSearchResponse> {
  const query = new URLSearchParams({ search, limit: "8" });
  return request<CrewSearchResponse>(`/crew?${query.toString()}`);
}
