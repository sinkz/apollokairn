const state = {
  lang: localStorage.getItem("cairn-lang") || "en",
  benchmark: null,
};

const text = {
  en: {
    updated: "Updated",
    suite: "Deterministic search benchmark",
    benchmarkUnavailable: "Benchmark data could not be loaded.",
    history: "History",
    metric: "Metric",
    date: "Date",
    label: "Label",
    shortHistory: "Trend chart appears after three benchmark runs. Current snapshot:",
  },
  pt: {
    updated: "Atualizado",
    suite: "Benchmark determinístico de busca",
    benchmarkUnavailable: "Não foi possível carregar os dados de benchmark.",
    history: "Histórico",
    metric: "Métrica",
    date: "Data",
    label: "Rótulo",
    shortHistory: "O gráfico de tendência aparece após três rodadas de benchmark. Snapshot atual:",
  },
};

function activeLang() {
  return state.lang === "pt" ? "pt" : "en";
}

function localized(value, lang) {
  if (typeof value === "string") return value;
  if (value && typeof value === "object") {
    return value[lang] || value.en || value.pt || "";
  }
  return "";
}

function setLanguage(lang) {
  state.lang = lang === "pt" ? "pt" : "en";
  localStorage.setItem("cairn-lang", state.lang);
  document.body.dataset.lang = state.lang;
  document.documentElement.lang = state.lang === "pt" ? "pt-BR" : "en";

  document.querySelectorAll("[data-set-lang]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.setLang === state.lang));
  });

  renderBenchmark();
}

function formatMetric(metric, lang, value = metric.value) {
  const precision = Number(metric.precision || 0);
  if (metric.format === "percent") {
    return new Intl.NumberFormat(lang === "pt" ? "pt-BR" : "en-US", {
      style: "percent",
      minimumFractionDigits: precision,
      maximumFractionDigits: precision,
    }).format(value);
  }

  if (metric.format === "integer") {
    return new Intl.NumberFormat(lang === "pt" ? "pt-BR" : "en-US", {
      maximumFractionDigits: 0,
    }).format(value);
  }

  return new Intl.NumberFormat(lang === "pt" ? "pt-BR" : "en-US", {
    minimumFractionDigits: precision,
    maximumFractionDigits: precision,
  }).format(value);
}

function benchmarkSuites(data) {
  if (Array.isArray(data?.suites)) return data.suites;
  if (!data) return [];
  return [
    {
      id: "retrieval",
      suite: {
        name: { en: text.en.suite, pt: text.pt.suite },
        command: data.suite?.command || "",
        notes: data.suite?.notes || {},
      },
      current: data.current,
      history: data.history || [],
      history_metrics: ["recall_at_3", "ndcg_at_3", "context_reduction"],
    },
  ];
}

function metricDefinitions(suite) {
  const out = new Map();
  (suite.current?.metrics || []).forEach((metric) => out.set(metric.id, metric));
  return out;
}

function findSuiteMetric(suites, suiteId, metricId) {
  const suite = suites.find((item) => item.id === suiteId);
  return (suite?.current?.metrics || []).find((metric) => metric.id === metricId);
}

function benchmarkPreviewMetrics(data, suites) {
  return [
    findSuiteMetric(suites, "retrieval", "recall_at_3"),
    findSuiteMetric(suites, "retrieval", "context_reduction"),
    findSuiteMetric(suites, "writeback", "decision_accuracy"),
    (data.current?.metrics || []).find((metric) => metric.id === "tests"),
  ].filter(Boolean);
}

function renderMetricCard(metric, lang) {
  const article = document.createElement("article");
  article.className = "metric-card";

  const label = document.createElement("span");
  label.textContent = localized(metric.label, lang);

  const value = document.createElement("strong");
  value.textContent = formatMetric(metric, lang);

  const description = document.createElement("p");
  description.textContent = localized(metric.description, lang);

  article.append(label, value, description);
  return article;
}

function renderSuite(suite, lang) {
  const section = document.createElement("article");
  section.className = "benchmark-suite-card";

  const heading = document.createElement("div");
  heading.className = "suite-heading";

  const label = document.createElement("p");
  label.className = "panel-label";
  label.textContent = localized(suite.suite?.name, lang);

  const title = document.createElement("h3");
  title.textContent = localized(suite.current?.label, lang);

  const note = document.createElement("p");
  note.className = "panel-note";
  note.textContent = localized(suite.suite?.notes, lang);

  heading.append(label, title, note);

  const command = document.createElement("code");
  command.textContent = suite.suite?.command || "";

  const metrics = document.createElement("div");
  metrics.className = "metric-grid";
  metrics.append(...(suite.current?.metrics || []).map((metric) => renderMetricCard(metric, lang)));

  section.append(heading, command, metrics);
  return section;
}

function svgElement(name) {
  return document.createElementNS("http://www.w3.org/2000/svg", name);
}

function metricScale(metric, values) {
  if (metric?.format === "percent" || metric?.format === "decimal") return 1;
  return Math.max(1, ...values);
}

function renderHistoryChart(suite, lang) {
  const metrics = metricDefinitions(suite);
  const history = suite.history || [];
  const ids = suite.history_metrics || [];
  const colors = ["#0f6b5b", "#285da8", "#bd4f3d", "#a16207"];
  const svg = svgElement("svg");
  svg.setAttribute("class", "history-chart");
  svg.setAttribute("viewBox", "0 0 360 214");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-labelledby", `chart-title-${suite.id} chart-desc-${suite.id}`);

  const title = svgElement("title");
  title.setAttribute("id", `chart-title-${suite.id}`);
  title.textContent = `${localized(suite.current?.label, lang)} ${text[lang].history}`;
  const desc = svgElement("desc");
  desc.setAttribute("id", `chart-desc-${suite.id}`);
  desc.textContent = localized(suite.suite?.notes, lang);
  svg.append(title, desc);

  const axis = svgElement("path");
  axis.setAttribute("d", "M36 150H342M36 26V150");
  axis.setAttribute("fill", "none");
  axis.setAttribute("stroke", "rgba(21,19,15,0.35)");
  axis.setAttribute("stroke-width", "1.5");
  svg.append(axis);

  ids.forEach((id, index) => {
    const metric = metrics.get(id);
    if (!metric || history.length === 0) return;
    const rawValues = history.map((item) => Number(item[id] || 0));
    const scale = metricScale(metric, rawValues);
    const points = rawValues.map((value, pointIndex) => {
      const x = history.length === 1 ? 188 : 44 + (pointIndex * 286) / (history.length - 1);
      const y = 150 - (Math.min(value / scale, 1) * 112);
      return { x, y, value };
    });
    const color = colors[index % colors.length];

    if (points.length > 1) {
      const polyline = svgElement("polyline");
      polyline.setAttribute("points", points.map((point) => `${point.x},${point.y}`).join(" "));
      polyline.setAttribute("fill", "none");
      polyline.setAttribute("stroke", color);
      polyline.setAttribute("stroke-width", "3");
      svg.append(polyline);
    }

    points.forEach((point) => {
      const circle = svgElement("circle");
      circle.setAttribute("cx", String(point.x));
      circle.setAttribute("cy", String(point.y));
      circle.setAttribute("r", "4");
      circle.setAttribute("fill", color);
      svg.append(circle);
    });

    const legend = svgElement("text");
    legend.setAttribute("x", "44");
    legend.setAttribute("y", String(172 + index * 14));
    legend.setAttribute("fill", color);
    legend.setAttribute("font-size", "10");
    legend.textContent = `${localized(metric.label, lang)} ${formatMetric(metric, lang, rawValues[rawValues.length - 1] || 0)}`;
    svg.append(legend);
  });

  return svg;
}

function renderHistorySnapshot(suite, lang) {
  const metrics = metricDefinitions(suite);
  const history = suite.history || [];
  const ids = suite.history_metrics || [];
  const latest = history[history.length - 1] || {};
  const panel = document.createElement("div");
  panel.className = "history-snapshot";

  const note = document.createElement("p");
  note.className = "history-snapshot-note";
  note.textContent = text[lang].shortHistory;
  panel.append(note);

  ids.forEach((id) => {
    const metric = metrics.get(id);
    if (!metric) return;
    const item = document.createElement("div");
    item.className = "history-snapshot-item";

    const label = document.createElement("span");
    label.textContent = localized(metric.label, lang);

    const value = document.createElement("strong");
    value.textContent = formatMetric(metric, lang, Number(latest[id] || 0));

    item.append(label, value);
    panel.append(item);
  });

  return panel;
}

function renderHistoryVisual(suite, lang) {
  const history = suite.history || [];
  if (history.length < 3) return renderHistorySnapshot(suite, lang);
  return renderHistoryChart(suite, lang);
}

function renderHistoryTable(suite, lang) {
  const metrics = metricDefinitions(suite);
  const ids = suite.history_metrics || [];
  const table = document.createElement("table");
  table.className = "history-table";

  const thead = document.createElement("thead");
  const headRow = document.createElement("tr");
  [text[lang].date, text[lang].label, ...ids.map((id) => localized(metrics.get(id)?.label, lang))].forEach((heading) => {
    const th = document.createElement("th");
    th.textContent = heading;
    headRow.append(th);
  });
  thead.append(headRow);

  const tbody = document.createElement("tbody");
  (suite.history || []).forEach((row) => {
    const tr = document.createElement("tr");
    const date = document.createElement("td");
    date.textContent = row.date || "";
    const label = document.createElement("td");
    label.textContent = row.label || "";
    tr.append(date, label);
    ids.forEach((id) => {
      const td = document.createElement("td");
      const metric = metrics.get(id);
      td.textContent = metric ? formatMetric(metric, lang, Number(row[id] || 0)) : String(row[id] || "");
      tr.append(td);
    });
    tbody.append(tr);
  });

  table.append(thead, tbody);
  return table;
}

function renderHistory(suite, lang) {
  const article = document.createElement("article");
  article.className = "history-card";

  const heading = document.createElement("h3");
  heading.textContent = `${localized(suite.current?.label, lang)} - ${text[lang].history}`;

  article.append(heading, renderHistoryVisual(suite, lang), renderHistoryTable(suite, lang));
  return article;
}

function renderBenchmark() {
  const lang = activeLang();
  const labels = text[lang];
  const data = state.benchmark;
  const suiteContainer = document.getElementById("benchmark-suites");
  const historyContainer = document.getElementById("benchmark-history");
  const legacyCards = document.getElementById("benchmark-cards");
  const previewCards = document.getElementById("benchmark-preview-cards");

  if (!suiteContainer && !legacyCards && !previewCards) return;
  if (!data) return;

  const suites = benchmarkSuites(data);
  const first = suites[0];

  if (first) {
    const suiteLabel = document.getElementById("benchmark-suite");
    const currentLabel = document.getElementById("benchmark-current-label");
    const note = document.getElementById("benchmark-note");
    const command = document.getElementById("benchmark-command");
    const updated = document.getElementById("benchmark-updated");
    if (suiteLabel) suiteLabel.textContent = localized(first.suite?.name, lang);
    if (currentLabel) currentLabel.textContent = localized(first.current?.label, lang);
    if (note) note.textContent = localized(first.suite?.notes, lang);
    if (command) command.textContent = first.suite?.command || "";
    if (updated) updated.textContent = `${labels.updated} ${data.updated_at}`;
  }

  if (suiteContainer) {
    suiteContainer.replaceChildren(...suites.map((suite) => renderSuite(suite, lang)));
  } else if (legacyCards && first) {
    legacyCards.replaceChildren(...(first.current?.metrics || []).map((metric) => renderMetricCard(metric, lang)));
  }

  if (previewCards) {
    previewCards.replaceChildren(...benchmarkPreviewMetrics(data, suites).map((metric) => renderMetricCard(metric, lang)));
  }

  if (historyContainer) {
    historyContainer.replaceChildren(...suites.map((suite) => renderHistory(suite, lang)));
  }
}

async function loadBenchmark() {
  try {
    const response = await fetch("data/benchmarks.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.benchmark = await response.json();
    renderBenchmark();
  } catch (error) {
    const target = document.getElementById("benchmark-suites")
      || document.getElementById("benchmark-preview-cards")
      || document.getElementById("benchmark-cards");
    if (target) {
      target.replaceChildren();
      const article = document.createElement("article");
      article.className = "metric-card";
      const label = document.createElement("span");
      label.textContent = "Benchmark";
      const value = document.createElement("strong");
      value.textContent = "--";
      const description = document.createElement("p");
      description.textContent = text[activeLang()].benchmarkUnavailable;
      article.append(label, value, description);
      target.append(article);
    }
  }
}

document.querySelectorAll("[data-set-lang]").forEach((button) => {
  button.addEventListener("click", () => setLanguage(button.dataset.setLang));
});

function activateTab(target) {
  document.querySelectorAll("[data-tab-target]").forEach((button) => {
    button.setAttribute("aria-selected", String(button.dataset.tabTarget === target));
  });

  document.querySelectorAll("[data-tab-panel]").forEach((panel) => {
    panel.hidden = panel.dataset.tabPanel !== target;
  });
}

document.querySelectorAll("[data-tab-target]").forEach((button) => {
  button.addEventListener("click", () => activateTab(button.dataset.tabTarget));
});

const selectedTab = document.querySelector('[data-tab-target][aria-selected="true"]');
if (selectedTab) {
  activateTab(selectedTab.dataset.tabTarget);
}

setLanguage(state.lang);
loadBenchmark();
