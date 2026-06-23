import { FileSpreadsheet, Loader2, Plus, Search } from "lucide-react";
import { ChangeEvent, useEffect, useState } from "react";

import {
  Material,
  MaterialsSearchResponse,
  searchMaterials,
} from "../../api/materials";
import { useMaterialsStore } from "../../store/materialsStore";
import { CreateMaterialDialog } from "./CreateMaterialDialog";

function formatCurrency(value: string) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    return value;
  }

  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  }).format(parsed);
}

function MaterialCard({ material }: { material: Material }) {
  return (
    <article className="materialCard">
      <div className="materialCardHeader">
        <strong>{material.codigo}</strong>
        <span>{material.und}</span>
      </div>
      <p>{material.descripcion}</p>
      <dl>
        <div>
          <dt>Marca</dt>
          <dd>{material.marca || "Sin marca"}</dd>
        </div>
        <div>
          <dt>Costo IVA</dt>
          <dd>{formatCurrency(material.valor_costo_incluido_iva)}</dd>
        </div>
      </dl>
    </article>
  );
}

export function MaterialsPage() {
  const [search, setSearch] = useState("");
  const [response, setResponse] = useState<MaterialsSearchResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const openCreate = useMaterialsStore((state) => state.openCreate);

  function loadMaterials(value = search) {
    setIsLoading(true);
    setError(null);
    searchMaterials(value)
      .then(setResponse)
      .catch((caught) =>
        setError(caught instanceof Error ? caught.message : "Error inesperado."),
      )
      .finally(() => setIsLoading(false));
  }

  useEffect(() => {
    const timeout = window.setTimeout(() => loadMaterials(search), 250);
    return () => window.clearTimeout(timeout);
  }, [search]);

  function handleSearch(event: ChangeEvent<HTMLInputElement>) {
    setSearch(event.target.value);
  }

  const items = response?.items ?? [];
  const canCreate = response?.can_create && response.search;

  return (
    <main className="appShell">
      <section className="topBar">
        <div>
          <span className="eyebrow">Modulo A</span>
          <h1>Materiales</h1>
          <p>
            Busqueda, codificacion y alta segura en el Excel base del presupuesto.
          </p>
        </div>
        <div className="statusPill">
          <FileSpreadsheet size={16} />
          Excel conectado
        </div>
      </section>

      <section className="toolbar">
        <label className="searchBox">
          <Search size={18} />
          <input
            value={search}
            onChange={handleSearch}
            placeholder="Buscar por codigo o descripcion"
          />
        </label>

        <button
          className="primaryButton"
          type="button"
          onClick={() => openCreate(search, response?.suggested_code)}
        >
          <Plus size={17} />
          Nuevo
        </button>
      </section>

      {canCreate ? (
        <button
          className="createPrompt"
          type="button"
          onClick={() => openCreate(response.search, response.suggested_code)}
        >
          <Plus size={18} />
          Crear nuevo: {response.search}
        </button>
      ) : null}

      <section className="resultsHeader">
        <div>
          <h2>Lista de materiales</h2>
          <span>
            {response ? `${response.total} coincidencias` : "Cargando datos"}
          </span>
        </div>
        {isLoading ? (
          <span className="loadingText">
            <Loader2 className="spin" size={16} />
            Actualizando
          </span>
        ) : null}
      </section>

      {error ? <p className="panelError">{error}</p> : null}

      <section className="mobileList">
        {items.map((material) => (
          <MaterialCard key={`${material.row_number}-${material.codigo}`} material={material} />
        ))}
      </section>

      <section className="desktopTableWrap">
        <table className="materialsTable">
          <thead>
            <tr>
              <th>Codigo</th>
              <th>Descripcion</th>
              <th>Marca</th>
              <th>UND</th>
              <th>Costo IVA</th>
              <th>Formula presupuesto</th>
            </tr>
          </thead>
          <tbody>
            {items.map((material) => (
              <tr key={`${material.row_number}-${material.codigo}`}>
                <td>{material.codigo}</td>
                <td>{material.descripcion}</td>
                <td>{material.marca || "-"}</td>
                <td>{material.und}</td>
                <td>{formatCurrency(material.valor_costo_incluido_iva)}</td>
                <td>{material.valor_presupuesto_formula || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {!isLoading && !items.length ? (
        <p className="emptyState">No hay materiales para esta busqueda.</p>
      ) : null}

      <CreateMaterialDialog onCreated={() => loadMaterials(search)} />
    </main>
  );
}
