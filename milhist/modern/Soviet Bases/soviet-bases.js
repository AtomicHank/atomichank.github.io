(function () {
  var DATA_PATH = "./soviet-bases-data.json";
  var dataPromise = null;

  document.addEventListener("DOMContentLoaded", function () {
    loadData()
      .then(function (data) {
        enhanceBases(data);
        renderSummary(data);

        if (document.getElementById("base-map")) {
          initMapPage(data);
        }

        if (document.getElementById("base-list")) {
          initListPage(data);
        }
      })
      .catch(function (error) {
        console.error("Soviet Bases data load failed:", error);
        renderLoadErrors();
      });
  });

  function loadData() {
    if (!dataPromise) {
      dataPromise = fetch(DATA_PATH).then(function (response) {
        if (!response.ok) {
          throw new Error("HTTP " + response.status + " loading Soviet base data");
        }
        return response.json();
      });
    }

    return dataPromise;
  }

  function enhanceBases(data) {
    if (data._enhanced) {
      return;
    }

    data.bases.forEach(function (base) {
      base.searchText = [
        base.name,
        base.locationName,
        base.hostCountry,
        base.operatorCountry,
        (base.militaryDistricts || []).join(" "),
        (base.armies || []).join(" "),
        (base.corps || []).join(" "),
        (base.divisions || []).join(" "),
        (base.regiments || []).join(" "),
        (base.formations || []).join(" "),
        (base.formationTypes || []).map(function (item) {
          return item.name;
        }).join(" ")
      ]
        .join(" ")
        .toLowerCase();
    });

    data._enhanced = true;
  }

  function renderSummary(data) {
    Array.from(document.querySelectorAll("[data-summary]")).forEach(function (node) {
      var key = node.getAttribute("data-summary");
      if (key && Object.prototype.hasOwnProperty.call(data.summary, key)) {
        node.textContent = String(data.summary[key]);
      }
    });
  }

  function initMapPage(data) {
    var mapElement = document.getElementById("base-map");
    var mapStatus = document.getElementById("base-map-status");
    var searchInput = document.getElementById("map-search");
    var hostSelect = document.getElementById("map-host-filter");
    var mdSelect = document.getElementById("map-md-filter");
    var resultCount = document.getElementById("map-result-count");
    var directory = document.getElementById("base-directory");
    var detailTitle = document.getElementById("base-detail-title");
    var detailMeta = document.getElementById("base-detail-meta");
    var detailBody = document.getElementById("base-detail-body");

    populateSelect(hostSelect, data.filters.hostCountries, "All host countries");
    populateSelect(mdSelect, data.filters.militaryDistricts, "All districts");

    var mappedBases = data.bases.filter(function (base) {
      return base.latitude !== null && base.longitude !== null;
    });
    var markerIndex = new Map();
    var map = L.map(mapElement).setView([55.0, 40.0], 4);

    L.tileLayer(
      "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
      {
        attribution: "Tiles (c) Esri"
      }
    ).addTo(map);

    var layerGroup = L.layerGroup().addTo(map);
    var state = {
      map: map,
      layerGroup: layerGroup,
      bases: mappedBases,
      filteredBases: [],
      markerIndex: markerIndex,
      selectedId: null,
      search: "",
      host: "",
      militaryDistrict: "",
      directory: directory,
      detailTitle: detailTitle,
      detailMeta: detailMeta,
      detailBody: detailBody,
      resultCount: resultCount
    };

    searchInput.addEventListener("input", function (event) {
      state.search = event.target.value.trim().toLowerCase();
      applyMapFilters(state, false);
    });

    hostSelect.addEventListener("change", function (event) {
      state.host = event.target.value;
      applyMapFilters(state, true);
    });

    mdSelect.addEventListener("change", function (event) {
      state.militaryDistrict = event.target.value;
      applyMapFilters(state, true);
    });

    applyMapFilters(state, true);
    hideMapStatus(mapStatus);

    var hashTarget = decodeURIComponent((window.location.hash || "").replace(/^#/, ""));
    if (hashTarget) {
      var hashBase = mappedBases.find(function (base) {
        return base.id === hashTarget;
      });
      if (hashBase) {
        selectMapBase(state, hashBase.id, true, true);
      }
    }
  }

  function applyMapFilters(state, fitBounds) {
    state.filteredBases = filterBases(state.bases, state.search, state.host, state.militaryDistrict);
    state.layerGroup.clearLayers();

    if (!state.filteredBases.length) {
      state.resultCount.textContent = "No bases match the current filters.";
      state.directory.innerHTML = "<div class=\"empty-state\">No mapped bases match the current filters.</div>";
      renderEmptyDetail(state.detailTitle, state.detailMeta, state.detailBody, "No base selected.");
      return;
    }

    state.filteredBases.forEach(function (base) {
      var marker = state.markerIndex.get(base.id);
      if (!marker) {
        marker = createBaseMarker(base, state);
        state.markerIndex.set(base.id, marker);
      }
      state.layerGroup.addLayer(marker);
    });

    renderDirectory(state);
    state.resultCount.textContent =
      state.filteredBases.length + (state.filteredBases.length === 1 ? " mapped base" : " mapped bases");

    var selectedStillVisible = state.filteredBases.some(function (base) {
      return base.id === state.selectedId;
    });

    if (!selectedStillVisible) {
      selectMapBase(state, state.filteredBases[0].id, false, false);
    } else {
      updateDirectoryActiveState(state);
      renderDetail(state.detailTitle, state.detailMeta, state.detailBody, getBaseById(state.bases, state.selectedId));
    }

    if (fitBounds) {
      fitMapToBases(state.map, state.filteredBases);
    }
  }

  function createBaseMarker(base, state) {
    var marker = L.circleMarker([base.latitude, base.longitude], {
      radius: getBaseRadius(base.rowCount),
      fillColor: "#ef4444",
      color: "#111827",
      weight: 1.2,
      opacity: 1,
      fillOpacity: 0.86
    });

    marker.bindPopup(buildPopupHtml(base), { maxWidth: 280 });
    marker.on("click", function () {
      selectMapBase(state, base.id, false, false);
    });

    return marker;
  }

  function selectMapBase(state, baseId, panToBase, openPopup) {
    var base = getBaseById(state.bases, baseId);
    if (!base) {
      return;
    }

    state.selectedId = baseId;
    updateDirectoryActiveState(state);
    renderDetail(state.detailTitle, state.detailMeta, state.detailBody, base);

    if (panToBase) {
      state.map.flyTo([base.latitude, base.longitude], Math.max(state.map.getZoom(), 6), { duration: 0.65 });
    }

    var marker = state.markerIndex.get(base.id);
    if (openPopup && marker) {
      marker.openPopup();
    }

    if (window.history && window.history.replaceState) {
      window.history.replaceState(null, "", "#" + encodeURIComponent(base.id));
    } else {
      window.location.hash = base.id;
    }
  }

  function renderDirectory(state) {
    state.directory.innerHTML = "";
    var fragment = document.createDocumentFragment();

    state.filteredBases.forEach(function (base) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "directory-item";
      button.classList.toggle("is-active", base.id === state.selectedId);
      button.setAttribute("data-base-id", base.id);
      button.innerHTML =
        "<span class=\"directory-title\">" +
        escapeHtml(base.name) +
        "</span>" +
        "<span class=\"directory-meta\">" +
        escapeHtml(buildBaseMeta(base)) +
        "</span>";

      button.addEventListener("click", function () {
        selectMapBase(state, base.id, true, true);
      });

      fragment.appendChild(button);
    });

    state.directory.appendChild(fragment);
  }

  function updateDirectoryActiveState(state) {
    Array.from(state.directory.querySelectorAll("[data-base-id]")).forEach(function (button) {
      button.classList.toggle("is-active", button.getAttribute("data-base-id") === state.selectedId);
    });
  }

  function fitMapToBases(map, bases) {
    var bounds = L.latLngBounds(
      bases.map(function (base) {
        return [base.latitude, base.longitude];
      })
    );
    map.fitBounds(bounds.pad(0.12), { maxZoom: 7 });
  }

  function initListPage(data) {
    var searchInput = document.getElementById("list-search");
    var hostSelect = document.getElementById("list-host-filter");
    var mdSelect = document.getElementById("list-md-filter");
    var resultCount = document.getElementById("list-result-count");
    var listRoot = document.getElementById("base-list");
    var state = {
      bases: data.bases,
      filteredBases: [],
      search: "",
      host: "",
      militaryDistrict: "",
      resultCount: resultCount,
      listRoot: listRoot
    };

    populateSelect(hostSelect, data.filters.hostCountries, "All host countries");
    populateSelect(mdSelect, data.filters.militaryDistricts, "All districts");

    searchInput.addEventListener("input", function (event) {
      state.search = event.target.value.trim().toLowerCase();
      renderListCards(state);
    });

    hostSelect.addEventListener("change", function (event) {
      state.host = event.target.value;
      renderListCards(state);
    });

    mdSelect.addEventListener("change", function (event) {
      state.militaryDistrict = event.target.value;
      renderListCards(state);
    });

    renderListCards(state);
  }

  function renderListCards(state) {
    state.filteredBases = filterBases(state.bases, state.search, state.host, state.militaryDistrict);
    state.resultCount.textContent =
      state.filteredBases.length + (state.filteredBases.length === 1 ? " base" : " bases");

    if (!state.filteredBases.length) {
      state.listRoot.innerHTML = "<div class=\"empty-state\">No bases match the current filters.</div>";
      return;
    }

    state.listRoot.innerHTML = state.filteredBases
      .map(function (base) {
        return (
          "<article class=\"base-card\">" +
          "<h2 class=\"base-card-title\">" +
          escapeHtml(base.name) +
          "</h2>" +
          "<p class=\"base-card-meta\">" +
          escapeHtml(buildBaseMeta(base)) +
          "</p>" +
          "<p class=\"base-card-copy\">" +
          escapeHtml(buildBaseCardSummary(base)) +
          "</p>" +
          buildTagGroup(base) +
          "<div class=\"base-card-links\">" +
          (base.latitude !== null && base.longitude !== null
            ? "<a class=\"base-link\" href=\"refmap.html#" + encodeURIComponent(base.id) + "\">Open on map</a>"
            : "") +
          "<a class=\"base-link\" href=\"Soviet Force Structure 1989.xlsx\">Workbook</a>" +
          "</div>" +
          "</article>"
        );
      })
      .join("");
  }

  function buildTagGroup(base) {
    var tags = [];

    if (base.hostCountry) {
      tags.push(base.hostCountry);
    }
    if (base.militaryDistricts && base.militaryDistricts.length) {
      tags = tags.concat(base.militaryDistricts.slice(0, 2));
    }
    if (base.divisions && base.divisions.length) {
      tags = tags.concat(base.divisions.slice(0, 2));
    }

    if (!tags.length) {
      return "";
    }

    return (
      "<div class=\"tag-list\" style=\"margin-top: 14px;\">" +
      tags
        .map(function (tag) {
          return "<span class=\"tag-chip\">" + escapeHtml(tag) + "</span>";
        })
        .join("") +
      "</div>"
    );
  }

  function renderDetail(titleNode, metaNode, bodyNode, base) {
    if (!base) {
      renderEmptyDetail(titleNode, metaNode, bodyNode, "No base selected.");
      return;
    }

    titleNode.textContent = base.name;
    metaNode.textContent = buildBaseMeta(base) + " | " + base.rowCount + (base.rowCount === 1 ? " workbook row" : " workbook rows");

    var sections = [];

    sections.push(renderTagSection("Command Chain", []
      .concat(base.militaryDistricts || [])
      .concat(base.armies || [])
      .concat(base.corps || [])
      .concat(base.divisions || [])
      .concat(base.brigades || [])));

    if (base.regiments && base.regiments.length) {
      sections.push(renderListSection("Regiments", base.regiments));
    }

    if (base.formationTypes && base.formationTypes.length) {
      sections.push(
        renderListSection(
          "Formation Mix",
          base.formationTypes.map(function (item) {
            return item.name + " x" + item.count;
          })
        )
      );
    }

    if (base.equipmentTotals && base.equipmentTotals.length) {
      sections.push(
        renderListSection(
          "Equipment Snapshot",
          base.equipmentTotals.map(function (item) {
            return item.name + ": " + item.count;
          })
        )
      );
    }

    if (base.formations && base.formations.length) {
      var formationItems = base.formations.slice();
      if (base.formationOverflow) {
        formationItems.push("+" + base.formationOverflow + " more workbook rows at this base");
      }
      sections.push(renderListSection("Representative Formations", formationItems));
    }

    bodyNode.innerHTML = sections.filter(Boolean).join("");
  }

  function renderTagSection(title, items) {
    var cleanItems = items.filter(Boolean);
    if (!cleanItems.length) {
      return "";
    }

    return (
      "<section class=\"detail-section\">" +
      "<h3 class=\"detail-section-title\">" +
      escapeHtml(title) +
      "</h3>" +
      "<div class=\"tag-list\">" +
      cleanItems
        .map(function (item) {
          return "<span class=\"tag-chip\">" + escapeHtml(item) + "</span>";
        })
        .join("") +
      "</div>" +
      "</section>"
    );
  }

  function renderListSection(title, items) {
    var cleanItems = items.filter(Boolean);
    if (!cleanItems.length) {
      return "";
    }

    return (
      "<section class=\"detail-section\">" +
      "<h3 class=\"detail-section-title\">" +
      escapeHtml(title) +
      "</h3>" +
      "<ul class=\"detail-list\">" +
      cleanItems
        .map(function (item) {
          return "<li>" + escapeHtml(item) + "</li>";
        })
        .join("") +
      "</ul>" +
      "</section>"
    );
  }

  function renderEmptyDetail(titleNode, metaNode, bodyNode, message) {
    titleNode.textContent = "No base selected";
    metaNode.textContent = message;
    bodyNode.innerHTML = "";
  }

  function renderLoadErrors() {
    Array.from(document.querySelectorAll(".filter-result")).forEach(function (node) {
      node.textContent = "The Soviet base data could not be loaded.";
    });

    var mapStatus = document.getElementById("base-map-status");
    if (mapStatus) {
      mapStatus.textContent = "The Soviet base data could not be loaded.";
    }

    var directory = document.getElementById("base-directory");
    if (directory) {
      directory.innerHTML = "<div class=\"empty-state\">The Soviet base data could not be loaded.</div>";
    }

    var listRoot = document.getElementById("base-list");
    if (listRoot) {
      listRoot.innerHTML = "<div class=\"empty-state\">The Soviet base data could not be loaded.</div>";
    }
  }

  function filterBases(bases, search, host, militaryDistrict) {
    return bases.filter(function (base) {
      var matchesSearch = !search || base.searchText.indexOf(search) !== -1;
      var matchesHost = !host || base.hostCountry === host;
      var matchesDistrict =
        !militaryDistrict || (base.militaryDistricts || []).indexOf(militaryDistrict) !== -1;
      return matchesSearch && matchesHost && matchesDistrict;
    });
  }

  function populateSelect(select, values, label) {
    if (!select) {
      return;
    }

    select.innerHTML =
      "<option value=\"\">" +
      escapeHtml(label) +
      "</option>" +
      values
        .map(function (value) {
          return "<option value=\"" + escapeHtml(value) + "\">" + escapeHtml(value) + "</option>";
        })
        .join("");
  }

  function buildBaseMeta(base) {
    return [base.locationName, base.hostCountry].filter(Boolean).join(", ");
  }

  function buildBaseCardSummary(base) {
    var firstDistrict = (base.militaryDistricts || [])[0] || "No district label";
    var firstDivision = (base.divisions || [])[0] || "No division label";
    return firstDistrict + " | " + firstDivision + " | " + base.rowCount + " workbook rows";
  }

  function getBaseById(bases, baseId) {
    return bases.find(function (base) {
      return base.id === baseId;
    }) || null;
  }

  function getBaseRadius(rowCount) {
    return Math.max(5, Math.min(16, Math.round(4 + Math.sqrt(rowCount))));
  }

  function buildPopupHtml(base) {
    return (
      "<strong>" +
      escapeHtml(base.name) +
      "</strong><br>" +
      escapeHtml(buildBaseMeta(base)) +
      "<br>" +
      escapeHtml(base.rowCount + (base.rowCount === 1 ? " workbook row" : " workbook rows"))
    );
  }

  function hideMapStatus(node) {
    if (node) {
      node.classList.add("is-hidden");
    }
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }
})();
