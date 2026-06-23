import { create } from "zustand";

export type MaterialDraft = {
  codigo: string;
  descripcion: string;
  marca: string;
  und: string;
  factor: string;
  valor_costo_incluido_iva: string;
};

type MaterialsState = {
  isCreateOpen: boolean;
  draft: MaterialDraft;
  openCreate: (description?: string, suggestedCode?: string | null) => void;
  closeCreate: () => void;
  updateDraft: (patch: Partial<MaterialDraft>) => void;
  resetDraft: () => void;
};

const emptyDraft: MaterialDraft = {
  codigo: "",
  descripcion: "",
  marca: "",
  und: "UN",
  factor: "20",
  valor_costo_incluido_iva: "0",
};

export const useMaterialsStore = create<MaterialsState>((set) => ({
  isCreateOpen: false,
  draft: emptyDraft,
  openCreate: (description = "", suggestedCode = null) =>
    set((state) => ({
      isCreateOpen: true,
      draft: {
        ...state.draft,
        descripcion: state.draft.descripcion || description,
        codigo: state.draft.codigo || suggestedCode || "",
      },
    })),
  closeCreate: () => set({ isCreateOpen: false }),
  updateDraft: (patch) =>
    set((state) => ({
      draft: { ...state.draft, ...patch },
    })),
  resetDraft: () => set({ draft: emptyDraft }),
}));
