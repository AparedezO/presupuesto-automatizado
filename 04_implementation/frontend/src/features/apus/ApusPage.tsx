import * as Dialog from "@radix-ui/react-dialog";
import {
  FileSpreadsheet,
  Loader2,
  Minus,
  PencilLine,
  Plus,
  Save,
  Search,
  Trash2,
  X,
} from "lucide-react";
import { FormEvent, useEffect, useMemo, useState } from "react";

import {
  Apu,
  createApu,
  getApuDraft,
  searchApus,
  suggestApuCode,
} from "../../api/apus";
import {
  Material,
  createMaterial,
  searchMaterials,
  suggestMaterialCode,
} from "../../api/materials";
import {
  ApuDetailDraft,
  useApuBuilderStore,
} from "../../store/apuBuilderStore";
import { useBudgetStore } from "../../store/budgetStore";

type LookupItem = {
  codigo: string;
  descripcion: string;
  und: string;
  costo: string;
};

type InlineDialogRequest = {
  initialDescription: string;
  cantidad: string;
};

function formatCurrency(value: string) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    return value || "-";
  }

  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  }).format(parsed);
}

function mapMaterial(material: Material): LookupItem {
  return {
    codigo: material.codigo,
    descripcion: material.descripcion,
    und: material.und,
    costo: material.valor_costo_incluido_iva,
  };
}

function ApuCard({
  apu,
  onAdd,
  onEditAsNew,
  isEditingAsNew,
}: {
  apu: Apu;
  onAdd: (apu: Apu) => void;
  onEditAsNew: (apu: Apu) => void;
  isEditingAsNew: boolean;
}) {
  return (
    <article className="materialCard">
      <div className="materialCardHeader">
        <strong>{apu.codigo_apu}</strong>
        <span>{apu.unidad}</span>
      </div>
      <p>{apu.descripcion_apu}</p>
      <dl>
        <div>
          <dt>Fila</dt>
          <dd>{apu.row_number}</dd>
        </div>
        <div>
          <dt>Costo total</dt>
          <dd>{apu.costo_total_formula || "-"}</dd>
        </div>
      </dl>
      <div className="cardActions">
        <button className="secondaryButton cardAction" type="button" onClick={() => onAdd(apu)}>
          <Plus size={16} />
          Agregar APU
        </button>
        <button
          className="secondaryButton cardAction"
          type="button"
          onClick={() => onEditAsNew(apu)}
          disabled={isEditingAsNew}
        >
          {isEditingAsNew ? <Loader2 className="spin" size={16} /> : <PencilLine size={16} />}
          Editar como nuevo
        </button>
      </div>
    </article>
  );
}
function normalizeQuantity(value: string) {
  const parsed = Number(value.replace(",", "."));
  if (!Number.isFinite(parsed)) {
    return 0;
  }
  return Math.max(0, parsed);
}

function stepQuantity(value: string, delta: number) {
  return String(Math.max(0, normalizeQuantity(value) + delta));
}

function QuantityStepper({
  value,
  onChange,
}: {
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <div className="quantityStepper">
      <button type="button" onClick={() => onChange(stepQuantity(value, -1))}>
        <Minus size={15} />
      </button>
      <input
        inputMode="decimal"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
      <button type="button" onClick={() => onChange(stepQuantity(value, 1))}>
        <Plus size={15} />
      </button>
    </div>
  );
}

function AddedMaterialsTable({ details }: { details: ApuDetailDraft[] }) {
  const updateDetail = useApuBuilderStore((state) => state.updateDetail);
  const removeDetail = useApuBuilderStore((state) => state.removeDetail);

  return (
    <div className="apuMaterialsTableWrap">
      {details.length ? (
        <table className="materialsTable apuMaterialsTable">
          <thead>
            <tr>
              <th>Codigo</th>
              <th>Material</th>
              <th>UND</th>
              <th>Costo</th>
              <th>Cantidad</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {details.map((detail) => (
              <tr key={detail.id}>
                <td>{detail.codigo_item}</td>
                <td>{detail.descripcion || "Material agregado"}</td>
                <td>{detail.und || "-"}</td>
                <td>{detail.costo ? formatCurrency(detail.costo) : "-"}</td>
                <td>
                  <QuantityStepper
                    value={detail.cantidad}
                    onChange={(cantidad) =>
                      updateDetail(detail.id, {
                        cantidad,
                        cantidad_formula: null,
                        source_row_number: null,
                      })
                    }
                  />
                  {detail.cantidad_formula ? (
                    <small className="formulaHint">Formula del APU base</small>
                  ) : null}
                </td>
                <td>
                  <button
                    className="iconButton"
                    type="button"
                    onClick={() => removeDetail(detail.id)}
                    aria-label="Quitar material"
                  >
                    <Trash2 size={17} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}

      {!details.length ? (
        <p className="emptyState compact">Agrega materiales para construir el APU.</p>
      ) : null}
    </div>
  );
}
function InlineItemDialog({
  request,
  onClose,
  onCreated,
}: {
  request: InlineDialogRequest | null;
  onClose: () => void;
  onCreated: (material: LookupItem, cantidad: string) => void;
}) {
  const [codigo, setCodigo] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [marca, setMarca] = useState("");
  const [und, setUnd] = useState("UN");
  const [factor, setFactor] = useState("20");
  const [costo, setCosto] = useState("0");
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!request) {
      return;
    }

    setDescripcion(request.initialDescription);
    setCodigo("");
    setMarca("");
    setUnd("UN");
    setFactor("20");
    setCosto("0");
    setError(null);
    setMessage(null);
  }, [request]);

  useEffect(() => {
    if (!request || !descripcion.trim() || codigo.trim()) {
      return;
    }

    const timeout = window.setTimeout(() => {
      suggestMaterialCode(descripcion)
        .then(setCodigo)
        .catch(() => undefined);
    }, 250);

    return () => window.clearTimeout(timeout);
  }, [codigo, descripcion, request]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!request) {
      return;
    }

    setIsSaving(true);
    setError(null);
    setMessage(null);

    try {
      const result = await createMaterial({
        codigo: codigo.trim(),
        descripcion: descripcion.trim(),
        marca: marca.trim() || null,
        und: und.trim() || "UN",
        factor: String(Number(factor.replace("%", "").replace(",", ".")) / 100 || 0),
        valor_costo_incluido_iva: costo || "0",
      });

      setMessage("Insumo creado. El APU en progreso se conserva.");
      onCreated(mapMaterial(result.material), request.cantidad);
      window.setTimeout(onClose, 600);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Error inesperado.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <Dialog.Root open={Boolean(request)} onOpenChange={(open) => !open && onClose()}>
      <Dialog.Portal>
        <Dialog.Overlay className="dialogOverlay" />
        <Dialog.Content className="dialogContent">
          <div className="dialogHeader">
            <div>
              <Dialog.Title className="dialogTitle">
                Crear material
              </Dialog.Title>
              <Dialog.Description className="dialogDescription">
                Se registra sin perder la cabecera ni detalles del APU actual.
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
                value={descripcion}
                onChange={(event) => {
                  setDescripcion(event.target.value);
                  setCodigo("");
                }}
              />
            </label>

            <label className="field">
              <span>Codigo sugerido</span>
              <input required value={codigo} onChange={(event) => setCodigo(event.target.value)} />
            </label>

            <div className="formGrid">
              <label className="field">
                <span>Marca</span>
                <input value={marca} onChange={(event) => setMarca(event.target.value)} />
              </label>

              <label className="field">
                <span>Unidad</span>
                <input required value={und} onChange={(event) => setUnd(event.target.value)} />
              </label>
            </div>

            <div className="formGrid">
              <label className="field">
                <span>Factor (%)</span>
                <input
                  inputMode="decimal"
                  value={factor}
                  onChange={(event) => setFactor(event.target.value)}
                />
              </label>

              <label className="field">
                <span>Costo con IVA</span>
                <input
                  inputMode="decimal"
                  value={costo}
                  onChange={(event) => setCosto(event.target.value)}
                />
              </label>
            </div>

            {error ? <p className="formError">{error}</p> : null}
            {message ? <p className="formSuccess">{message}</p> : null}

            <div className="dialogActions">
              <button className="secondaryButton" type="button" onClick={onClose}>
                Cancelar
              </button>
              <button className="primaryButton" type="submit" disabled={isSaving}>
                {isSaving ? <Loader2 className="spin" size={17} /> : <Save size={17} />}
                Guardar insumo
              </button>
            </div>
          </form>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

export function ApusPage() {
  const [search, setSearch] = useState("");
  const [apus, setApus] = useState<Apu[]>([]);
  const [total, setTotal] = useState(0);
  const [canCreate, setCanCreate] = useState(false);
  const [suggestedCode, setSuggestedCode] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [builderError, setBuilderError] = useState<string | null>(null);
  const [builderMessage, setBuilderMessage] = useState<string | null>(null);
  const [budgetMessage, setBudgetMessage] = useState<string | null>(null);
  const [inlineRequest, setInlineRequest] = useState<InlineDialogRequest | null>(null);
  const [materialSearch, setMaterialSearch] = useState("");
  const [materialQuantity, setMaterialQuantity] = useState("1");
  const [materialResults, setMaterialResults] = useState<LookupItem[]>([]);
  const [selectedMaterial, setSelectedMaterial] = useState<LookupItem | null>(null);
  const [materialCanCreate, setMaterialCanCreate] = useState(false);
  const [materialStatus, setMaterialStatus] = useState("");
  const [isMaterialLookupLoading, setIsMaterialLookupLoading] = useState(false);
  const [editingBaseRow, setEditingBaseRow] = useState<number | null>(null);

  const draft = useApuBuilderStore((state) => state.draft);
  const setHeader = useApuBuilderStore((state) => state.setHeader);
  const startFromSearch = useApuBuilderStore((state) => state.startFromSearch);
  const startFromBase = useApuBuilderStore((state) => state.startFromBase);
  const addMaterialDetail = useApuBuilderStore((state) => state.addMaterialDetail);
  const resetBuilder = useApuBuilderStore((state) => state.resetBuilder);
  const addApuToDraftBudget = useBudgetStore((state) => state.addApu);

  const validDetails = useMemo(
    () => draft.detalles.filter((detail) => detail.codigo_item.trim()),
    [draft.detalles],
  );

  const budgetCandidate = useMemo(() => {
    const normalizedSearch = search.trim().toUpperCase();
    if (!normalizedSearch) {
      return null;
    }
    const exact = apus.find(
      (apu) =>
        apu.codigo_apu.toUpperCase() === normalizedSearch ||
        apu.descripcion_apu.toUpperCase() === normalizedSearch,
    );
    if (exact) {
      return exact;
    }
    return apus.length === 1 ? apus[0] : null;
  }, [apus, search]);

  function loadApus(value = search) {
    setIsLoading(true);
    setError(null);
    searchApus(value)
      .then((response) => {
        setApus(response.items);
        setTotal(response.total);
        setCanCreate(response.can_create);
        setSuggestedCode(response.suggested_code);
      })
      .catch((caught) =>
        setError(caught instanceof Error ? caught.message : "Error inesperado."),
      )
      .finally(() => setIsLoading(false));
  }

  useEffect(() => {
    const timeout = window.setTimeout(() => loadApus(search), 250);
    return () => window.clearTimeout(timeout);
  }, [search]);

  useEffect(() => {
    if (!draft.descripcion_apu.trim() || draft.codigo_apu.trim()) {
      return;
    }

    const timeout = window.setTimeout(() => {
      suggestApuCode(draft.descripcion_apu)
        .then((codigo) => setHeader({ codigo_apu: codigo }))
        .catch(() => undefined);
    }, 250);

    return () => window.clearTimeout(timeout);
  }, [draft.codigo_apu, draft.descripcion_apu, setHeader]);

  useEffect(() => {
    const term = materialSearch.trim();

    if (!term) {
      setMaterialResults([]);
      setMaterialCanCreate(false);
      setMaterialStatus("");
      return;
    }

    if (selectedMaterial?.codigo === term) {
      setMaterialResults([]);
      setMaterialCanCreate(false);
      setMaterialStatus("Material seleccionado");
      return;
    }

    const timeout = window.setTimeout(async () => {
      setIsMaterialLookupLoading(true);
      setMaterialStatus("Buscando material...");

      try {
        const response = await searchMaterials(term);
        const mapped = response.items.slice(0, 8).map(mapMaterial);
        setMaterialResults(mapped);
        setMaterialCanCreate(response.can_create);
        setMaterialStatus(
          mapped.length ? `${mapped.length} coincidencias` : "Sin coincidencias",
        );
      } catch (caught) {
        setMaterialResults([]);
        setMaterialCanCreate(false);
        setMaterialStatus(caught instanceof Error ? caught.message : "Error al buscar.");
      } finally {
        setIsMaterialLookupLoading(false);
      }
    }, 250);

    return () => window.clearTimeout(timeout);
  }, [materialSearch, selectedMaterial]);

  function clearMaterialPicker(message = "") {
    setMaterialSearch("");
    setMaterialQuantity("1");
    setMaterialResults([]);
    setSelectedMaterial(null);
    setMaterialCanCreate(false);
    setMaterialStatus(message);
  }

  function selectMaterial(material: LookupItem) {
    setSelectedMaterial(material);
    setMaterialSearch(material.codigo);
    setMaterialResults([]);
    setMaterialCanCreate(false);
    setMaterialStatus("Material seleccionado");
  }

  function handleAddMaterial() {
    if (!selectedMaterial) {
      setBuilderError("Selecciona un material antes de agregarlo a la tabla.");
      return;
    }

    addMaterialDetail(selectedMaterial.codigo, materialQuantity || "1", {
      descripcion: selectedMaterial.descripcion,
      und: selectedMaterial.und,
      costo: selectedMaterial.costo,
    });
    setBuilderError(null);
    clearMaterialPicker("Material agregado. Busca el siguiente.");
  }

  function handleCreatedMaterial(material: LookupItem, cantidad: string) {
    addMaterialDetail(material.codigo, cantidad || "1", {
      descripcion: material.descripcion,
      und: material.und,
      costo: material.costo,
    });
    clearMaterialPicker("Material creado y agregado. Busca el siguiente.");
  }

  function handleStartCreate(description = search, code = suggestedCode) {
    startFromSearch(description.trim(), code);
    window.setTimeout(() => {
      document.getElementById("apu-builder")?.scrollIntoView({ behavior: "smooth" });
    }, 50);
  }

  async function handleEditAsNew(apu: Apu) {
    setBuilderError(null);
    setBuilderMessage(null);
    setBudgetMessage(null);
    setEditingBaseRow(apu.row_number);

    try {
      const base = await getApuDraft(apu.row_number);
      const term = search.trim();
      const normalizedTerm = term.toUpperCase();
      const useSearchAsDescription =
        term &&
        normalizedTerm !== apu.codigo_apu.toUpperCase() &&
        normalizedTerm !== apu.descripcion_apu.toUpperCase();
      const description = useSearchAsDescription
        ? term
        : `${base.descripcion_apu} - copia`;
      const code = await suggestApuCode(description).catch(() => null);

      startFromBase(base, description, code);
      clearMaterialPicker(
        `APU ${base.base_codigo_apu} cargado como base. Edita materiales y cantidades.`,
      );
      setBuilderMessage(
        `APU ${base.base_codigo_apu} cargado con ${base.detalles.length} materiales. Se guardara como APU nuevo.`,
      );

      window.setTimeout(() => {
        document.getElementById("apu-builder")?.scrollIntoView({ behavior: "smooth" });
      }, 50);
    } catch (caught) {
      setBuilderError(caught instanceof Error ? caught.message : "No se pudo cargar el APU base.");
    } finally {
      setEditingBaseRow(null);
    }
  }

  async function handleSaveApu() {
    setBuilderError(null);
    setBuilderMessage(null);
    setIsSaving(true);

    try {
      if (!draft.descripcion_apu.trim()) {
        throw new Error("La descripcion del APU es obligatoria.");
      }
      if (!draft.codigo_apu.trim()) {
        throw new Error("El codigo del APU es obligatorio.");
      }
      if (!validDetails.length) {
        throw new Error("Agrega al menos un detalle con codigo de insumo.");
      }

      const result = await createApu({
        codigo_apu: draft.codigo_apu.trim(),
        descripcion_apu: draft.descripcion_apu.trim(),
        unidad: draft.unidad.trim() || "UN",
        detalles: validDetails.map((detail) => ({
          tipo_item: "MATERIAL",
          codigo_item: detail.codigo_item.trim(),
          cantidad: detail.cantidad || "1",
          source_row_number: detail.source_row_number ?? null,
          cantidad_formula: detail.cantidad_formula ?? null,
        })),
      });

      setBuilderMessage(
        `APU guardado en fila ${result.header_row}. Formulas preservadas.`,
      );
      resetBuilder();
      loadApus(search);
    } catch (caught) {
      setBuilderError(caught instanceof Error ? caught.message : "Error inesperado.");
    } finally {
      setIsSaving(false);
    }
  }

  function handleAddApuToBudget(apu: Apu | null = budgetCandidate) {
    setBudgetMessage(null);
    setError(null);

    if (!apu) {
      setError("Busca o selecciona un APU especifico para agregarlo al presupuesto.");
      return;
    }

    addApuToDraftBudget(apu, "1");
    setBudgetMessage(`APU ${apu.codigo_apu} agregado al presupuesto en la app.`);
  }

  return (
    <main className="appShell">
      <section className="topBar">
        <div>
          <span className="eyebrow">Modulo B</span>
          <h1>APUs</h1>
          <p>
            Busqueda, construccion por detalles y guardado directo manteniendo los
            vinculos del Excel.
          </p>
        </div>
        <div className="statusPill">
          <FileSpreadsheet size={16} />
          APU&apos;S conectado
        </div>
      </section>

      <section className="toolbar">
        <label className="searchBox">
          <Search size={18} />
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Buscar APU por codigo o descripcion"
          />
        </label>

        <button
          className="primaryButton"
          type="button"
          onClick={() => handleStartCreate()}
        >
          <Plus size={17} />
          Nuevo APU
        </button>

        <button
          className="secondaryButton"
          type="button"
          onClick={() => handleAddApuToBudget()}
        >
          <Plus size={17} />
          Agregar APU
        </button>
      </section>

      {canCreate && search.trim() ? (
        <button
          className="createPrompt"
          type="button"
          onClick={() => handleStartCreate(search, suggestedCode)}
        >
          <Plus size={18} />
          Crear nuevo APU: {search}
        </button>
      ) : null}

      <section className="resultsHeader">
        <div>
          <h2>Lista de APUs</h2>
          <span>{`${total} coincidencias`}</span>
        </div>
        {isLoading ? (
          <span className="loadingText">
            <Loader2 className="spin" size={16} />
            Actualizando
          </span>
        ) : null}
      </section>

      {error ? <p className="panelError">{error}</p> : null}
      {budgetMessage ? <p className="formSuccess">{budgetMessage}</p> : null}

      <section className="mobileList">
        {apus.map((apu) => (
          <ApuCard
            key={`${apu.row_number}-${apu.codigo_apu}`}
            apu={apu}
            onAdd={handleAddApuToBudget}
            onEditAsNew={handleEditAsNew}
            isEditingAsNew={editingBaseRow === apu.row_number}
          />
        ))}
      </section>

      <section className="desktopTableWrap">
        <table className="materialsTable">
          <thead>
            <tr>
              <th>Codigo</th>
              <th>Descripcion</th>
              <th>Unidad</th>
              <th>Fila</th>
              <th>Formula total</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {apus.map((apu) => (
              <tr key={`${apu.row_number}-${apu.codigo_apu}`}>
                <td>{apu.codigo_apu}</td>
                <td>{apu.descripcion_apu}</td>
                <td>{apu.unidad}</td>
                <td>{apu.row_number}</td>
                <td>{apu.costo_total_formula || "-"}</td>
                <td>
                  <div className="tableActions">
                    <button
                      className="secondaryButton tableAction"
                      type="button"
                      onClick={() => handleAddApuToBudget(apu)}
                    >
                      <Plus size={15} />
                      Agregar
                    </button>
                    <button
                      className="secondaryButton tableAction"
                      type="button"
                      onClick={() => handleEditAsNew(apu)}
                      disabled={editingBaseRow === apu.row_number}
                    >
                      {editingBaseRow === apu.row_number ? (
                        <Loader2 className="spin" size={15} />
                      ) : (
                        <PencilLine size={15} />
                      )}
                      Editar como nuevo
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {!isLoading && !apus.length ? (
        <p className="emptyState">No hay APUs para esta busqueda.</p>
      ) : null}

      <section className="builderPanel" id="apu-builder">
        <div className="resultsHeader">
          <div>
            <h2>Constructor de APU</h2>
            <span>{validDetails.length} detalles listos para guardar</span>
          </div>
        </div>

        <div className="builderHeader">
          <label className="field">
            <span>Descripcion APU</span>
            <input
              value={draft.descripcion_apu}
              onChange={(event) =>
                setHeader({ descripcion_apu: event.target.value, codigo_apu: "" })
              }
              placeholder="Ej. Suministro e instalacion..."
            />
            <small className="fieldHint">Puedes editar el nombre antes de guardar.</small>
          </label>
          <label className="field">
            <span>Codigo APU</span>
            <input
              value={draft.codigo_apu}
              onChange={(event) => setHeader({ codigo_apu: event.target.value })}
              placeholder="Codigo sugerido"
            />
          </label>
          <label className="field">
            <span>Unidad</span>
            <input
              value={draft.unidad}
              onChange={(event) => setHeader({ unidad: event.target.value })}
              placeholder="UN"
            />
          </label>
        </div>

        <AddedMaterialsTable details={draft.detalles} />

        <div className="materialPicker">
          <label className="field materialSearchField">
            <span>Buscar material</span>
            <input
              value={materialSearch}
              onChange={(event) => {
                setMaterialSearch(event.target.value);
                setSelectedMaterial(null);
              }}
              placeholder="Codigo o descripcion del material"
            />
          </label>

          <label className="field">
            <span>Cantidad</span>
            <QuantityStepper value={materialQuantity} onChange={setMaterialQuantity} />
          </label>
        </div>

        <div className="lookupSummary">
          <span>
            {isMaterialLookupLoading ? <Loader2 className="spin" size={15} /> : null}
            {materialStatus || "Busca y selecciona un material"}
          </span>
        </div>

        {selectedMaterial ? (
          <div className="selectedItem">
            <strong>{selectedMaterial.codigo}</strong>
            <span>{selectedMaterial.descripcion}</span>
            <small>
              {selectedMaterial.und} · {formatCurrency(selectedMaterial.costo)}
            </small>
          </div>
        ) : null}

        {materialResults.length ? (
          <div className="lookupResults">
            {materialResults.map((material) => (
              <button
                className="lookupChoice"
                key={material.codigo}
                type="button"
                onClick={() => selectMaterial(material)}
              >
                <strong>{material.codigo}</strong>
                <span>{material.descripcion}</span>
              </button>
            ))}
          </div>
        ) : null}

        {materialCanCreate && materialSearch.trim() && !materialResults.length ? (
          <button
            className="createPrompt compact"
            type="button"
            onClick={() =>
              setInlineRequest({
                initialDescription: materialSearch,
                cantidad: materialQuantity || "1",
              })
            }
          >
            <Plus size={17} />
            Crear material: {materialSearch}
          </button>
        ) : null}

        <div className="detailsToolbar">
          <button
            className="secondaryButton"
            type="button"
            onClick={handleAddMaterial}
            disabled={!selectedMaterial}
          >
            <Plus size={17} />
            Agregar material
          </button>
        </div>

        {builderError ? <p className="formError">{builderError}</p> : null}
        {builderMessage ? <p className="formSuccess">{builderMessage}</p> : null}

        <div className="dialogActions builderActions">
          <button className="secondaryButton" type="button" onClick={resetBuilder}>
            Limpiar
          </button>
          <button className="primaryButton" type="button" onClick={handleSaveApu} disabled={isSaving}>
            {isSaving ? <Loader2 className="spin" size={17} /> : <Save size={17} />}
            Guardar APU
          </button>
        </div>
      </section>

      <InlineItemDialog
        request={inlineRequest}
        onClose={() => setInlineRequest(null)}
        onCreated={handleCreatedMaterial}
      />
    </main>
  );
}
