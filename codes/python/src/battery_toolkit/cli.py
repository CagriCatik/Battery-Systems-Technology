import argparse
import sys
from battery_toolkit.core.cell import BatteryCell, CellChemistry
from battery_toolkit.core.units import kw_to_hp, hp_to_kw, celsius_to_kelvin, kelvin_to_celsius
from battery_toolkit.sizing.vehicle import VehicleParameters
from battery_toolkit.sizing.optimizer import PackSizingOptimizer, SizingRequirements
from battery_toolkit.sizing.pack_geometry import PackGeometryCalculator
from battery_toolkit.thermal.cooling_benchmark import CoolingTechnologyBenchmark


def handle_size(args):
    print("=== Battery Sizing Optimizer ===")
    cell = BatteryCell(
        name="Automotive Cell",
        chemistry=CellChemistry.NMC,
        nominal_voltage=args.cell_voltage,
        capacity_ah=args.cell_capacity,
    )
    vehicle = VehicleParameters()
    optimizer = PackSizingOptimizer(cell, vehicle)
    pack = optimizer.size_pack(
        desired_energy_kwh=args.energy,
        system_voltage=args.voltage,
        buffer_percentage=args.buffer,
    )
    summary = pack.summary()
    print(f"Topology:          {summary['topology']}")
    print(f"Total Cells:       {summary['total_cells']}")
    print(f"Nominal Voltage:   {summary['nominal_voltage_v']} V")
    print(f"Total Capacity:    {summary['capacity_ah']} Ah")
    print(f"Nominal Energy:    {summary['nominal_energy_kwh']} kWh")
    print(f"Total Pack Mass:   {summary['total_pack_mass_kg']} kg")

    if args.csv:
        PackGeometryCalculator.export_sizing_to_csv(pack, args.csv)
        print(f"Results exported to {args.csv}")


def handle_convert(args):
    if args.kw is not None:
        hp = kw_to_hp(args.kw)
        print(f"{args.kw:.2f} kW = {hp:.2f} HP")
    elif args.hp is not None:
        kw = hp_to_kw(args.hp)
        print(f"{args.hp:.2f} HP = {kw:.2f} kW")
    elif args.celsius is not None:
        k = celsius_to_kelvin(args.celsius)
        print(f"{args.celsius:.2f} °C = {k:.2f} K")
    elif args.kelvin is not None:
        c = kelvin_to_celsius(args.kelvin)
        print(f"{args.kelvin:.2f} K = {c:.2f} °C")
    else:
        print("Please provide a value to convert (e.g. --kw, --hp, --celsius, --kelvin).")


def handle_benchmark(args):
    print("=== BTMS Cooling Benchmark ===")
    bench = CoolingTechnologyBenchmark()
    df = bench.run_full_benchmark()
    print(df.to_string(index=False))


def main():
    parser = argparse.ArgumentParser(
        prog="battery-toolkit",
        description="Battery Systems Technology CLI Toolkit",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Sizing Subcommand
    size_p = subparsers.add_parser("size", help="Size a battery pack to voltage and energy specs")
    size_p.add_argument("--voltage", type=float, default=400.0, help="Target system voltage (V)")
    size_p.add_argument("--energy", type=float, default=65.0, help="Desired pack energy (kWh)")
    size_p.add_argument("--buffer", type=float, default=15.0, help="Safety buffer percentage")
    size_p.add_argument("--cell-voltage", type=float, default=3.65, help="Nominal cell voltage (V)")
    size_p.add_argument("--cell-capacity", type=float, default=5.0, help="Cell capacity (Ah)")
    size_p.add_argument("--csv", type=str, default=None, help="Optional output CSV path")

    # Convert Subcommand
    conv_p = subparsers.add_parser("convert", help="Convert engineering units")
    conv_p.add_argument("--kw", type=float, help="Kilowatts to HP")
    conv_p.add_argument("--hp", type=float, help="Horsepower to kW")
    conv_p.add_argument("--celsius", type=float, help="Celsius to Kelvin")
    conv_p.add_argument("--kelvin", type=float, help="Kelvin to Celsius")

    # Benchmark Subcommand
    subparsers.add_parser("benchmark", help="Run BTMS cooling technology benchmark")

    args = parser.parse_args()
    if args.command == "size":
        handle_size(args)
    elif args.command == "convert":
        handle_convert(args)
    elif args.command == "benchmark":
        handle_benchmark(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
