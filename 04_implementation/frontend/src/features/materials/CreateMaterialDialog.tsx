import * as Dialog from "@radix-ui/react-dialog";
import { Loader2, Save, X } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";

import {
  MaterialCreatePayload,
  createMaterial,
  suggestMaterialCode,
} from "../../api/materials";
import { useMaterialsStore } from "../../store/materialsStore";

type Props = {
  onCreated: () => void;
};

export function CreateMaterialDialog({ onCreated }: Props) {
  const { isCreateOpen, closeCreate, draft, updateDraft, resetDraft } =
    useMaterialsStore();
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isCreateOpen || !draft.descripcion || draft.codigo) {
      return;
    }

    const timeout = window.setTimeout(() => {
      suggestMaterialCode(draft.descripcion)
        .then((codigo) => updateDraft({ codigo }))
        .catch(() => undefined);
    }, 300);

    return () => window.clearTimeout(timeout);
  }, [draft.codigo, draft.descripcion, isCreateOpen, updateDraft]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSaving(true);
    setError(null);
    setMessage(null);

    const payload: MaterialCreatePayload = {
      codigo: draft.codigo.trim(),
      descripcion: draft.descripcion.trim(),
      marca: draft.marca.trim() || null,
      und: draft.und.trim() || "UN",
      factor: percentageToDecimal(draft.factor),
      valor_costo_incluido_iva: draft.valor_costo_incluido_iva || "0",
    };

    try {
      const result = await createMaterial(payload);
      setMessage(
        `Material guardado en fila ${result.row_number}. Formulas preservadas.`,
      );
      resetDraft();
      onCreated();
      window.setTimeout(() => {
        setMessage(null);
        closeCreate();
      }, 900);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Error inesperado.");
    } finally {
      setIsSaving(false);
    }
  }

  function percentageToDecimal(value: string) {
    const cleaned = value.replace("%", "").replace(",", ".").trim();
    const parsed = Number(cleaned);
    if (!Number.isFinite(parsed)) {
      return "0";
    }
    return String(parsed / 100);
  }

  return (
    <Dialog.Root open={isCreateOpen} onOpenChange={(open) => !open && closeCreate()}>
      <Dialog.Portal>
        <Dialog.Overlay className="dialogOverlay" />
        <Dialog.Content className="dialogContent">
          <div className="dialogHeader">
            <div>
              <Dialog.Title className="dialogTitle">Crear material</Dialog.Title>
              <Dialog.Description className="dialogDescription">
                Se agregara al Excel copiando formulas de la fila anterior.
              </Dialog.Description>
            </div>
            <Dialog.Close className="iconButton" aria-label="Cerrar">
              <X size={18} />
            </Dialog.Close>
          </div>

          <form className="materialForm" onSubmit={handleSubmit}>
            <label className="field">
              <span>Descripcion</span>
              <input
                required
                value={draft.descripcion}
                onChange={(event) =>
                  updateDraft({ descripcion: event.target.value, codigo: "" })
                }
                placeholder="Ej. Tubo PVC 3/4"
              />
            </label>

            <label className="field">
              <span>Codigo sugerido</span>
              <input
                required
                value={draft.codigo}
                onChange={(event) => updateDraft({ codigo: event.target.value })}
                placeholder="TUBO-PVC-3/4"
              />
            </label>

            <div className="formGrid">
              <label className="field">
                <span>Marca</span>
                <input
                  value={draft.marca}
                  onChange={(event) => updateDraft({ marca: event.target.value })}
                  placeholder="Opcional"
                />
              </label>

              <label className="field">
                <span>Unidad</span>
                <input
                  required
                  value={draft.und}
                  onChange={(event) => updateDraft({ und: event.target.value })}
                  placeholder="UN"
                />
              </label>
            </div>

            <div className="formGrid">
              <label className="field">
                <span>Factor (%)</span>
                <input
                  inputMode="decimal"
                  value={draft.factor}
                  onChange={(event) => updateDraft({ factor: event.target.value })}
                  placeholder="20"
                />
              </label>

              <label className="field">
                <span>Costo con IVA</span>
                <input
                  inputMode="decimal"
                  value={draft.valor_costo_incluido_iva}
                  onChange={(event) =>
                    updateDraft({ valor_costo_incluido_iva: event.target.value })
                  }
                  placeholder="0"
                />
              </label>
            </div>

            {error ? <p className="formError">{error}</p> : null}
            {message ? <p className="formSuccess">{message}</p> : null}

            <div className="dialogActions">
              <button className="secondaryButton" type="button" onClick={closeCreate}>
                Cancelar
              </button>
              <button className="primaryButton" type="submit" disabled={isSaving}>
                {isSaving ? <Loader2 className="spin" size={17} /> : <Save size={17} />}
                Guardar
              </button>
            </div>
          </form>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
