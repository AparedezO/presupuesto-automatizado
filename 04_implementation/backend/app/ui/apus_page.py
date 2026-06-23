from __future__ import annotations


def render_apus_page() -> str:
    return """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Gestor de Presupuestos APU - APUs</title>
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
    button, input, select {
      font: inherit;
    }
    button { cursor: pointer; }
    .appShell {
      width: min(1280px, calc(100% - 28px));
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
    .hero {
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
    h1, h2, h3, p { margin: 0; }
    h1 {
      color: #10231a;
      font-size: clamp(2rem, 7vw, 4.2rem);
      line-height: 0.95;
      margin-top: 6px;
    }
    .hero p {
      color: #506158;
      max-width: 760px;
      margin-top: 12px;
      font-size: 1rem;
    }
    .statusPill, .loadingText, .lookupState {
      align-items: center;
      display: inline-flex;
      gap: 8px;
      width: fit-content;
    }
    .statusPill {
      background: #173d31;
      border: 1px solid #0e2b22;
      border-radius: 999px;
      color: #f6fff9;
      font-size: 0.9rem;
      font-weight: 700;
      padding: 9px 13px;
    }
    .toolbar {
      display: grid;
      gap: 10px;
      grid-template-columns: 1fr;
      margin: 14px 0 8px;
    }
    .searchBox, .field, .card, .dialogContent, .detailsPanel, .resultsPanel, .resultsCard {
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
    .searchBox input, .field input, .field select {
      background: transparent;
      border: 0;
      color: #10231a;
      outline: 0;
      width: 100%;
      min-width: 0;
    }
    .primaryButton, .secondaryButton, .dangerButton, .createPrompt, .iconButton {
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
      min-height: 48px;
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
    .dangerButton {
      background: #ffe8df;
      border: 1px solid #f2b198;
      border-radius: 8px;
      color: #7d240f;
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
      min-height: 46px;
      padding: 0 14px;
      width: 100%;
    }
    .gridTwo {
      display: grid;
      gap: 10px;
      grid-template-columns: 1fr;
    }
    .sectionTitle {
      align-items: flex-end;
      display: flex;
      justify-content: space-between;
      gap: 16px;
      margin: 24px 0 12px;
    }
    .sectionTitle h2, .sectionTitle h3 {
      color: #1d3428;
      font-size: 1.1rem;
    }
    .sectionTitle span, .loadingText, .lookupState {
      color: #65766b;
      font-size: 0.9rem;
      font-weight: 700;
    }
    .resultsPanel { padding: 14px; }
    .resultsList { display: grid; gap: 10px; margin-top: 12px; }
    .resultsCard { padding: 12px 14px; }
    .resultsCard strong { display: block; overflow-wrap: anywhere; }
    .resultsCard p { color: #46574e; margin-top: 6px; }
    .builderPanel {
      display: grid;
      gap: 14px;
    }
    .builderHeader {
      display: grid;
      gap: 10px;
      grid-template-columns: 1fr;
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
    .detailsPanel { padding: 14px; }
    .detailsHead {
      align-items: center;
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 12px;
    }
    .detailRows { display: grid; gap: 10px; }
    .detailCard {
      border: 1px solid #d7e1da;
      border-radius: 8px;
      padding: 12px;
      background: #fff;
      display: grid;
      gap: 10px;
    }
    .detailTop {
      display: grid;
      gap: 8px;
      grid-template-columns: 1fr 1fr;
    }
    .detailTop .wide { grid-column: 1 / -1; }
    .detailMeta {
      display: grid;
      gap: 8px;
      grid-template-columns: 1fr 1fr 1fr;
      color: #415047;
      font-size: 0.9rem;
    }
    .detailMeta div {
      background: #f6faf7;
      border-radius: 8px;
      padding: 10px;
    }
    .detailMeta strong { display: block; color: #173d31; margin-top: 4px; }
    .detailActions {
      align-items: center;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .lookupResults {
      display: grid;
      gap: 8px;
    }
    .lookupChoice {
      background: #f7faf8;
      border: 1px solid #d7e1da;
      border-radius: 8px;
      color: #173d31;
      padding: 10px 12px;
      text-align: left;
      width: 100%;
    }
    .lookupChoice strong {
      display: block;
      overflow-wrap: anywhere;
    }
    .lookupChoice small {
      color: #65766b;
      display: block;
      margin-top: 4px;
      overflow-wrap: anywhere;
    }
    .lookupHint {
      color: #6a7a71;
      font-size: 0.85rem;
    }
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
    .formGrid {
      display: grid;
      gap: 13px;
      grid-template-columns: 1fr;
      margin-top: 16px;
    }
    .formError, .formSuccess {
      border-radius: 8px;
      padding: 12px;
      margin-top: 12px;
    }
    .formError {
      background: #ffe8df;
      border: 1px solid #f2b198;
      color: #7d240f;
    }
    .formSuccess {
      background: #e8f6e7;
      border: 1px solid #a4d0a2;
      color: #245626;
    }
    .hide { display: none !important; }
    @media (min-width: 900px) {
      .hero {
        align-items: flex-end;
        flex-direction: row;
        justify-content: space-between;
      }
      .toolbar, .builderHeader, .gridTwo {
        grid-template-columns: 1fr 1fr;
      }
      .detailsHead { align-items: flex-end; }
      .detailTop { grid-template-columns: 1fr 1fr 1fr 1fr; }
      .dialogContent {
        border-radius: 8px;
        bottom: auto;
        left: 50%;
        max-width: 720px;
        right: auto;
        top: 50%;
        transform: translate(-50%, 140%);
        width: min(720px, calc(100% - 34px));
      }
      .dialogContent.open { transform: translate(-50%, -50%); }
      .formGrid { grid-template-columns: 1fr 1fr; }
    }
  </style>
</head>
<body>
  <main class="appShell">
    <nav class="navBar">
      <a href="/">Materiales</a>
      <a href="/apus">APUs</a>
    </nav>

    <section class="hero">
      <div>
        <span class="eyebrow">Modulo B</span>
        <h1>APUs</h1>
        <p>Busqueda, construccion por bloques y alta segura de insumos con preservacion de formulas en la hoja APU'S.</p>
      </div>
      <div class="statusPill">Excel conectado</div>
    </section>

    <section class="toolbar">
      <label class="searchBox">
        <span>Buscar</span>
        <input id="apuSearch" placeholder="Buscar por codigo o descripcion" />
      </label>
      <button id="createApu" class="primaryButton" type="button">Nuevo APU</button>
    </section>

    <section class="resultsPanel">
      <div class="sectionTitle">
        <div>
          <h2>APUs existentes</h2>
          <span id="apuCount">Cargando datos</span>
        </div>
        <span id="searchLoading" class="loadingText hide">Actualizando</span>
      </div>
      <button id="createPrompt" class="createPrompt hide" type="button"></button>
      <div id="apuResults" class="resultsList"></div>
    </section>

    <section class="builderPanel">
      <div class="sectionTitle">
        <div>
          <h2>Constructor de APU</h2>
          <span>Cabecera, detalles y guardado directo en Excel</span>
        </div>
      </div>

      <div class="builderHeader">
        <label class="field">
          <span>Descripcion APU</span>
          <input id="apuDescripcion" placeholder="Ej. SUMINISTRO E INSTALACION ..." />
        </label>
        <label class="field">
          <span>Codigo APU</span>
          <input id="apuCodigo" placeholder="Se autogenerara si queda vacio" />
        </label>
        <label class="field">
          <span>Unidad</span>
          <input id="apuUnidad" placeholder="UN" value="UN" />
        </label>
        <div class="detailsHead">
          <div class="lookupState" id="builderState">0 detalles</div>
          <div class="detailActions">
            <button id="addRow" class="secondaryButton" type="button">Agregar detalle</button>
            <button id="saveApu" class="primaryButton" type="button">Guardar APU</button>
          </div>
        </div>
      </div>

      <div id="detailRows" class="detailRows"></div>
      <div id="builderError" class="formError hide"></div>
      <div id="builderSuccess" class="formSuccess hide"></div>
    </section>
  </main>

  <div id="dialogOverlay" class="dialogOverlay"></div>
  <section id="dialogContent" class="dialogContent" aria-hidden="true">
    <div class="dialogHeader">
      <div>
        <h3 class="dialogTitle">Crear insumo</h3>
        <p class="dialogDescription">La carga del APU quedara en memoria mientras registras el insumo faltante.</p>
      </div>
      <button id="closeDialog" class="iconButton" type="button" aria-label="Cerrar">X</button>
    </div>

    <div class="formGrid">
      <label class="field">
        <span>Tipo</span>
        <select id="itemType">
          <option value="MATERIAL">Material</option>
          <option value="LABOR">Mano de obra / E&H</option>
        </select>
      </label>
      <label class="field">
        <span>Codigo</span>
        <input id="itemCode" placeholder="Codigo del insumo" />
      </label>
      <label class="field">
        <span>Descripcion</span>
        <input id="itemDescription" placeholder="Descripcion" />
      </label>
      <label class="field" id="itemBrandWrap">
        <span>Marca</span>
        <input id="itemBrand" placeholder="Opcional" />
      </label>
      <label class="field">
        <span>Unidad</span>
        <input id="itemUnit" placeholder="UN" />
      </label>
      <label class="field" id="itemFactorWrap">
        <span>Factor (%)</span>
        <input id="itemFactor" inputmode="decimal" placeholder="20" />
      </label>
      <label class="field" id="itemCostWrap">
        <span>Costo / Valor dia</span>
        <input id="itemCost" inputmode="decimal" placeholder="0" />
      </label>
    </div>

    <div id="dialogError" class="formError hide"></div>
    <div id="dialogSuccess" class="formSuccess hide"></div>
    <div class="detailActions" style="margin-top:16px;">
      <button id="cancelCreate" class="secondaryButton" type="button">Cancelar</button>
      <button id="saveItem" class="primaryButton" type="button">Guardar insumo</button>
    </div>
  </section>

  <script>
    const API = "/api";
    const state = {
      apuSearch: "",
      apus: [],
      builder: {
        codigo: "",
        descripcion: "",
        unidad: "UN",
        details: [],
      },
      activeDialogRowId: null,
      activeDialogType: "MATERIAL",
      activeDialogSearch: "",
    };

    const el = (id) => document.getElementById(id);
    const apuSearchInput = el("apuSearch");
    const apuResults = el("apuResults");
    const apuCount = el("apuCount");
    const searchLoading = el("searchLoading");
    const createPrompt = el("createPrompt");
    const builderState = el("builderState");
    const apuDescripcion = el("apuDescripcion");
    const apuCodigo = el("apuCodigo");
    const apuUnidad = el("apuUnidad");
    const detailRows = el("detailRows");
    const builderError = el("builderError");
    const builderSuccess = el("builderSuccess");
    const addRowButton = el("addRow");
    const saveApuButton = el("saveApu");
    const createApuButton = el("createApu");
    const dialogOverlay = el("dialogOverlay");
    const dialogContent = el("dialogContent");
    const closeDialog = el("closeDialog");
    const cancelCreate = el("cancelCreate");
    const saveItem = el("saveItem");
    const dialogError = el("dialogError");
    const dialogSuccess = el("dialogSuccess");
    const itemType = el("itemType");
    const itemCode = el("itemCode");
    const itemDescription = el("itemDescription");
    const itemBrandWrap = el("itemBrandWrap");
    const itemBrand = el("itemBrand");
    const itemUnit = el("itemUnit");
    const itemFactorWrap = el("itemFactorWrap");
    const itemFactor = el("itemFactor");
    const itemCostWrap = el("itemCostWrap");
    const itemCost = el("itemCost");

    function request(path, options) {
      return fetch(API + path, {
        headers: { "Content-Type": "application/json" },
        ...options,
      }).then(async (response) => {
        if (!response.ok) {
          let detail = null;
          try { detail = await response.json(); } catch (err) { detail = null; }
          const message = detail && detail.detail && typeof detail.detail === "string"
            ? detail.detail
            : "No se pudo completar la operacion.";
          throw new Error(message);
        }
        return response.json();
      });
    }

    function slugCode(value) {
      return String(value || "")
        .normalize("NFKD")
        .replace(/[^\w\s/.-]+/g, "")
        .toUpperCase()
        .replace(/\s+/g, "-")
        .replace(/-+/g, "-")
        .replace(/^-|-$/g, "")
        .slice(0, 28) || "APU-001";
    }

    function percentToDecimal(value) {
      const cleaned = String(value || "0").replace("%", "").replace(",", ".").trim();
      const parsed = Number(cleaned);
      if (!Number.isFinite(parsed)) {
        return "0";
      }
      return String(parsed / 100);
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

    function setText(elm, text) {
      elm.textContent = text;
    }

    function setVisible(elm, visible) {
      elm.classList.toggle("hide", !visible);
    }

    function showDialogError(message) {
      setText(dialogError, message);
      setVisible(dialogError, Boolean(message));
    }

    function showDialogSuccess(message) {
      setText(dialogSuccess, message);
      setVisible(dialogSuccess, Boolean(message));
    }

    function showBuilderError(message) {
      setText(builderError, message);
      setVisible(builderError, Boolean(message));
    }

    function showBuilderSuccess(message) {
      setText(builderSuccess, message);
      setVisible(builderSuccess, Boolean(message));
    }

    function openDialog(type, rowId, searchTerm = "") {
      state.activeDialogType = type;
      state.activeDialogRowId = rowId;
      state.activeDialogSearch = searchTerm;
      itemType.value = type;
      itemCode.value = searchTerm ? slugCode(searchTerm) : "";
      itemDescription.value = searchTerm || "";
      itemBrand.value = "";
      itemUnit.value = type === "LABOR" ? "HR" : "UN";
      itemFactor.value = "20";
      itemCost.value = "0";
      showDialogError("");
      showDialogSuccess("");
      syncDialogFields();
      updateDialogFields();
      dialogOverlay.classList.add("open");
      dialogContent.classList.add("open");
      dialogContent.setAttribute("aria-hidden", "false");
      setTimeout(() => itemCode.focus(), 20);
    }

    function closeDialogFn() {
      state.activeDialogRowId = null;
      dialogOverlay.classList.remove("open");
      dialogContent.classList.remove("open");
      dialogContent.setAttribute("aria-hidden", "true");
    }

    function syncDialogFields() {
      state.activeDialogType = itemType.value;
      state.activeDialogSearch = itemDescription.value;
    }

    function updateDialogFields() {
      const isMaterial = itemType.value === "MATERIAL";
      itemBrandWrap.style.display = isMaterial ? "grid" : "none";
      itemFactorWrap.style.display = isMaterial ? "grid" : "none";
      itemCostWrap.querySelector("span").textContent = isMaterial ? "Costo con IVA" : "Valor dia";
      itemUnit.placeholder = isMaterial ? "UN" : "HR";
    }

    async function loadApus(search = "") {
      searchLoading.classList.remove("hide");
      try {
        const query = new URLSearchParams({ search, limit: "50" });
        const response = await request("/apus?" + query.toString());
        state.apus = response.items || [];
        apuCount.textContent = response.total + " coincidencias";
        createPrompt.textContent = response.can_create && response.search
          ? "Crear nuevo: " + response.search
          : "";
        setVisible(createPrompt, Boolean(response.can_create && response.search));
        renderApuCards();
      } catch (error) {
        apuCount.textContent = "No se pudo cargar la lista";
        console.warn(error);
      } finally {
        searchLoading.classList.add("hide");
      }
    }

    function renderApuCards() {
      apuResults.innerHTML = state.apus.map((apu) => `
        <article class="resultsCard">
          <strong>${apu.codigo_apu}</strong>
          <p>${apu.descripcion_apu}</p>
          <p>${apu.unidad} | Fila ${apu.row_number}</p>
        </article>
      `).join("");
    }

    function updateBuilderState() {
      builderState.textContent = state.builder.details.length + " detalles";
    }

    function createDetailRow(detail = { tipo_item: "MATERIAL", codigo_item: "", cantidad: "1" }) {
      const rowId = "row-" + Math.random().toString(36).slice(2, 9);
      const row = {
        id: rowId,
        tipo_item: detail.tipo_item,
        codigo_item: detail.codigo_item || "",
        cantidad: String(detail.cantidad || "1"),
        descripcion: "",
        unidad: "",
        costo: "",
        searchResults: [],
        canCreate: false,
        search: "",
      };
      state.builder.details.push(row);

      const card = document.createElement("article");
      card.className = "detailCard";
      card.id = rowId;
      card.innerHTML = `
        <div class="detailTop">
          <label class="field wide">
            <span>Tipo</span>
            <select data-role="type">
              <option value="MATERIAL">Material</option>
              <option value="LABOR">Mano de obra / E&H</option>
              <option value="CUADRILLA">Cuadrilla</option>
            </select>
          </label>
        <label class="field wide">
            <span>Codigo o descripcion</span>
            <input data-role="code" placeholder="Ej. ARAN-P1/2 o arandela" />
          </label>
          <label class="field">
            <span>Cantidad</span>
            <input data-role="qty" inputmode="decimal" placeholder="1" />
          </label>
          <div class="detailActions">
            <button data-role="lookup" class="secondaryButton" type="button">Buscar</button>
            <button data-role="create" class="primaryButton" type="button">Crear insumo</button>
            <button data-role="remove" class="dangerButton" type="button">Quitar</button>
          </div>
        </div>
        <div class="lookupResults" data-role="results"></div>
        <div class="detailMeta">
          <div>Descripcion<strong data-role="description">-</strong></div>
          <div>Unidad<strong data-role="unit">-</strong></div>
          <div>Valor unitario<strong data-role="cost">-</strong></div>
        </div>
        <div class="lookupState" data-role="status"></div>
      `;
      detailRows.appendChild(card);

      const typeInput = card.querySelector('[data-role="type"]');
      const codeInput = card.querySelector('[data-role="code"]');
      const qtyInput = card.querySelector('[data-role="qty"]');
      const lookupButton = card.querySelector('[data-role="lookup"]');
      const createButton = card.querySelector('[data-role="create"]');
      const removeButton = card.querySelector('[data-role="remove"]');
      const resultsEl = card.querySelector('[data-role="results"]');
      const descriptionEl = card.querySelector('[data-role="description"]');
      const unitEl = card.querySelector('[data-role="unit"]');
      const costEl = card.querySelector('[data-role="cost"]');
      const statusEl = card.querySelector('[data-role="status"]');

      typeInput.value = row.tipo_item;
      codeInput.value = row.codigo_item;
      qtyInput.value = row.cantidad;

      function syncRow() {
        row.tipo_item = typeInput.value;
        row.codigo_item = codeInput.value;
        row.cantidad = qtyInput.value || "1";
      }

      function candidateCode(item) {
        return String(item.codigo_apu || item.codigo || item.code || "").trim();
      }

      function candidateDescription(item) {
        return String(item.descripcion_apu || item.descripcion || item.description || "").trim();
      }

      function candidateUnit(item) {
        return String(item.und || item.unidad || item.unit || "").trim();
      }

      function candidateCost(item) {
        const value =
          item.valor_costo_incluido_iva ??
          item.valor_dia ??
          item.valor_hora_formula ??
          item.costo_total_formula ??
          item.valor_presupuesto_formula ??
          "";
        return typeof value === "number" ? formatCurrency(value) : String(value || "").trim();
      }

      function escapeHtml(value) {
        return String(value)
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/"/g, "&quot;")
          .replace(/'/g, "&#39;");
      }

      function selectSearchItem(item, quiet = false) {
        const code = candidateCode(item);
        const description = candidateDescription(item);
        const unit = candidateUnit(item);
        const cost = candidateCost(item);

        if (code) {
          row.codigo_item = code;
          codeInput.value = code;
        }
        row.descripcion = description || code || "-";
        row.unidad = unit || "-";
        row.costo = cost || "-";
        descriptionEl.textContent = row.descripcion;
        unitEl.textContent = row.unidad;
        costEl.textContent = row.costo;
        row.searchResults = [item];
        row.canCreate = false;
        setText(statusEl, quiet ? "" : "Seleccionado");
        setVisible(createButton, false);
        resultsEl.innerHTML = "";
      }

      function renderSearchResults(items) {
        if (!items.length) {
          resultsEl.innerHTML = "";
          return;
        }

        resultsEl.innerHTML = items
          .map((item, index) => {
            const code = candidateCode(item) || "(sin codigo)";
            const description = candidateDescription(item) || "(sin descripcion)";
            const unit = candidateUnit(item);
            const cost = candidateCost(item);
            return `
              <button class="lookupChoice" type="button" data-index="${index}">
                <strong>${escapeHtml(code)}</strong>
                <small>${escapeHtml(description)}${unit ? " | " + escapeHtml(unit) : ""}${cost ? " | " + escapeHtml(cost) : ""}</small>
              </button>
            `;
          })
          .join("");

        resultsEl.querySelectorAll("[data-index]").forEach((button) => {
          button.addEventListener("click", () => {
            const index = Number(button.getAttribute("data-index"));
            const selected = items[index];
            if (selected) {
              selectSearchItem(selected);
            }
          });
        });
      }

      async function lookupRow() {
        syncRow();
        const term = row.codigo_item.trim();
        row.search = term;
        if (!term) {
          row.searchResults = [];
          row.canCreate = false;
          descriptionEl.textContent = "-";
          unitEl.textContent = "-";
          costEl.textContent = "-";
          setText(statusEl, "");
          setVisible(createButton, false);
          resultsEl.innerHTML = "";
          return;
        }

        const endpoint = row.tipo_item === "MATERIAL"
          ? "/materials?search=" + encodeURIComponent(term) + "&limit=5"
          : row.tipo_item === "LABOR"
            ? "/labor?search=" + encodeURIComponent(term) + "&limit=5"
            : "/crew?search=" + encodeURIComponent(term) + "&limit=5";

        try {
          const response = await request(endpoint);
          row.searchResults = response.items || [];
          row.canCreate = Boolean(response.can_create);
          const exact = row.searchResults.find((item) => {
            const candidate = candidateCode(item);
            const description = candidateDescription(item);
            return (
              candidate.toUpperCase() === term.toUpperCase() ||
              description.toUpperCase() === term.toUpperCase()
            );
          }) || null;

          if (exact) {
            selectSearchItem(exact, true);
            setText(statusEl, "Coincidencia exacta");
          } else if (row.searchResults.length === 1) {
            selectSearchItem(row.searchResults[0], true);
            setText(statusEl, "1 coincidencia");
          } else {
            row.descripcion = "";
            row.unidad = "";
            row.costo = "";
            descriptionEl.textContent = "-";
            unitEl.textContent = "-";
            costEl.textContent = "-";
            setText(
              statusEl,
              row.searchResults.length
                ? row.searchResults.length + " coincidencias. Elige una."
                : "Sin coincidencias",
            );
            renderSearchResults(row.searchResults);
            setVisible(createButton, row.tipo_item !== "CUADRILLA" && row.canCreate && !row.searchResults.length);
          }
        } catch (error) {
          setText(statusEl, error instanceof Error ? error.message : "Error al buscar.");
          setVisible(createButton, false);
          resultsEl.innerHTML = "";
        }
      }

      typeInput.addEventListener("change", async () => {
        syncRow();
        descriptionEl.textContent = "-";
        unitEl.textContent = "-";
        costEl.textContent = "-";
        setText(statusEl, "");
        setVisible(createButton, false);
        await lookupRow();
      });
      codeInput.addEventListener("input", () => {
        syncRow();
        window.clearTimeout(card.__lookupTimer);
        card.__lookupTimer = window.setTimeout(lookupRow, 220);
      });
      qtyInput.addEventListener("input", syncRow);
      lookupButton.addEventListener("click", lookupRow);
      createButton.addEventListener("click", () => {
        syncRow();
        openDialog(row.tipo_item === "CUADRILLA" ? "LABOR" : row.tipo_item, row.id, row.codigo_item || state.builder.descripcion);
      });
      removeButton.addEventListener("click", () => {
        const index = state.builder.details.findIndex((item) => item.id === row.id);
        if (index >= 0) {
          state.builder.details.splice(index, 1);
        }
        card.remove();
        updateBuilderState();
      });

      lookupRow();
      updateBuilderState();
    }

    async function saveApu() {
      showBuilderError("");
      showBuilderSuccess("");
      try {
        syncHeader();
        const details = state.builder.details
          .filter((detail) => detail.codigo_item.trim())
          .map((detail) => ({
            tipo_item: detail.tipo_item,
            codigo_item: detail.codigo_item.trim(),
            cantidad: detail.cantidad || "1",
          }));

        if (!state.builder.descripcion.trim()) {
          throw new Error("La descripcion del APU es obligatoria.");
        }
        if (!state.builder.codigo.trim()) {
          state.builder.codigo = slugCode(state.builder.descripcion);
          apuCodigo.value = state.builder.codigo;
        }
        if (!details.length) {
          throw new Error("Debes agregar al menos un detalle.");
        }

        const payload = {
          codigo_apu: state.builder.codigo.trim(),
          descripcion_apu: state.builder.descripcion.trim(),
          unidad: state.builder.unidad.trim() || "UN",
          detalles: details,
        };

        const result = await request("/apus", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        showBuilderSuccess(
          "APU guardado en fila " + result.header_row + ". Formulas preservadas.",
        );
        await loadApus(apuSearchInput.value);
      } catch (error) {
        showBuilderError(error instanceof Error ? error.message : "Error inesperado.");
      }
    }

    function syncHeader() {
      state.builder.codigo = apuCodigo.value.trim();
      state.builder.descripcion = apuDescripcion.value.trim();
      state.builder.unidad = apuUnidad.value.trim() || "UN";
    }

    async function suggestApuCode() {
      const description = apuDescripcion.value.trim();
      if (!description) return;
      try {
        const query = new URLSearchParams({ description });
        const response = await request("/apus/suggest-code?" + query.toString());
        if (!apuCodigo.value.trim()) {
          apuCodigo.value = response.suggested_code;
        }
        syncHeader();
      } catch (error) {
        console.warn(error);
      }
    }

    function addDefaultRow() {
      createDetailRow();
    }

    async function saveDialogItem() {
      showDialogError("");
      showDialogSuccess("");
      try {
        const payloadBase = {
          codigo: itemCode.value.trim(),
          descripcion: itemDescription.value.trim(),
        };

        if (itemType.value === "MATERIAL") {
          const payload = {
            ...payloadBase,
            marca: itemBrand.value.trim() || null,
            und: itemUnit.value.trim() || "UN",
            factor: percentToDecimal(itemFactor.value),
            valor_costo_incluido_iva: itemCost.value || "0",
          };
          await request("/materials", {
            method: "POST",
            body: JSON.stringify(payload),
          });
        } else {
          const payload = {
            ...payloadBase,
            valor_dia: itemCost.value || "0",
            und: itemUnit.value.trim() || "HR",
          };
          await request("/labor", {
            method: "POST",
            body: JSON.stringify(payload),
          });
        }

        showDialogSuccess("Insumo guardado. Puedes volver al APU sin perder el progreso.");
        if (state.activeDialogRowId) {
          const rowCard = document.getElementById(state.activeDialogRowId);
          if (rowCard) {
            const codeInput = rowCard.querySelector('[data-role="code"]');
            if (codeInput) {
              codeInput.value = itemCode.value.trim();
              codeInput.dispatchEvent(new Event("input"));
            }
            const lookupButton = rowCard.querySelector('[data-role="lookup"]');
            if (lookupButton) {
              lookupButton.click();
            }
          }
        }
        window.setTimeout(closeDialogFn, 700);
      } catch (error) {
        showDialogError(error instanceof Error ? error.message : "Error inesperado.");
      }
    }

    apuSearchInput.addEventListener("input", () => {
      window.clearTimeout(window.__apuSearchTimer);
      const value = apuSearchInput.value;
      window.__apuSearchTimer = window.setTimeout(() => loadApus(value), 250);
    });

    apuDescripcion.addEventListener("input", () => {
      syncHeader();
      window.clearTimeout(window.__apuCodeTimer);
      window.__apuCodeTimer = window.setTimeout(suggestApuCode, 250);
    });
    apuCodigo.addEventListener("input", syncHeader);
    apuUnidad.addEventListener("input", syncHeader);

    addRowButton.addEventListener("click", addDefaultRow);
    saveApuButton.addEventListener("click", saveApu);
    createApuButton.addEventListener("click", () => {
      apuDescripcion.focus();
      window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
    });

    closeDialog.addEventListener("click", closeDialogFn);
    cancelCreate.addEventListener("click", closeDialogFn);
    dialogOverlay.addEventListener("click", closeDialogFn);
    saveItem.addEventListener("click", saveDialogItem);
    itemType.addEventListener("change", updateDialogFields);

    loadApus("");
    addDefaultRow();
    syncHeader();
  </script>
</body>
</html>"""
