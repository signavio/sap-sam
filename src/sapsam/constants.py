from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).parents[2].resolve()
DATA_ROOT = PROJECT_ROOT / "data"
DATA_RAW = DATA_ROOT / "raw"
DATA_DATASET = DATA_RAW / "sap_sam_2022" / "models" / "SAPSAM"
DATA_INTERIM = DATA_ROOT / "interim"
SRC_ROOT = PROJECT_ROOT / "src" / "sapsam"
FIGURES_ROOT = PROJECT_ROOT / "reports" / "figures"

BPMN2_NAMESPACE = "http://b3mn.org/stencilset/bpmn2.0#"

EMAIL_DUMMY = "jane.doe@dummy.com"
NAME_DUMMY = "Jane Doe"
NUMBER_DUMMY = "12345678"

COLORS_SIGNAVIO_HSL = [
    "hsl(309, 88%, 33%)", "hsl(313, 81%, 35%)", "hsl(318, 75%, 36%)", "hsl(322, 70%, 39%)", "hsl(326, 65%, 40%)",
    "hsl(331, 60%, 43%)", "hsl(336, 56%, 45%)", "hsl(341, 53%, 46%)", "hsl(352, 47%, 50%)", "hsl(358, 48%, 53%)",
    "hsl(4, 51%, 53%)", "hsl(9, 54%, 53%)", "hsl(14, 57%, 52%)", "hsl(18, 60%, 52%)", "hsl(21, 64%, 52%)",
    "hsl(25, 67%, 51%)", "hsl(27, 70%, 51%)", "hsl(30, 73%, 51%)", "hsl(32, 76%, 50%)", "hsl(34, 79%, 50%)",
    "hsl(36, 83%, 50%)", "hsl(38, 87%, 49%)", "hsl(40, 91%, 49%)", "hsl(41, 96%, 48%)", "hsl(43, 100%, 48%)"
]

COLORS_SIGNAVIO_ = [
    "#9c0a85", "#a01180", "#a3177a", "#a71e75", "#aa2470", "#ae2b6a", "#b23265", "#b53860", "#b93f5a", "#bc4555",
    "#c04c50", "#c4534a", "#c75945", "#cb6040", "#ce663b", "#d26d35", "#d67430", "#d97a2b", "#dd8125", "#e08720",
    "#e48e1b", "#e89515", "#eb9b10", "#efa20b", "#f2a805", "#f6af00"
]
