import math
from dataclasses import dataclass
from typing import Dict, Any, Optional
from pathlib import Path
import pandas as pd
from battery_toolkit.core.cell import BatteryCell
from battery_toolkit.core.pack import BatteryPack


@dataclass
class PackPhysicalDimensions:
    length_mm: float
    width_mm: float
    height_mm: float
    enclosure_volume_liters: float
    volumetric_packaging_efficiency: float # Cell volume / Enclosure volume
    packing_style: str                    # "Hexagonal" or "Orthogonal"


class PackGeometryCalculator:
    """
    Computes spatial arrangement, module packaging geometry, and volumetric efficiency
    of cylindrical or prismatic cell arrays within automotive battery enclosures.
    """
    @staticmethod
    def calculate_cylindrical_layout(
        pack: BatteryPack,
        aspect_ratio_l_to_w: float = 1.6, # Typical vehicle underfloor pack aspect ratio (e.g. 1.8m x 1.1m)
        cell_spacing_gap_mm: float = 2.0,  # Clearance for swelling and cooling ducts
        enclosure_wall_thickness_mm: float = 25.0, # Structural aluminum crash frame
        hexagonal_packing: bool = True,
    ) -> PackPhysicalDimensions:
        """
        Arranges N cells into a 2D grid satisfying target aspect ratio.
        """
        n_cells = pack.total_cells
        cell_d = pack.cell.diameter_mm
        pitch_x = cell_d + cell_spacing_gap_mm
        pitch_y = (cell_d + cell_spacing_gap_mm) * (math.sqrt(3) / 2.0 if hexagonal_packing else 1.0)

        # Estimate rows and columns
        # Length ~ n_rows * pitch_x, Width ~ n_cols * pitch_y, Length / Width ~ aspect_ratio
        n_rows = max(1, int(math.sqrt(n_cells * aspect_ratio_l_to_w)))
        n_cols = math.ceil(n_cells / n_rows)

        core_length_mm = n_rows * pitch_x
        core_width_mm = n_cols * pitch_y
        core_height_mm = pack.cell.length_mm + 15.0 # Height + busbar clearance

        # Add enclosure walls and crash structure
        total_length_mm = core_length_mm + 2.0 * enclosure_wall_thickness_mm
        total_width_mm = core_width_mm + 2.0 * enclosure_wall_thickness_mm
        total_height_mm = core_height_mm + 2.0 * enclosure_wall_thickness_mm

        enclosure_vol_l = (total_length_mm * total_width_mm * total_height_mm) / 1e6
        total_cell_vol_l = n_cells * pack.cell.volume_liters
        vol_efficiency = total_cell_vol_l / max(0.1, enclosure_vol_l)

        return PackPhysicalDimensions(
            length_mm=round(total_length_mm, 1),
            width_mm=round(total_width_mm, 1),
            height_mm=round(total_height_mm, 1),
            enclosure_volume_liters=round(enclosure_vol_l, 1),
            volumetric_packaging_efficiency=round(vol_efficiency, 3),
            packing_style="Hexagonal Close-Packing" if hexagonal_packing else "Orthogonal Grid",
        )

    @staticmethod
    def export_sizing_to_csv(pack: BatteryPack, filepath: str | Path) -> None:
        """Exports pack summary metrics to a standardized CSV file."""
        df = pd.DataFrame([pack.summary()])
        df.to_csv(filepath, index=False)

