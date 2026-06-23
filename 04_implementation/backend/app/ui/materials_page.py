from __future__ import annotations


def render_materials_page() -> str:
    return """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Gestor de Presupuestos APU</title>
  <style>
    :root {
      color: #13271e;
      background: #eef3ee;
      font-family: "Aptos", "Segoe UI", sans-serif;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      background:
        linear-gradient(135deg, rgba(34, 95, 79, 0.08), transparent 36%),
        linear-gradient(180deg, #f8fbf7 0%, #e8f0eb 100%);
    }
    button, input { font: inherit; }
    button { cursor: pointer; }
    .appShell {
      width: min(1180px, calc(100% - 28px));
      margin: 0 auto;
      padding: 24px 0 42px;
    }
    .navBar {
      display: flex;
      gap: 10px;
      margin-bottom: 16px;
    }
    .navBar a {
      color: #173d31;
      text-decoration: none;
      font-weight: 800;
      background: rgba(255,255,255,0.9);
      border: 1px solid #c7d5cb;
      border-radius: 8px;
      padding: 10px 14px;
    }
    .topBar {
      display: flex;
      flex-direction: column;
      gap: 18px;
      padding: 18px 0 22px;
    }
    .eyebrow {
      color: #5d6f64;
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0;
      text-transform: uppercase;
    }
    h1, h2, p { margin: 0; }
    h1 {
      color: #10231a;
      font-size: clamp(2rem, 7vw, 4.6rem);
      line-height: 0.95;
      margin-top: 6px;
    }
    .topBar p {
      color: #506158;
      max-width: 720px;
      margin-top: 12px;
      font-size: 1rem;
    }
    .statusPill {
      align-items: center;
      display: inline-flex;
      gap: 8px;
      width: fit-content;
      background: #173d31;
      border: 1px solid #0e2b22;
      border-radius: 999px;
      color: #f6fff9;
      font-size: 0.9rem;
      font-weight: 700;
      padding: 9px 13px;
    }
    .toolbar {
      align-items: stretch;
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin: 10px 0 12px;
    }
    .searchBox, .field, .materialCard, .dialogContent, .materialsTable {
      background: rgba(255,255,255,0.96);
      border: 1px solid #d7e1da;
      border-radius: 8px;
    }
    .searchBox {
      align-items: center;
      display: flex;
      gap: 10px;
      min-height: 52px;
      padding: 0 14px;
      box-shadow: 0 12px 30px rgba(39, 75, 58, 0.08);
    }
    .searchBox input, .field input {
      background: transparent;
      border: 0;
      color: #10231a;
      outline: 0;
      width: 100%;
      min-width: 0;
    }
    .primaryButton, .secondaryButton, .createPrompt, .iconButton {
      align-items: center;
      border: 0;
      display: inline-flex;
      gap: 8px;
      justify-content: center;
    }
    .primaryButton {
      background: #d66b2c;
      border-radius: 8px;
      color: #fffaf6;
      font-weight: 800;
      min-height: 52px;
      padding: 0 18px;
    }
    .secondaryButton {
      background: #edf2ee;
      border: 1px solid #c7d5cb;
      border-radius: 8px;
      color: #1d3428;
      font-weight: 800;
      min-height: 46px;
      padding: 0 16px;
    }
    .createPrompt {
      background: #fff5de;
      border: 1px solid #f0c978;
      border-radius: 8px;
      color: #5f3b09;
      font-weight: 800;
      margin-bottom: 14px;
      min-height: 48px;
      padding: 0 14px;
      width: 100%;
    }
    .resultsHeader {
      align-items: flex-end;
      display: flex;
      justify-content: space-between;
      gap: 16px;
      margin: 22px 0 12px;
    }
    .resultsHeader h2 { color: #1d3428; font-size: 1.1rem; }
    .resultsHeader span, .loadingText { color: #65766b; font-size: 0.9rem; }
    .loadingText { align-items: center; display: inline-flex; gap: 8px; font-weight: 700; }
    .mobileList { display: grid; gap: 10px; }
    .materialCard { padding: 14px; }
    .materialCardHeader {
      align-items: flex-start;
      display: flex;
      gap: 12px;
      justify-content: space-between;
    }
    .materialCardHeader strong { overflow-wrap: anywhere; }
    .materialCardHeader span {
      background: #e9f0ea;
      border-radius: 999px;
      color: #355346;
      flex: 0 0 auto;
      font-size: 0.78rem;
      font-weight: 800;
      padding: 4px 9px;
    }
    .materialCard p { color: #46574e; margin-top: 8px; }
    .materialCard dl {
      display: grid;
      gap: 8px;
      grid-template-columns: 1fr 1fr;
      margin: 14px 0 0;
    }
    .materialCard dt { color: #79877f; font-size: 0.75rem; }
    .materialCard dd {
      color: #173d31;
      font-weight: 800;
      margin: 2px 0 0;
      overflow-wrap: anywhere;
    }
    .desktopTableWrap { display: none; }
    .materialsTable {
      border-collapse: collapse;
      overflow: hidden;
      width: 100%;
      box-shadow: 0 18px 44px rgba(39, 75, 58, 0.1);
    }
    .materialsTable th, .materialsTable td {
      border-bottom: 1px solid #dde7e0;
      padding: 12px 14px;
      text-align: left;
      vertical-align: top;
    }
    .materialsTable th {
      background: #173d31;
      color: #f4fff7;
      font-size: 0.78rem;
      text-transform: uppercase;
    }
    .materialsTable td { color: #243c30; font-size: 0.9rem; }
    .panelError, .formError, .formSuccess {
      border-radius: 8px;
      padding: 12px;
      margin-top: 12px;
    }
    .panelError, .formError {
      background: #ffe8df;
      border: 1px solid #f2b198;
      color: #7d240f;
    }
    .formSuccess {
      background: #e8f6e7;
      border: 1px solid #a4d0a2;
      color: #245626;
    }
    .emptyState { color: #65766b; padding: 26px 0; }
    .dialogOverlay {
      background: rgba(8, 24, 18, 0.55);
      inset: 0;
      display: none;
      position: fixed;
      z-index: 30;
    }
    .dialogOverlay.open { display: block; }
    .dialogContent {
      bottom: 0;
      box-shadow: 0 -24px 50px rgba(11, 32, 24, 0.2);
      left: 0;
      max-height: 92vh;
      overflow-y: auto;
      padding: 18px;
      position: fixed;
      right: 0;
      transform: translateY(100%);
      transition: transform 160ms ease-out;
      z-index: 31;
    }
    .dialogContent.open { transform: translateY(0); }
    .dialogHeader {
      align-items: flex-start;
      display: flex;
      gap: 16px;
      justify-content: space-between;
    }
    .dialogTitle {
      color: #13271e;
      font-size: 1.3rem;
      font-weight: 900;
      margin: 0;
    }
    .dialogDescription { color: #5e6f65; margin-top: 4px; }
    .iconButton {
      background: #edf2ee;
      border-radius: 999px;
      color: #22372c;
      height: 38px;
      width: 38px;
    }
    .materialForm {
      display: grid;
      gap: 13px;
      margin-top: 18px;
    }
    .field {
      display: grid;
      gap: 6px;
      padding: 11px 12px;
    }
    .field span {
      color: #5f7066;
      font-size: 0.78rem;
      font-weight: 800;
      text-transform: uppercase;
    }
    .field input { font-size: 1rem; }
    .formGrid { display: grid; gap: 13px; grid-template-columns: 1fr; }
    .dialogActions {
      display: grid;
      gap: 10px;
      grid-template-columns: 1fr;
      margin-top: 4px;
    }
    .spin { animation: spin 0.9s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
    @media (min-width: 720px) {
      .appShell { padding-top: 38px; }
      .topBar {
        align-items: flex-end;
        flex-direction: row;
        justify-content: space-between;
      }
      .toolbar { align-items: center; flex-direction: row; }
      .searchBox { flex: 1; }
      .primaryButton { width: auto; }
      .createPrompt { width: auto; }
      .mobileList { display: none; }
      .desktopTableWrap { display: block; overflow-x: auto; }
      .dialogContent {
        border-radius: 8px;
        bottom: auto;
        left: 50%;
        max-width: 620px;
        right: auto;
        top: 50%;
        transform: translate(-50%, 140%);
        width: min(620px, calc(100% - 34px));
      }
      .dialogContent.open { transform: translate(-50%, -50%); }
      .formGrid, .dialogActions { grid-template-columns: 1fr 1fr; }
      .dialogActions { justify-content: end; }
    }
  </style>
</head>
<body>
  <main class="appShell">
    <nav class="navBar">
      <a href="/">Materiales</a>
      <a href="/apus">APUs</a>
    </nav>

    <section class="topBar">
      <div>
        <span class="eyebrow">Modulo A</span>
        <h1>Materiales</h1>
        <p>Busqueda, codificacion y alta segura en el Excel base del presupuesto.</p>
      </div>
      <div class="statusPill">Excel conectado</div>
    </section>

    <section class="toolbar">
      <label class="searchBox">
        <span>Buscar</span>
        <input id="search" placeholder="Buscar por codigo o descripcion" />
      </label>
      <button id="newButton" class="primaryButton" type="button">Nuevo</button>
    </section>

    <button id="createPrompt" class="createPrompt" type="button" style="display:none;"></button>

    <section class="resultsHeader">
      <div>
        <h2>Lista de materiales</h2>
        <span id="resultCount">Cargando datos</span>
      </div>
      <span id="loadingText" class="loadingText" style="display:none;">Actualizando</span>
    </section>

    <div id="errorBox" class="panelError" style="display:none;"></div>
    <section id="mobileList" class="mobileList"></section>
    <section class="desktopTableWrap">
      <table class="materialsTable">
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
        <tbody id="tableBody"></tbody>
      </table>
    </section>
    <p id="emptyState" class="emptyState" style="display:none;">No hay materiales para esta busqueda.</p>
  </main>

  <div id="dialogOverlay" class="dialogOverlay"></div>
  <section id="dialogContent" class="dialogContent" aria-hidden="true">
    <div class="dialogHeader">
      <div>
        <h3 class="dialogTitle">Crear material</h3>
        <p class="dialogDescription">Se agregara al Excel copiando formulas de la fila anterior.</p>
      </div>
      <button id="closeDialog" class="iconButton" type="button" aria-label="Cerrar">X</button>
    </div>
    <form id="materialForm" class="materialForm">
      <label class="field">
        <span>Descripcion</span>
        <input id="descripcion" required placeholder="Ej. Tubo PVC 3/4" />
      </label>
      <label class="field">
        <span>Codigo sugerido</span>
        <input id="codigo" required placeholder="TUBO-PVC-3/4" />
      </label>
      <div class="formGrid">
        <label class="field">
          <span>Marca</span>
          <input id="marca" placeholder="Opcional" />
        </label>
        <label class="field">
          <span>Unidad</span>
          <input id="und" required placeholder="UN" />
        </label>
      </div>
      <div class="formGrid">
        <label class="field">
          <span>Factor (%)</span>
          <input id="factor" inputmode="decimal" placeholder="20" />
        </label>
        <label class="field">
          <span>Costo con IVA</span>
          <input id="costo" inputmode="decimal" placeholder="0" />
        </label>
      </div>
      <div id="formError" class="formError" style="display:none;"></div>
      <div id="formSuccess" class="formSuccess" style="display:none;"></div>
      <div class="dialogActions">
        <button id="cancelButton" class="secondaryButton" type="button">Cancelar</button>
        <button id="saveButton" class="primaryButton" type="submit">Guardar</button>
      </div>
    </form>
  </section>

  <script>
    const API_BASE = "/api";
    const state = {
      search: "",
      items: [],
      total: 0,
      canCreate: false,
      suggestedCode: null,
      isLoading: false,
      draft: {
        codigo: "",
        descripcion: "",
        marca: "",
        und: "UN",
        factor: "20",
        valor_costo_incluido_iva: "0",
      },
      createOpen: false,
      message: "",
    };

    const el = (id) => document.getElementById(id);
    const searchInput = el("search");
    const newButton = el("newButton");
    const createPrompt = el("createPrompt");
    const loadingText = el("loadingText");
    const resultCount = el("resultCount");
    const mobileList = el("mobileList");
    const tableBody = el("tableBody");
    const emptyState = el("emptyState");
    const errorBox = el("errorBox");
    const dialogOverlay = el("dialogOverlay");
    const dialogContent = el("dialogContent");
    const closeDialog = el("closeDialog");
    const cancelButton = el("cancelButton");
    const materialForm = el("materialForm");
    const descripcionInput = el("descripcion");
    const codigoInput = el("codigo");
    const marcaInput = el("marca");
    const undInput = el("und");
    const factorInput = el("factor");
    const costoInput = el("costo");
    const formError = el("formError");
    const formSuccess = el("formSuccess");
    const saveButton = el("saveButton");

    function setLoading(value) {
      state.isLoading = value;
      loadingText.style.display = value ? "inline-flex" : "none";
    }

    function setError(message) {
      errorBox.style.display = message ? "block" : "none";
      errorBox.textContent = message || "";
    }

    function setFormMessage(error, success) {
      formError.style.display = error ? "block" : "none";
      formSuccess.style.display = success ? "block" : "none";
      formError.textContent = error || "";
      formSuccess.textContent = success || "";
    }

    function formatCurrency(value) {
      const parsed = Number(value);
      if (!Number.isFinite(parsed)) return value || "-";
      return new Intl.NumberFormat("es-CO", {
        style: "currency",
        currency: "COP",
        maximumFractionDigits: 0,
      }).format(parsed);
    }

    function openDialog() {
      state.createOpen = true;
      dialogOverlay.classList.add("open");
      dialogContent.classList.add("open");
      dialogContent.setAttribute("aria-hidden", "false");
      descripcionInput.value = state.draft.descripcion;
      codigoInput.value = state.draft.codigo;
      marcaInput.value = state.draft.marca;
      undInput.value = state.draft.und;
      factorInput.value = state.draft.factor;
      costoInput.value = state.draft.valor_costo_incluido_iva;
      setFormMessage("", "");
      setTimeout(() => descripcionInput.focus(), 20);
    }

    function closeDialogFn() {
      state.createOpen = false;
      dialogOverlay.classList.remove("open");
      dialogContent.classList.remove("open");
      dialogContent.setAttribute("aria-hidden", "true");
    }

    function syncDraftFromFields() {
      state.draft.descripcion = descripcionInput.value;
      state.draft.codigo = codigoInput.value;
      state.draft.marca = marcaInput.value;
      state.draft.und = undInput.value;
      state.draft.factor = factorInput.value;
      state.draft.valor_costo_incluido_iva = costoInput.value;
    }

    function percentageToDecimal(value) {
      const cleaned = String(value || "0").replace("%", "").replace(",", ".").trim();
      const parsed = Number(cleaned);
      if (!Number.isFinite(parsed)) {
        return "0";
      }
      return String(parsed / 100);
    }

    async function request(path, options) {
      const response = await fetch(API_BASE + path, {
        headers: { "Content-Type": "application/json" },
        ...options,
      });
      if (!response.ok) {
        let detail = null;
        try { detail = await response.json(); } catch (err) { detail = null; }
        const message = detail && detail.detail && typeof detail.detail === "string"
          ? detail.detail
          : "No se pudo completar la operacion.";
        throw new Error(message);
      }
      return response.json();
    }

    async function loadMaterials(value) {
      setLoading(true);
      setError("");
      try {
        const query = new URLSearchParams({ search: value || "", limit: "80" });
        const response = await request("/materials?" + query.toString());
        state.search = response.search || "";
        state.items = response.items || [];
        state.total = response.total || 0;
        state.canCreate = Boolean(response.can_create);
        state.suggestedCode = response.suggested_code || null;
        render();
      } catch (error) {
        setError(error instanceof Error ? error.message : "Error inesperado.");
      } finally {
        setLoading(false);
      }
    }

    function renderCards() {
      mobileList.innerHTML = state.items.map((material) => `
        <article class="materialCard">
          <div class="materialCardHeader">
            <strong>${material.codigo}</strong>
            <span>${material.und}</span>
          </div>
          <p>${material.descripcion}</p>
          <dl>
            <div>
              <dt>Marca</dt>
              <dd>${material.marca || "Sin marca"}</dd>
            </div>
            <div>
              <dt>Costo IVA</dt>
              <dd>${formatCurrency(material.valor_costo_incluido_iva)}</dd>
            </div>
          </dl>
        </article>
      `).join("");
    }

    function renderTable() {
      tableBody.innerHTML = state.items.map((material) => `
        <tr>
          <td>${material.codigo}</td>
          <td>${material.descripcion}</td>
          <td>${material.marca || "-"}</td>
          <td>${material.und}</td>
          <td>${formatCurrency(material.valor_costo_incluido_iva)}</td>
          <td>${material.valor_presupuesto_formula || "-"}</td>
        </tr>
      `).join("");
    }

    function renderPrompt() {
      if (state.canCreate && state.search) {
        createPrompt.style.display = "inline-flex";
        createPrompt.textContent = "Crear nuevo: " + state.search;
      } else {
        createPrompt.style.display = "none";
      }
    }

    function render() {
      resultCount.textContent = state.total + " coincidencias";
      renderPrompt();
      renderCards();
      renderTable();
      emptyState.style.display = !state.isLoading && !state.items.length ? "block" : "none";
    }

    searchInput.addEventListener("input", () => {
      window.clearTimeout(window.__searchTimer);
      const value = searchInput.value;
      window.__searchTimer = window.setTimeout(() => loadMaterials(value), 250);
    });

    newButton.addEventListener("click", () => {
      syncDraftFromFields();
      if (!state.draft.descripcion) {
        state.draft.descripcion = searchInput.value;
      }
      if (!state.draft.codigo) {
        state.draft.codigo = state.suggestedCode || "";
      }
      openDialog();
    });

    createPrompt.addEventListener("click", () => {
      state.draft.descripcion = state.search;
      state.draft.codigo = state.suggestedCode || "";
      openDialog();
    });

    closeDialog.addEventListener("click", closeDialogFn);
    cancelButton.addEventListener("click", closeDialogFn);
    dialogOverlay.addEventListener("click", closeDialogFn);

    descripcionInput.addEventListener("input", () => {
      state.draft.descripcion = descripcionInput.value;
      state.draft.codigo = "";
      if (!descripcionInput.value.trim()) return;
      window.clearTimeout(window.__suggestTimer);
      window.__suggestTimer = window.setTimeout(async () => {
        try {
          const query = new URLSearchParams({ description: descripcionInput.value });
          const response = await request("/materials/suggest-code?" + query.toString());
          state.draft.codigo = response.suggested_code;
          codigoInput.value = response.suggested_code;
        } catch (error) {
          console.warn(error);
        }
      }, 300);
    });

    codigoInput.addEventListener("input", () => state.draft.codigo = codigoInput.value);
    marcaInput.addEventListener("input", () => state.draft.marca = marcaInput.value);
    undInput.addEventListener("input", () => state.draft.und = undInput.value);
    factorInput.addEventListener("input", () => state.draft.factor = factorInput.value);
    costoInput.addEventListener("input", () => state.draft.valor_costo_incluido_iva = costoInput.value);

    materialForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      syncDraftFromFields();
      setFormMessage("", "");
      saveButton.disabled = true;
      try {
        const payload = {
          codigo: state.draft.codigo.trim(),
          descripcion: state.draft.descripcion.trim(),
          marca: state.draft.marca.trim() || null,
          und: state.draft.und.trim() || "UN",
          factor: percentageToDecimal(state.draft.factor),
          valor_costo_incluido_iva: state.draft.valor_costo_incluido_iva || "0",
        };
        const result = await request("/materials", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        setFormMessage("", "Material guardado en fila " + result.row_number + ". Formulas preservadas.");
        await loadMaterials(searchInput.value);
        state.draft = {
          codigo: "",
          descripcion: "",
          marca: "",
          und: "UN",
          factor: "20",
          valor_costo_incluido_iva: "0",
        };
        window.setTimeout(closeDialogFn, 900);
      } catch (error) {
        setFormMessage(error instanceof Error ? error.message : "Error inesperado.", "");
      } finally {
        saveButton.disabled = false;
      }
    });

    loadMaterials("");
  </script>
</body>
</html>"""
