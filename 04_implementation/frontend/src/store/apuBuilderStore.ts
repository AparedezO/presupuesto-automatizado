import { create } from "zustand";

import { ApuDraftFromBase, ApuItemType } from "../api/apus";

export type ApuDetailDraft = {
  id: string;
  tipo_item: ApuItemType;
  codigo_item: string;
  cantidad: string;
  source_row_number?: number | null;
  cantidad_formula?: string | null;
  descripcion?: string;
  und?: string;
  costo?: string;
};

export type ApuBuilderDraft = {
  codigo_apu: string;
  descripcion_apu: string;
  unidad: string;
  detalles: ApuDetailDraft[];
};

type ApuBuilderState = {
  draft: ApuBuilderDraft;
  setHeader: (patch: Partial<Omit<ApuBuilderDraft, "detalles">>) => void;
  startFromSearch: (description: string, suggestedCode?: string | null) => void;
  startFromBase: (
    base: ApuDraftFromBase,
    descriptionOverride?: string,
    suggestedCode?: string | null,
  ) => void;
  addDetail: (tipo_item?: ApuItemType) => void;
  addMaterialDetail: (
    codigo_item: string,
    cantidad: string,
    display?: Pick<ApuDetailDraft, "descripcion" | "und" | "costo">,
  ) => void;
  updateDetail: (id: string, patch: Partial<ApuDetailDraft>) => void;
  removeDetail: (id: string) => void;
  resetBuilder: () => void;
};

const createDetail = (tipo_item: ApuItemType = "MATERIAL"): ApuDetailDraft => ({
  id: crypto.randomUUID(),
  tipo_item,
  codigo_item: "",
  cantidad: "1",
});

const emptyDraft: ApuBuilderDraft = {
  codigo_apu: "",
  descripcion_apu: "",
  unidad: "UN",
  detalles: [],
};

export const useApuBuilderStore = create<ApuBuilderState>((set) => ({
  draft: emptyDraft,
  setHeader: (patch) =>
    set((state) => ({
      draft: { ...state.draft, ...patch },
    })),
  startFromSearch: (description, suggestedCode = null) =>
    set((state) => ({
      draft: {
        ...state.draft,
        descripcion_apu: state.draft.descripcion_apu || description,
        codigo_apu: state.draft.codigo_apu || suggestedCode || "",
      },
    })),
  startFromBase: (base, descriptionOverride = "", suggestedCode = null) =>
    set({
      draft: {
        codigo_apu: suggestedCode || "",
        descripcion_apu: descriptionOverride.trim() || base.descripcion_apu,
        unidad: base.unidad || "UN",
        detalles: base.detalles.map((detail) => ({
          id: crypto.randomUUID(),
          tipo_item: "MATERIAL",
          codigo_item: detail.codigo_item,
          cantidad: String(detail.cantidad || "1"),
          source_row_number: detail.source_row_number,
          cantidad_formula: detail.cantidad_formula,
          descripcion: detail.descripcion || undefined,
          und: detail.und || undefined,
          costo: detail.costo || undefined,
        })),
      },
    }),
  addDetail: (tipo_item = "MATERIAL") =>
    set((state) => ({
      draft: {
        ...state.draft,
        detalles: [...state.draft.detalles, createDetail(tipo_item)],
      },
    })),
  addMaterialDetail: (codigo_item, cantidad, display = {}) =>
    set((state) => ({
      draft: {
        ...state.draft,
        detalles: [
          ...state.draft.detalles,
          {
            ...createDetail("MATERIAL"),
            codigo_item,
            cantidad,
            ...display,
          },
        ],
      },
    })),
  updateDetail: (id, patch) =>
    set((state) => ({
      draft: {
        ...state.draft,
        detalles: state.draft.detalles.map((detail) =>
          detail.id === id ? { ...detail, ...patch } : detail,
        ),
      },
    })),
  removeDetail: (id) =>
    set((state) => {
      const detalles = state.draft.detalles.filter((detail) => detail.id !== id);
      return {
        draft: {
          ...state.draft,
          detalles: detalles.length ? detalles : [createDetail()],
        },
      };
    }),
  resetBuilder: () =>
    set({
      draft: {
        ...emptyDraft,
        detalles: [],
      },
    }),
}));
