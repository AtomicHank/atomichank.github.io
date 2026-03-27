(function () {
  var KMZ_PATH = "./Cold War 1985.kmz";
  var mapStatus = document.getElementById("map-status");
  var loadStatus = document.getElementById("load-status");
  var searchInput = document.getElementById("unit-search");
  var resultCount = document.getElementById("result-count");
  var unitList = document.getElementById("unit-list");
  var detailTitle = document.getElementById("detail-title");
  var detailPath = document.getElementById("detail-path");
  var detailCoords = document.getElementById("detail-coords");
  var detailDescription = document.getElementById("detail-description");
  var statTotal = document.getElementById("stat-total");
  var statNato = document.getElementById("stat-nato");
  var statWarsaw = document.getElementById("stat-warsaw");
  var filterButtons = Array.from(document.querySelectorAll("[data-filter]"));

  var state = {
    map: null,
    layerGroup: null,
    allUnits: [],
    filteredUnits: [],
    selectedId: null,
    allianceFilter: "All",
    searchTerm: "",
    iconCache: new Map()
  };

  init();

  function init() {
    createMap();
    wireControls();
    loadKmzData()
      .then(function (units) {
        state.allUnits = units.sort(compareUnits);
        updateStats();
        applyFilters({ fitBounds: true });
        setStatus("KMZ loaded.", false);
        hideMapStatus();
      })
      .catch(function (error) {
        console.error("Cold War KMZ load failed:", error);
        setStatus("Unable to load the KMZ on this page.", true);
        showMapStatus("KMZ load failed. Make sure the page is being served over HTTP rather than opened as a raw file.", true);
        renderEmptyList("No map data could be loaded.");
        renderEmptyDetail("The KMZ could not be parsed in this browser context.");
      });
  }

  function createMap() {
    state.map = L.map("map", { zoomControl: true }).setView([51.0, 12.0], 5);

    L.tileLayer(
      "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
      {
        attribution: "Tiles (c) Esri"
      }
    ).addTo(state.map);

    state.layerGroup = L.layerGroup().addTo(state.map);

    state.map.on("zoomend", function () {
      state.filteredUnits.forEach(function (unit) {
        if (unit.marker) {
          unit.marker.setIcon(getLeafletIcon(unit));
        }
      });
    });
  }

  function wireControls() {
    searchInput.addEventListener("input", function (event) {
      state.searchTerm = event.target.value.trim().toLowerCase();
      applyFilters({ fitBounds: false });
    });

    filterButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        var nextFilter = button.getAttribute("data-filter") || "All";
        state.allianceFilter = nextFilter;

        filterButtons.forEach(function (item) {
          item.classList.toggle("is-active", item === button);
        });

        applyFilters({ fitBounds: true });
      });
    });
  }

  async function loadKmzData() {
    showMapStatus("Fetching KMZ package...", false);
    setStatus("Fetching KMZ package...", false);

    var response = await fetch(KMZ_PATH);
    if (!response.ok) {
      throw new Error("HTTP " + response.status + " loading KMZ");
    }

    var zip = await JSZip.loadAsync(await response.arrayBuffer());
    var kmlFile = zip.file("doc.kml");
    if (!kmlFile) {
      throw new Error("doc.kml was not found inside the KMZ");
    }

    showMapStatus("Extracting marker art...", false);
    var assetUrls = await extractAssetUrls(zip);

    showMapStatus("Parsing KML placemarks...", false);
    var xmlText = await kmlFile.async("string");
    var parser = new DOMParser();
    var xml = parser.parseFromString(xmlText, "application/xml");
    var parseError = xml.querySelector("parsererror");
    if (parseError) {
      throw new Error("The KML document could not be parsed");
    }

    var styleIndex = buildStyleIndex(xml, assetUrls);
    var documentNode = Array.from(xml.documentElement.children).find(function (child) {
      return child.localName === "Document";
    });

    if (!documentNode) {
      throw new Error("The KML document node could not be found");
    }

    var units = [];
    walkKmlContainers(documentNode, [], styleIndex, units);
    if (!units.length) {
      throw new Error("No placemarks were found in the KMZ");
    }

    return units;
  }

  async function extractAssetUrls(zip) {
    var assetUrls = new Map();
    var work = Object.keys(zip.files)
      .filter(function (name) {
        return name.indexOf("files/") === 0 && !zip.files[name].dir;
      })
      .map(async function (name) {
        var blob = await zip.files[name].async("blob");
        assetUrls.set(name, URL.createObjectURL(blob));
      });

    await Promise.all(work);
    return assetUrls;
  }

  function buildStyleIndex(xml, assetUrls) {
    var styles = new Map();
    var styleMaps = new Map();

    Array.from(xml.getElementsByTagNameNS("*", "Style")).forEach(function (styleNode) {
      var id = styleNode.getAttribute("id");
      if (!id) {
        return;
      }

      var href = getNestedChildText(styleNode, ["IconStyle", "Icon", "href"]);
      var scale = parseFloat(getNestedChildText(styleNode, ["IconStyle", "scale"])) || 1;

      styles.set(id, {
        iconHref: resolveIconHref(href, assetUrls),
        scale: scale
      });
    });

    Array.from(xml.getElementsByTagNameNS("*", "StyleMap")).forEach(function (styleMapNode) {
      var id = styleMapNode.getAttribute("id");
      if (!id) {
        return;
      }

      Array.from(styleMapNode.children).forEach(function (pairNode) {
        if (pairNode.localName !== "Pair") {
          return;
        }

        var key = getDirectChildText(pairNode, "key");
        var styleUrl = getDirectChildText(pairNode, "styleUrl");
        if (key === "normal" && styleUrl) {
          styleMaps.set(id, styleUrl.replace(/^#/, ""));
        }
      });
    });

    return {
      styles: styles,
      styleMaps: styleMaps
    };
  }

  function walkKmlContainers(node, path, styleIndex, units) {
    Array.from(node.children).forEach(function (child) {
      if (child.localName === "Folder") {
        var folderName = getDirectChildText(child, "name");
        var nextPath = folderName ? path.concat(folderName) : path.slice();
        walkKmlContainers(child, nextPath, styleIndex, units);
        return;
      }

      if (child.localName === "Placemark") {
        var unit = parsePlacemark(child, path, styleIndex, units.length);
        if (unit) {
          units.push(unit);
        }
      }
    });
  }

  function parsePlacemark(node, rawPath, styleIndex, index) {
    var pointNode = getDirectChild(node, "Point");
    var coordsText = pointNode ? getDirectChildText(pointNode, "coordinates") : "";
    if (!coordsText) {
      return null;
    }

    var coords = coordsText.split(",");
    if (coords.length < 2) {
      return null;
    }

    var lon = parseFloat(coords[0]);
    var lat = parseFloat(coords[1]);
    if (!isFinite(lat) || !isFinite(lon)) {
      return null;
    }

    var path = rawPath.filter(function (item) {
      return item && item !== "Cold War 1985" && item !== "Cold War 1985.kmz";
    });
    var descriptionLines = normalizeDescription(getDirectChildText(node, "description"));
    var style = resolvePlacemarkStyle(getDirectChildText(node, "styleUrl"), styleIndex);
    var name = getDirectChildText(node, "name") || "Unnamed formation";
    var alliance = path[0] || "Unknown";

    return {
      id: "unit-" + index,
      name: name,
      path: path,
      alliance: alliance,
      descriptionLines: descriptionLines,
      lat: lat,
      lon: lon,
      iconHref: style.iconHref,
      iconScale: style.scale || 1,
      marker: null,
      searchText: [name, path.join(" "), descriptionLines.join(" ")].join(" ").toLowerCase()
    };
  }

  function resolvePlacemarkStyle(styleUrl, styleIndex) {
    var rawKey = (styleUrl || "").replace(/^#/, "");
    var resolvedKey = styleIndex.styleMaps.get(rawKey) || rawKey;
    return styleIndex.styles.get(resolvedKey) || { iconHref: "", scale: 1 };
  }

  function normalizeDescription(description) {
    if (!description) {
      return [];
    }

    var source = description.trim();
    if (!source) {
      return [];
    }

    if (source.indexOf("<") !== -1 && source.indexOf(">") !== -1) {
      var scratch = document.createElement("div");
      scratch.innerHTML = source;
      source = scratch.textContent || scratch.innerText || "";
    }

    return source
      .split(/\r?\n+/)
      .map(function (line) {
        return line.trim();
      })
      .filter(Boolean);
  }

  function resolveIconHref(href, assetUrls) {
    if (!href) {
      return "";
    }

    var trimmed = href.trim();
    if (assetUrls.has(trimmed)) {
      return assetUrls.get(trimmed);
    }

    if (/^http:\/\//i.test(trimmed)) {
      return trimmed.replace(/^http:\/\//i, "https://");
    }

    return trimmed;
  }

  function compareUnits(a, b) {
    return (
      a.alliance.localeCompare(b.alliance) ||
      a.path.join(" / ").localeCompare(b.path.join(" / ")) ||
      a.name.localeCompare(b.name)
    );
  }

  function updateStats() {
    var natoCount = state.allUnits.filter(function (unit) {
      return unit.alliance === "NATO";
    }).length;
    var warsawCount = state.allUnits.filter(function (unit) {
      return unit.alliance === "Warsaw Pact";
    }).length;

    statTotal.textContent = String(state.allUnits.length);
    statNato.textContent = String(natoCount);
    statWarsaw.textContent = String(warsawCount);
  }

  function applyFilters(options) {
    var fitBounds = options && options.fitBounds;

    state.filteredUnits = state.allUnits.filter(function (unit) {
      var matchesAlliance =
        state.allianceFilter === "All" || unit.alliance === state.allianceFilter;
      var matchesSearch =
        !state.searchTerm || unit.searchText.indexOf(state.searchTerm) !== -1;
      return matchesAlliance && matchesSearch;
    });

    renderMapMarkers();
    renderList();

    resultCount.textContent =
      state.filteredUnits.length + (state.filteredUnits.length === 1 ? " result" : " results");

    if (!state.filteredUnits.length) {
      renderEmptyList("No formations match the current filters.");
      renderEmptyDetail("No formation is selected because the current filters returned no results.");
      return;
    }

    var selectionStillVisible = state.filteredUnits.some(function (unit) {
      return unit.id === state.selectedId;
    });

    if (!selectionStillVisible) {
      selectUnit(state.filteredUnits[0].id, { panToUnit: false, openPopup: false });
    } else {
      updateDetailFromSelection();
      updateListActiveState();
    }

    if (fitBounds) {
      fitMapToUnits(state.filteredUnits);
    }
  }

  function renderMapMarkers() {
    state.layerGroup.clearLayers();

    state.filteredUnits.forEach(function (unit) {
      if (!unit.marker) {
        unit.marker = buildMarker(unit);
      } else {
        unit.marker.setIcon(getLeafletIcon(unit));
      }

      state.layerGroup.addLayer(unit.marker);
    });
  }

  function buildMarker(unit) {
    var marker = L.marker([unit.lat, unit.lon], {
      icon: getLeafletIcon(unit)
    });

    marker.bindPopup(buildPopupHtml(unit), {
      maxWidth: 280
    });

    marker.on("click", function () {
      selectUnit(unit.id, { panToUnit: false, openPopup: false });
    });

    return marker;
  }

  function getLeafletIcon(unit) {
    var href = unit.iconHref;
    if (!href) {
      return L.divIcon({
        className: "fallback-marker",
        html: "<span></span>",
        iconSize: [16, 16],
        iconAnchor: [8, 8],
        popupAnchor: [0, -8]
      });
    }

    var zoom = state.map ? state.map.getZoom() : 5;
    var isPaddle = href.indexOf("/mapfiles/kml/paddle/") !== -1;
    var base = Math.max(16, Math.min(38, Math.round(8 + zoom * 3)));
    var size = Math.max(16, Math.min(54, Math.round(base * (unit.iconScale || 1))));
    var width = size;
    var height = isPaddle ? Math.round(size * 1.24) : size;
    var cacheKey = [href, width, height, isPaddle ? "paddle" : "flat"].join("|");

    if (!state.iconCache.has(cacheKey)) {
      state.iconCache.set(
        cacheKey,
        L.icon({
          iconUrl: href,
          iconSize: [width, height],
          iconAnchor: isPaddle ? [Math.round(width / 2), height - 2] : [Math.round(width / 2), Math.round(height / 2)],
          popupAnchor: isPaddle ? [0, -height + 8] : [0, -Math.round(height / 2)],
          className: "coldwar-marker-icon"
        })
      );
    }

    return state.iconCache.get(cacheKey);
  }

  function renderList() {
    if (!state.filteredUnits.length) {
      renderEmptyList("No formations match the current filters.");
      return;
    }

    unitList.innerHTML = "";
    var fragment = document.createDocumentFragment();

    state.filteredUnits.forEach(function (unit) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "unit-item";
      button.classList.toggle("is-active", unit.id === state.selectedId);
      button.setAttribute("data-unit-id", unit.id);
      button.innerHTML =
        "<span class=\"unit-name\">" +
        escapeHtml(unit.name) +
        "</span>" +
        "<span class=\"unit-path\">" +
        escapeHtml(buildPathLabel(unit)) +
        "</span>";

      button.addEventListener("click", function () {
        selectUnit(unit.id, { panToUnit: true, openPopup: true });
      });

      fragment.appendChild(button);
    });

    unitList.appendChild(fragment);
  }

  function renderEmptyList(message) {
    unitList.innerHTML = "<div class=\"empty-state\">" + escapeHtml(message) + "</div>";
  }

  function selectUnit(id, options) {
    var config = options || {};
    var unit = state.allUnits.find(function (item) {
      return item.id === id;
    });

    if (!unit) {
      return;
    }

    state.selectedId = id;
    updateListActiveState();
    renderDetail(unit);

    if (config.panToUnit) {
      var nextZoom = Math.max(state.map.getZoom(), 7);
      state.map.flyTo([unit.lat, unit.lon], nextZoom, { duration: 0.65 });
    }

    if (config.openPopup && unit.marker) {
      unit.marker.openPopup();
    }
  }

  function updateListActiveState() {
    Array.from(unitList.querySelectorAll("[data-unit-id]")).forEach(function (button) {
      button.classList.toggle("is-active", button.getAttribute("data-unit-id") === state.selectedId);
    });
  }

  function updateDetailFromSelection() {
    var unit = state.filteredUnits.find(function (item) {
      return item.id === state.selectedId;
    });

    if (unit) {
      renderDetail(unit);
    }
  }

  function renderDetail(unit) {
    detailTitle.textContent = unit.name;
    detailPath.textContent = buildPathLabel(unit);
    detailCoords.textContent = "Coordinates: " + formatCoordinate(unit.lat, "N", "S") + ", " + formatCoordinate(unit.lon, "E", "W");

    if (!unit.descriptionLines.length) {
      detailDescription.innerHTML =
        "<p>No additional note was attached to this placemark inside the KMZ.</p>";
      return;
    }

    var listItems = unit.descriptionLines
      .map(function (line) {
        return "<li>" + escapeHtml(line) + "</li>";
      })
      .join("");

    detailDescription.innerHTML = "<ul class=\"detail-list\">" + listItems + "</ul>";
  }

  function renderEmptyDetail(message) {
    detailTitle.textContent = "No formation selected";
    detailPath.textContent = message;
    detailCoords.textContent = "";
    detailDescription.innerHTML = "";
  }

  function fitMapToUnits(units) {
    if (!units.length) {
      return;
    }

    var bounds = L.latLngBounds(
      units.map(function (unit) {
        return [unit.lat, unit.lon];
      })
    );

    state.map.fitBounds(bounds.pad(0.12), { maxZoom: 7 });
  }

  function buildPopupHtml(unit) {
    var description = unit.descriptionLines.length
      ? "<br><span>" + escapeHtml(unit.descriptionLines.slice(0, 3).join(" | ")) + "</span>"
      : "";

    return (
      "<strong>" +
      escapeHtml(unit.name) +
      "</strong><br>" +
      escapeHtml(buildPathLabel(unit)) +
      description
    );
  }

  function buildPathLabel(unit) {
    return unit.path.length ? unit.path.join(" / ") : unit.alliance;
  }

  function setStatus(message, isError) {
    loadStatus.textContent = message;
    loadStatus.classList.toggle("is-error", Boolean(isError));
  }

  function showMapStatus(message, isError) {
    mapStatus.textContent = message;
    mapStatus.classList.remove("is-hidden");
    mapStatus.classList.toggle("is-error", Boolean(isError));
  }

  function hideMapStatus() {
    mapStatus.classList.add("is-hidden");
  }

  function getDirectChild(node, localName) {
    return Array.from(node.children).find(function (child) {
      return child.localName === localName;
    }) || null;
  }

  function getDirectChildText(node, localName) {
    var child = getDirectChild(node, localName);
    return child ? child.textContent.trim() : "";
  }

  function getNestedChildText(node, path) {
    var current = node;

    for (var i = 0; i < path.length; i += 1) {
      current = getDirectChild(current, path[i]);
      if (!current) {
        return "";
      }
    }

    return current.textContent.trim();
  }

  function formatCoordinate(value, positiveLabel, negativeLabel) {
    var suffix = value >= 0 ? positiveLabel : negativeLabel;
    return Math.abs(value).toFixed(3) + " deg " + suffix;
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
