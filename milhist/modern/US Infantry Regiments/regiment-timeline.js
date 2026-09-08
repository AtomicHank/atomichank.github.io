"use strict";

// The HTML record is the single data source. Dates are ISO, with exclusive ends.
(() => {
  const list = document.getElementById("period-list");
  if (!list) return;
  const records = [...list.querySelectorAll(".period")].map(element => ({
    element, ...element.dataset,
    title: element.querySelector("h3").textContent.trim(),
    label: element.querySelector(".unit-label").textContent.trim(),
    dates: element.querySelector(".period-date").textContent.trim()
  }));
  const evidence = [...document.querySelectorAll(".battalion-evidence")];
  const filter = document.getElementById("unit-filter");
  const input = document.getElementById("assignment-date");
  const status = document.getElementById("filter-status");
  const results = document.getElementById("date-results");
  const unitNames = { reg: document.querySelector("h1").textContent.trim() };
  for (const option of filter.options) {
    if (!["all", "reg"].includes(option.value)) unitNames[option.value] = option.dataset.label || option.textContent.replace(/^Regiment → /, "").replace(/ - documented service$/, "");
  }
  const units = [...new Set(records.map(record => record.unit))];
  const defaultUnit = filter.value;
  const day = value => Date.parse(value + "T00:00:00Z");
  const min = day(input.min);
  const max = day(input.max) + 86400000;
  const position = value => (day(value) - min) / (max - min) * 100;

  function applyFilter() {
    let count = 0;
    for (const record of records) {
      const visible = filter.value === "all" || record.unit === "reg" || record.unit === filter.value;
      record.element.hidden = !visible;
      if (visible) count++;
    }
    let noteCount = 0;
    for (const element of evidence) {
      element.hidden = filter.value !== "all" && element.dataset.unit !== filter.value;
      if (!element.hidden) noteCount++;
    }
    status.textContent = count + " periods shown" + (noteCount ? " · " + noteCount + " service notes" : "") + " · common regimental history included";
  }
  function reveal(record) {
    filter.value = record.unit === "reg" ? defaultUnit : record.unit;
    applyFilter();
    record.element.tabIndex = -1;
    record.element.focus({ preventScroll: true });
    record.element.scrollIntoView({ block: "start", behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth" });
  }
  function showDate() {
    results.replaceChildren();
    if (!input.value || !input.validity.valid) {
      const p = document.createElement("p");
      p.textContent = "Enter a date from 1 January 1916 through 8 September 2026.";
      results.append(p);
      return;
    }
    const unitOrder = Object.fromEntries(units.map((unit, index) => [unit, index]));
    const matches = records.filter(r => r.start <= input.value && input.value < r.end)
      .sort((a, b) => unitOrder[a.unit] - unitOrder[b.unit]);
    if (!matches.length) {
      const p = document.createElement("p");
      p.textContent = "No dated assignment is established here for this date. See the service notes and source limits below.";
      results.append(p);
    }
    for (const record of matches) {
      const box = document.createElement("div");
      box.className = "date-result " + record.kind;
      const unit = document.createElement("span");
      unit.textContent = record.label;
      const title = document.createElement("strong");
      title.textContent = record.title;
      const dates = document.createElement("span");
      dates.textContent = record.dates;
      const link = document.createElement("a");
      link.href = "#" + record.element.id;
      link.textContent = "Read this period →";
      link.addEventListener("click", event => { event.preventDefault(); reveal(record); });
      box.append(unit, title, dates, link);
      results.append(box);
    }
  }
  function buildChart() {
    const chart = document.getElementById("timeline-chart");
    const axis = document.createElement("div");
    axis.className = "chart-row axis";
    const label = document.createElement("span");
    label.textContent = "Calendar year";
    label.className = "chart-label";
    const ticks = document.createElement("div");
    ticks.className = "chart-track";
    for (const year of [1916, 1930, 1945, 1957, 1970, 1987, 2000, 2015, 2026]) {
      const tick = document.createElement("span");
      tick.className = "axis-tick";
      tick.textContent = year;
      tick.style.left = (year === 2026 ? 100 : position(year + "-01-01")) + "%";
      ticks.append(tick);
    }
    axis.append(label, ticks);
    chart.append(axis);
    for (const unit of units) {
      const row = document.createElement("div");
      row.className = "chart-row";
      const heading = document.createElement("div");
      heading.className = "chart-label";
      heading.textContent = unitNames[unit];
      const track = document.createElement("div");
      track.className = "chart-track";
      for (const record of records.filter(r => r.unit === unit)) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "chart-segment " + record.kind;
        button.style.left = position(record.start) + "%";
        const width = (day(record.end) - day(record.start)) / (max - min) * 100;
        button.style.width = width + "%";
        button.title = record.label + ": " + record.title + " · " + record.dates;
        button.setAttribute("aria-label", button.title);
        if (width > 7) {
          button.textContent = record.short || ({first:"1st ID", eighth:"8th ID", second:"2d ID", airborne:"101st", training:"TRADOC", inactive:"Inactive", reported:"Last reported"})[record.kind] || record.title;
        }
        button.addEventListener("click", () => reveal(record));
        track.append(button);
      }
      const regEnd = records.filter(r => r.unit === "reg").at(-1).end;
      if (unit === "reg" && day(regEnd) < max) {
        const after = document.createElement("span");
        after.className = "chart-after";
        after.style.left = position(regEnd) + "%";
        after.textContent = regEnd.slice(0, 4) + " onward: see separate element rows";
        track.append(after);
      }
      row.append(heading, track);
      chart.append(row);
      const deployments = records.filter(r => r.unit === unit)
        .flatMap(r => [...r.element.querySelectorAll(".deployment")].map(element => ({ element, record: r })));
      if (deployments.length) {
        const deploymentRow = document.createElement("div");
        deploymentRow.className = "chart-row deployment-row";
        const deploymentLabel = document.createElement("span");
        deploymentLabel.className = "chart-label";
        deploymentLabel.textContent = "Deployments / operations";
        const deploymentTrack = document.createElement("div");
        deploymentTrack.className = "chart-track deployment-track";
        deployments.forEach(({ element, record }, index) => {
          const marker = document.createElement("button");
          marker.type = "button";
          marker.className = "deployment-marker";
          marker.style.left = position(element.dataset.year + "-07-01") + "%";
          marker.style.top = (index % 2 ? 37 : 3) + "px";
          marker.textContent = "\u25c6";
          marker.title = element.querySelector("h5").textContent + " - " + element.querySelector(".deployment-date").textContent;
          marker.setAttribute("aria-label", marker.title);
          marker.addEventListener("click", () => reveal({ ...record, element }));
          deploymentTrack.append(marker);
        });
        deploymentRow.append(deploymentLabel, deploymentTrack);
        chart.append(deploymentRow);
      }
    }
  }
  for (const element of evidence) {
    const row = document.createElement("div");
    row.className = "chart-row";
    const heading = document.createElement("span");
    heading.className = "chart-label";
    heading.textContent = unitNames[element.dataset.unit] || element.querySelector("h2").textContent;
    const link = document.createElement("a");
    link.className = "chart-evidence";
    link.href = "#" + element.id;
    link.textContent = "Documented service - dates incomplete - view entry →";
    row.append(heading, link);
    // Added after the dated chart is built below.
    element.chartRow = row;
  }
  document.addEventListener("click", event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link) return;
    const record = records.find(r => "#" + r.element.id === link.hash);
    if (record && record.element.hidden) { filter.value = record.unit === "reg" ? defaultUnit : record.unit; applyFilter(); }
    const note = evidence.find(e => "#" + e.id === link.hash);
    if (note) { filter.value = note.dataset.unit; applyFilter(); }
    const deployment = document.getElementById(link.hash.slice(1));
    if (deployment?.classList.contains("deployment")) {
      const parent = records.find(r => r.element.contains(deployment));
      if (parent) { filter.value = parent.unit === "reg" ? defaultUnit : parent.unit; applyFilter(); }
    }
  });
  filter.addEventListener("change", applyFilter);
  input.addEventListener("change", showDate);
  document.getElementById("latest-date").addEventListener("click", () => { input.value = input.max; showDate(); });
  buildChart();
  for (const element of evidence) document.getElementById("timeline-chart").append(element.chartRow);
  applyFilter();
  showDate();
  for (const id of ["overview", "date-explorer", "timeline-controls"]) document.getElementById(id).hidden = false;
  // A direct period bookmark must also reveal a record hidden by the default filter.
  const bookmarked = records.find(r => "#" + r.element.id === location.hash);
  const noteBookmark = evidence.find(e => "#" + e.id === location.hash);
  if (noteBookmark) { filter.value = noteBookmark.dataset.unit; applyFilter(); }
  if (bookmarked) { filter.value = bookmarked.unit === "reg" ? defaultUnit : bookmarked.unit; applyFilter(); }
  const deploymentBookmark = document.getElementById(location.hash.slice(1));
  if (deploymentBookmark?.classList.contains("deployment")) {
    const parent = records.find(r => r.element.contains(deploymentBookmark));
    if (parent) { filter.value = parent.unit === "reg" ? defaultUnit : parent.unit; applyFilter(); }
  }
})();
