import { useState } from "react";

import { ApusPage } from "../features/apus/ApusPage";
import { BudgetPage } from "../features/budget/BudgetPage";
import { MaterialsPage } from "../features/materials/MaterialsPage";

type AppSection = "materials" | "apus" | "budget";

export function App() {
  const [section, setSection] = useState<AppSection>("materials");

  return (
    <>
      <nav className="appNav" aria-label="Navegacion principal">
        <button
          className={section === "materials" ? "active" : ""}
          type="button"
          onClick={() => setSection("materials")}
        >
          Materiales
        </button>
        <button
          className={section === "apus" ? "active" : ""}
          type="button"
          onClick={() => setSection("apus")}
        >
          APUs
        </button>
        <button
          className={section === "budget" ? "active" : ""}
          type="button"
          onClick={() => setSection("budget")}
        >
          Presupuesto
        </button>
      </nav>
      {section === "materials" ? <MaterialsPage /> : null}
      {section === "apus" ? <ApusPage /> : null}
      {section === "budget" ? <BudgetPage /> : null}
    </>
  );
}
