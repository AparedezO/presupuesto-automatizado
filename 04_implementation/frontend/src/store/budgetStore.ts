import { create } from "zustand";

import { Apu } from "../api/apus";

export type BudgetDraftItem = {
  id: string;
  codigo_apu: string;
  descripcion_apu: string;
  unidad: string;
  cantidad: string;
};

type BudgetState = {
  items: BudgetDraftItem[];
  addApu: (apu: Apu, cantidad?: string) => void;
  updateQuantity: (id: string, cantidad: string) => void;
  removeItem: (id: string) => void;
  clearBudget: () => void;
};

export const useBudgetStore = create<BudgetState>((set) => ({
  items: [],
  addApu: (apu, cantidad = "1") =>
    set((state) => ({
      items: [
        ...state.items,
        {
          id: crypto.randomUUID(),
          codigo_apu: apu.codigo_apu,
          descripcion_apu: apu.descripcion_apu,
          unidad: apu.unidad,
          cantidad,
        },
      ],
    })),
  updateQuantity: (id, cantidad) =>
    set((state) => ({
      items: state.items.map((item) =>
        item.id === id ? { ...item, cantidad } : item,
      ),
    })),
  removeItem: (id) =>
    set((state) => ({
      items: state.items.filter((item) => item.id !== id),
    })),
  clearBudget: () => set({ items: [] }),
}));
