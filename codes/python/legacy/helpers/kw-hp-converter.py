import argparse

def hp_to_kw(hp):
    """
    Convert HP (horsepower) to kW (kilowatts).
    
    Parameters:
        hp (float): Power in HP.
        
    Returns:
        float: Power in kW.
    """
    return hp * 0.7355

def kw_to_hp(kw):
    """
    Convert kW (kilowatts) to HP (horsepower).
    
    Parameters:
        kw (float): Power in kW.
        
    Returns:
        float: Power in HP.
    """
    return kw / 0.7355

def main():
    parser = argparse.ArgumentParser(
        description="Convert between HP (horsepower) and kW (kilowatts)."
    )
    parser.add_argument(
        "--hp-to-kw",
        type=float,
        help="Convert a given value in HP to kW.",
    )
    parser.add_argument(
        "--kw-to-hp",
        type=float,
        help="Convert a given value in kW to HP.",
    )

    args = parser.parse_args()

    if args.hp_to_kw is not None:
        kw = hp_to_kw(args.hp_to_kw)
        print(f"{args.hp_to_kw} HP is approximately {kw:.2f} kW.")
    elif args.kw_to_hp is not None:
        hp = kw_to_hp(args.kw_to_hp)
        print(f"{args.kw_to_hp} kW is approximately {hp:.2f} HP.")
    else:
        print("Please provide a valid input. Use --help for more information.")

if __name__ == "__main__":
    main()
