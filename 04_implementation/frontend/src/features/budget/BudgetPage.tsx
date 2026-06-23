import { FileSpreadsheet, Loader2, Save, Trash2 } from "lucide-react";
import { useState } from "react";

import { exportFilteredBudget, saveBudget } from "../../api/budget";
import { useBudgetStore } from "../../store/budgetStore";

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

export function BudgetPage() {
  const items = useBudgetStore((state) => state.items);
  const updateQuantity = useBudgetStore((state) => state.updateQuantity);
  const removeItem = useBudgetStore((state) => state.removeItem);
  const clearBudget = useBudgetStore((state) => state.clearBudget);
  const [isSaving, setIsSaving] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [exportCode, setExportCode] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const payloadItems = items.map((item) => ({
    codigo_apu: item.codigo_apu,
    cantidad: item.cantidad || "1",
  }));

  async function handleSaveBudget() {
    setError(null);
    setMessage(null);

    if (!items.length) {
      setError("Agrega al menos un APU antes de guardar el presupuesto.");
      return;
    }

    setIsSaving(true);
    try {
      const result = await saveBudget(
        payloadItems,
      );
      setMessage(
        `Presupuesto guardado en la hoja ${result.sheet_name} con ${result.rows} APUs.`,
      );
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Error inesperado.");
    } finally {
      setIsSaving(false);
    }
  }

  async function handleExportFilteredBudget() {
    setError(null);
    setMessage(null);

    if (!items.length) {
      setError("Agrega al menos un APU antes de generar el archivo.");
      return;
    }
    if (!exportCode.trim()) {
      setError("Escribe un codigo para nombrar y seguir el archivo exportado.");
      return;
    }

    setIsExporting(true);
    try {
      const result = await exportFilteredBudget(payloadItems, exportCode.trim());
      setMessage(
        `Archivo ${result.file_name} generado con ${result.apus} APUs y ${result.materials} materiales. Ruta: ${result.file_path}`,
      );
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Error inesperado.");
    } finally {
      setIsExporting(false);
    }
  }

  return (
    <main className="appShell">
      <section className="topBar">
        <div>
          <span className="eyebrow">Presupuesto</span>
          <h1>Presupuesto</h1>
          <p>
            Revisa los APUs agregados y guarda una hoja nueva en Excel con el
            formato y formulas del presupuesto modelo.
          </p>
        </div>
        <div className="statusPill">
          <FileSpreadsheet size={16} />
          Borrador en app
        </div>
      </section>

      <section className="toolbar">
        <label className="field exportCodeField">
          <span>Codigo de archivo</span>
          <input
            value={exportCode}
            onChange={(event) => setExportCode(event.target.value)}
            placeholder="Ej. TULUA-001"
          />
        </label>
        <button
          className="primaryButton"
          type="button"
          onClick={handleSaveBudget}
          disabled={isSaving}
        >
          {isSaving ? <Loader2 className="spin" size={17} /> : <Save size={17} />}
          Guardar presupuesto
        </button>
        <button
          className="secondaryButton"
          type="button"
          onClick={handleExportFilteredBudget}
          disabled={isExporting}
        >
          {isExporting ? <Loader2 className="spin" size={17} /> : <FileSpreadsheet size={17} />}
          Generar archivo filtrado
        </button>
        <button className="secondaryButton" type="button" onClick={clearBudget}>
          Limpiar presupuesto
        </button>
      </section>

      {error ? <p className="panelError">{error}</p> : null}
      {message ? <p className="formSuccess">{message}</p> : null}

      <section className="resultsHeader">
        <div>
          <h2>APUs en presupuesto</h2>
          <span>{`${items.length} items`}</span>
        </div>
      </section>

      <section className="mobileList">
        {items.map((item) => (
          <article className="materialCard" key={item.id}>
            <div className="materialCardHeader">
              <strong>{item.codigo_apu}</strong>
              <span>{item.unidad || "UN"}</span>
            </div>
            <p>{item.descripcion_apu || "APU agregado al presupuesto"}</p>
            <dl>
              <div>
                <dt>Cantidad</dt>
                <dd>{item.cantidad}</dd>
              </div>
              <div>
                <dt>Destino</dt>
                <dd>Excel</dd>
              </div>
            </dl>
          </article>
        ))}
      </section>

      <section className="desktopTableWrap">
        <table className="materialsTable">
          <thead>
            <tr>
              <th>Item</th>
              <th>Codigo APU</th>
              <th>Descripcion</th>
              <th>UND</th>
              <th>Cantidad</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, index) => (
              <tr key={item.id}>
                <td>{index + 1}</td>
                <td>{item.codigo_apu}</td>
                <td>{item.descripcion_apu || "-"}</td>
                <td>{item.unidad || "-"}</td>
                <td>
                  <div className="quantityStepper">
                    <button
                      type="button"
                      onClick={() => updateQuantity(item.id, stepQuantity(item.cantidad, -1))}
                    >
                      -
                    </button>
                    <input
                      inputMode="decimal"
                      value={item.cantidad}
                      onChange={(event) => updateQuantity(item.id, event.target.value)}
                    />
                    <button
                      type="button"
                      onClick={() => updateQuantity(item.id, stepQuantity(item.cantidad, 1))}
                    >
                      +
                    </button>
                  </div>
                </td>
                <td>
                  <button
                    className="iconButton"
                    type="button"
                    onClick={() => removeItem(item.id)}
                    aria-label="Quitar APU"
                  >
                    <Trash2 size={17} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {!items.length ? (
        <p className="emptyState">
          Todavia no hay APUs en el presupuesto. Ve a APUs y usa Agregar APU.
        </p>
      ) : null}
    </main>
  );
}
