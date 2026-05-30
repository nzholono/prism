"""Prism GUI — Tkinter desktop client.

Run with `uv run prism-gui`. Requires Pharos to be running.

Layout: left tree of domains/scenarios, right pane with content and a tab for
the decision journal.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from prism.api_client import ApiClient, PharosUnavailable
from prism.models import DecisionCreate


class PrismGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Prism — Illinois legal & ethical reasoning")
        self.root.geometry("1100x700")

        try:
            self.client = ApiClient()
            self.client.health()
        except PharosUnavailable as exc:
            messagebox.showerror("Pharos unavailable", str(exc))
            root.destroy()
            return

        self._build_ui()
        self._load_domains()

    def _build_ui(self) -> None:
        toolbar = ttk.Frame(self.root, padding=4)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        ttk.Button(toolbar, text="Search", command=self._search).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="New decision", command=self._new_decision).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Ethics", command=self._ethics).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Decisions", command=self._list_decisions).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Stats", command=self._stats).pack(side=tk.LEFT)

        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        left = ttk.Frame(paned)
        paned.add(left, weight=1)
        ttk.Label(left, text="Domains & scenarios", font=("", 11, "bold")).pack(anchor="w")
        self.tree = ttk.Treeview(left, show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        right = ttk.Frame(paned)
        paned.add(right, weight=3)
        self.text = tk.Text(right, wrap=tk.WORD, font=("Helvetica", 12))
        scroll = ttk.Scrollbar(right, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.tag_configure("h1", font=("Helvetica", 18, "bold"), spacing3=8)
        self.text.tag_configure("h2", font=("Helvetica", 14, "bold"), spacing3=6)
        self.text.tag_configure("bias", background="#fff8dc", foreground="#a05a00")
        self.text.tag_configure("citation", foreground="#2980b9", font=("Menlo", 11))

    def _load_domains(self) -> None:
        domains = self.client.list_domains()
        for d in domains:
            domain_id = self.tree.insert("", tk.END, text=d.name, values=("domain", d.slug))
            detail = self.client.get_domain(d.slug)
            for sc in detail.scenarios:
                self.tree.insert(
                    domain_id, tk.END, text=f"  {sc.title}", values=("scenario", sc.slug)
                )

    def _on_tree_select(self, _event=None) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        if not values:
            return
        kind, slug = values
        if kind == "scenario":
            sc = self.client.get_scenario(slug)
            self._show_scenario(sc)
        else:
            d = self.client.get_domain(slug)
            self._show_domain(d)

    def _show_domain(self, d) -> None:
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, f"{d.name}\n", "h1")
        self.text.insert(tk.END, f"{d.summary}\n\n")
        if d.statutes:
            self.text.insert(tk.END, "Statutes\n", "h2")
            for st in d.statutes:
                self.text.insert(tk.END, f"  {st.citation}", "citation")
                self.text.insert(tk.END, f" — {st.title}\n  {st.summary}\n\n")
        self.text.config(state=tk.DISABLED)

    def _show_scenario(self, sc) -> None:
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, f"{sc.title}\n", "h1")
        self.text.insert(tk.END, f"{sc.description_md}\n\n")
        self.text.insert(tk.END, f"{sc.walkthrough_md}\n")
        if sc.statutes:
            self.text.insert(tk.END, "\nApplicable statutes\n", "h2")
            for st in sc.statutes:
                self.text.insert(tk.END, f"  {st.citation}", "citation")
                self.text.insert(tk.END, f" — {st.title}\n")
        if sc.template_md:
            self.text.insert(tk.END, f"\n{sc.template_md}\n")
        self.text.config(state=tk.DISABLED)

    def _search(self) -> None:
        q = simpledialog.askstring("Search", "Search for:")
        if not q:
            return
        hits = self.client.search(q)
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, f"Search: '{q}'\n", "h1")
        if not hits:
            self.text.insert(tk.END, "No matches.\n")
        for h in hits:
            self.text.insert(tk.END, f"[{h.kind}] {h.title} ({h.domain_slug})\n")
            self.text.insert(tk.END, f"   {h.snippet}\n\n")
        self.text.config(state=tk.DISABLED)

    def _ethics(self) -> None:
        situation = simpledialog.askstring(
            "Ethics analysis", "Describe the situation in one sentence:"
        )
        if not situation:
            return
        analysis = self.client.analyze_ethically(situation)
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, "Ethical analysis\n", "h1")
        self.text.insert(tk.END, f"{analysis.situation}\n\n")
        for p in analysis.perspectives:
            self.text.insert(tk.END, f"{p.framework_name}\n", "h2")
            self.text.insert(tk.END, f"{p.framing}\n\nKey questions:\n")
            for q in p.questions:
                self.text.insert(tk.END, f"  • {q}\n")
            self.text.insert(tk.END, "\n")
        self.text.config(state=tk.DISABLED)

    def _new_decision(self) -> None:
        dlg = NewDecisionDialog(self.root)
        self.root.wait_window(dlg.top)
        if not dlg.result:
            return
        try:
            decision = self.client.create_decision(DecisionCreate(**dlg.result))
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Error", str(exc))
            return
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, f"Decision #{decision.id} logged\n", "h1")
        self.text.insert(tk.END, f"Chose: {decision.chosen}\n")
        self.text.insert(tk.END, f"Confidence: {decision.confidence}\n\n")
        if decision.biases:
            self.text.insert(tk.END, "Bias flags:\n", "h2")
            for b in decision.biases:
                self.text.insert(tk.END, f"  [{b.bias_slug}] {b.evidence}\n\n", "bias")
        else:
            self.text.insert(tk.END, "No bias flags raised.\n")
        self.text.config(state=tk.DISABLED)

    def _list_decisions(self) -> None:
        decisions = self.client.list_decisions()
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, "Decision journal\n", "h1")
        if not decisions:
            self.text.insert(tk.END, "No decisions yet. Click 'New decision' to log one.\n")
        for d in decisions:
            self.text.insert(
                tk.END,
                f"#{d.id} ({d.created_at.strftime('%Y-%m-%d')}): {d.situation}\n",
                "h2",
            )
            self.text.insert(
                tk.END,
                f"  Chose: {d.chosen} (confidence {d.confidence})\n",
            )
            biases = ", ".join(b.bias_slug for b in d.biases) or "—"
            self.text.insert(tk.END, f"  Biases: {biases}\n")
            outcome = d.actual_outcome or "(not yet reviewed)"
            self.text.insert(tk.END, f"  Outcome: {outcome}\n\n")
        self.text.config(state=tk.DISABLED)

    def _stats(self) -> None:
        s = self.client.stats()
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, "Stats\n", "h1")
        self.text.insert(
            tk.END,
            f"  Domains:   {s.domains}\n  Statutes:  {s.statutes}\n"
            f"  Scenarios: {s.scenarios}\n  Decisions: {s.decisions}\n"
            f"  Bias flags raised: {s.bias_flags}\n",
        )
        self.text.config(state=tk.DISABLED)


class NewDecisionDialog:
    def __init__(self, parent: tk.Tk) -> None:
        self.result: dict | None = None
        self.top = tk.Toplevel(parent)
        self.top.title("New decision")
        self.top.geometry("520x520")

        def labeled(label: str) -> tk.Entry:
            ttk.Label(self.top, text=label).pack(anchor="w", padx=10, pady=(8, 0))
            entry = tk.Entry(self.top, width=70)
            entry.pack(padx=10, pady=2, fill=tk.X)
            return entry

        self.situation = labeled("Situation:")
        self.options = labeled("Options (comma-separated):")
        self.chosen = labeled("Chose:")
        ttk.Label(self.top, text="Reasoning:").pack(anchor="w", padx=10, pady=(8, 0))
        self.reasoning = tk.Text(self.top, height=4)
        self.reasoning.pack(padx=10, pady=2, fill=tk.X)
        self.expected = labeled("Expected outcome:")
        self.confidence = labeled("Confidence (0–100):")
        self.confidence.insert(0, "60")

        btns = ttk.Frame(self.top)
        btns.pack(pady=10)
        ttk.Button(btns, text="Save", command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Cancel", command=self.top.destroy).pack(side=tk.LEFT, padx=5)

    def _save(self) -> None:
        opts = [o.strip() for o in self.options.get().split(",") if o.strip()]
        if len(opts) < 2:
            messagebox.showerror("Error", "Need at least 2 options.")
            return
        try:
            confidence = int(self.confidence.get())
        except ValueError:
            messagebox.showerror("Error", "Confidence must be an integer 0–100.")
            return
        self.result = {
            "situation": self.situation.get(),
            "options": opts,
            "chosen": self.chosen.get(),
            "reasoning": self.reasoning.get("1.0", tk.END).strip(),
            "expected_outcome": self.expected.get(),
            "confidence": confidence,
        }
        self.top.destroy()


def main() -> None:
    root = tk.Tk()
    PrismGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
