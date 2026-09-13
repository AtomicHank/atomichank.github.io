> Website edition: this page includes the interactive viewer and three rendered images. The CAD exports and source scripts listed in the original package documentation below are not included on the website. Viewer colors and small-screen layout have been adapted to the site; model geometry is unchanged.

# Futuro House — furnished 3D reconstruction

**Start with `Futuro_Interactive_Viewer.html`.** Open the saved HTML file in a desktop browser. Its geometry is embedded; it does not require a server, an internet connection, or an account. WebGL 2 must be available. The CAD files are independent of the viewer.

This is a newly generated, Finnish-type architectural reconstruction. It is **not a measured replica of one particular surviving house**, an official manufacturer model, or construction documentation.

## Files and their purpose

| File | Use |
| --- | --- |
| `Futuro_Interactive_Viewer.html` | Self-contained 3D viewer: exterior, roof off, cutaway, plan and exploded roof. |
| `Futuro_Full_3D_mm.dxf` | Complete colored 3D mesh assembly for a CAD layout. Millimetres; a single insertion block with separate component layers. |
| `Futuro_Interior_View_mm.dxf` | The same complete geometry, with roof, hood and partition layers initially switched off. |
| `Futuro_Full_Assembly_mm.step` | 317 named B-rep solid components, with assembly grouping and colors. Preferred starting point for solid editing in a STEP-capable CAD application. |
| `Futuro_Full_Model.glb` | Colored display model with named assemblies and transparent glazing. Metres, glTF Y-up convention. |
| `Futuro_exterior.png`, `Futuro_interior.png`, `Futuro_plan.png` | Images rendered from this model, not photographs. |
| `Futuro_Viewer_Preview.png` | Screenshot of the working interactive viewer. |
| `model_manifest.json` | Dimensions, coordinate system and modeling limitations. |
| `component_inventory.json` | Component names and layer assignments. |
| `validation.json` | Geometry, file round-trip and browser checks. |
| `Source/` | Editable Python generation scripts and viewer template. Not needed to open the finished models. |

## Interior and exterior provided

The model contains an eight-part upper shell and eight-part lower shell, actual oval window openings with glazing and seals, a support ring and V-shaped legs, concrete pads, and a lowered entrance hatch with five curved treads.

The furnished interior includes six radial reclining-style chairs with molded side panels, arm openings and reading-light details; a central grill/table and separate conical hood; a sleeping alcove with mattress, pillows and shelf; a kitchenette with sink, tap, hob and cabinetry; and a bathroom with toilet, basin, shower fittings and raised floor. Curved partitions include oval openings and an open bathroom door.

The reclining chairs and entrance are fixed display poses, not animated mechanisms. Roof lifting is an inspection feature of the viewer, not a representation of an operable roof on the original house.

## Model coordinates and dimensions

The DXF and STEP files use **millimetres**. The origin is on the ground directly below the shell centre. **Z points up; the entrance faces −Y.** The drawings contain no building site or landscape.

| Model parameter | Value |
| --- | ---: |
| Main shell diameter | 7,800 mm |
| Main shell height, excluding supports and chimney | 3,800 mm |
| Shell bottom / top above model ground | 1,500 / 5,300 mm |
| Interior floor elevation | 2,090 mm |
| Nominal shell wall | 50 mm |
| Support ring outside diameter | 5,000 mm |
| Upper / lower windows | 16 / 4 |
| Reclining chairs | 6 |
| Named parts / CAD solids | 317 / 317 |
| Overall model height including chimney | 5,695 mm |
| Overall horizontal bounds including lowered stair/landing | approximately 7,808 × 8,980 mm |

The overall footprint is not the shell diameter: stairs and minor trim extend beyond the shell. These overall bounds describe this reconstruction, not a verified clearance envelope for every real Futuro.

## Viewer controls

Drag to orbit, scroll to zoom, and right-drag or Shift-drag to pan. The assembly checkboxes hide and show individual systems. The roof slider lifts the upper shell and its glazing together.

- **Exterior (1):** all assemblies visible.
- **Roof off (2):** upper shell hidden; partitions and fireplace hood retained.
- **Cutaway (3):** upper shell and hood hidden; lower shell clipped at 2.73 m and partitions at 3.10 m to expose the interior.
- **Plan (4):** top-down cutaway.
- **Exploded roof (5):** upper shell lifted 3 m; the slider permits adjustment.

The cutaway is a display clipping operation. It does not remove geometry from the STEP, DXF or GLB files. The viewer also offers a perspective toggle and auto-rotation. On a small window, scroll the left panel to reach the lower controls.

## CAD organization

Both DXF files contain a `FUTURO_HOUSE` block inserted once at `(0,0,0)`. The block contains 317 individually layered **MESH entities**, not native DWG `3DSOLID` entities. Component names are also recorded in `FUTURO_INFO` extended entity data.

Layers:

`F_ROOF`, `F_LOWER_SHELL`, `F_FLOOR`, `F_SUPPORTS`, `F_FOUNDATIONS`, `F_PARTITIONS`, `F_LOUNGE`, `F_BEDROOM`, `F_KITCHEN`, `F_BATHROOM`, `F_FIREPLACE`, `F_HOOD`, `F_ENTRANCE`.

The interior DXF is not a reduced or permanently cut model. Turn `F_ROOF`, `F_HOOD` and `F_PARTITIONS` back on to restore the complete view. Use a shaded visual style to see the colored surfaces. The STEP version preserves actual solid geometry and is preferable when editing individual parts or preparing a separate fabrication model.

No native DWG file is included. The supplied DXF is the CAD drawing exchange version. Retain millimetres when inserting it into another drawing; a feet- or inches-based drawing needs unit-aware insertion rather than treating a drawing unit as one millimetre.

## Research basis and accuracy

The principal technical reference is Pamela Voigt's 2022 DOCOMOMO study, particularly its Finnish shell construction, elevations and interior illustrations. It documents the 7.8 m × 3.8 m ellipsoid, sectional construction, oval windows and distinctions between Finnish and American interiors. The modeled furnishing arrangement follows the Finnish type rather than the American perimeter-bench version. The City of Espoo's restored Futuro 001 provides additional museum context.

**Documented dimensions do not make the entire reconstruction survey-exact.** Furniture dimensions, partition locations, cabinetry, sanitary fixtures, concrete pads and stair deployment were interpreted from published material and modeled approximately. The interior was not traced from a complete verified, dimensioned as-built plan. Colors are a chosen period-style palette, not a colorimetric match to a specific house.

The shell wall is approximated using nested ellipsoids. A 50 mm difference between their semiaxes is not a true constant-normal offset. Glazing, joints and supports are simplified. No hidden wiring or plumbing, full fastening specification, foundations analysis, structural verification, fire-safety review, building-code compliance, or full interference/clearance analysis has been performed.

The model is suited to visual study and space planning. It is not ready for construction, restoration fabrication, or direct full-assembly 3D printing. Printing would require selecting a scale, thickening fragile parts, resolving intentional assembly overlaps, and planning splits and supports.

### Sources

1. Pamela Voigt, **“THE FUTURO: History, Design and Construction in Finland and the USA,”** *DOCOMOMO Journal* 66 (2022). Primary technical and comparative reference:  
   https://docomomojournal.com/index.php/journal/article/download/533/436
2. City of Espoo, **Futuro House**, Exhibition Centre WeeGee. Official museum context:  
   https://www.espoo.fi/en/futuro-house
3. Anna-Maija Kuitunen, **Futuro no. 001** (2010), Theseus repository. Indexed text corroborates the six bed-chairs; the complete thesis was not available for full inspection during this build:  
   https://www.theseus.fi/bitstream/handle/10024/15865/Futuro%20no%20001.pdf
4. Charles Cleworth Archive, **Futuro House Plans**. Original American-variant plan archive, consulted for variant context, not used as a measured Finnish plan:  
   https://thefuturohouse.com/Futuro-House-Charles-Cleworth-Archive-Plan.html
5. **Futuro**, Wikipedia. User-provided starting reference:  
   https://en.wikipedia.org/wiki/Futuro

All included preview images were rendered from the newly generated model. No source photographs, scans or third-party CAD files are redistributed in this package.

## Checks completed

All 317 generated solids passed the CAD kernel's validity check. Re-importing the exported STEP recovered 317 valid solids. Both DXF files were re-read and audited with zero errors or repairs. The GLB re-imported with 317 named geometries. All 317 welded display meshes are watertight after degenerate/duplicate tessellation triangles were removed.

The HTML was rendered in Chromium using WebGL 2. All five view presets, the roof slider and the perspective control were exercised without JavaScript errors. These checks confirm file and display integrity; they are not certification of historical accuracy or engineering fitness.
