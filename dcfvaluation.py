import argparse
import csv
import os

def dcf_valuation(
    company_name,
    operating_cash_flow,
    capex,
    total_shares_outstanding,
    annual_growth_rate=0.05,
    discount_rate=0.10,
    terminal_growth_rate=0.04
):
    print(f"\n=== DCF Valuation for {company_name} ===")
    print("\n--- Step 1: Calculate Base Free Cash Flow (FCF) ---")
    base_fcf = operating_cash_flow - capex
    print(f"Operating Cash Flow: ₹{operating_cash_flow:,.2f}")
    print(f"Capital Expenditures (CapEx): ₹{capex:,.2f}")
    print(f"Base Free Cash Flow: ₹{base_fcf:,.2f}\n")

    print("--- Step 2: Project Free Cash Flows for Next 5 Years ---")
    projected_fcfs = []
    for year in range(1, 6):
        fcf = base_fcf * ((1 + annual_growth_rate) ** year)
        projected_fcfs.append(fcf)
        print(f"Year {year}: ₹{fcf:,.2f}")

    print("\n--- Step 3: Estimate Terminal Value ---")
    terminal_fcf = projected_fcfs[-1] * (1 + terminal_growth_rate)
    terminal_value = terminal_fcf / (discount_rate - terminal_growth_rate)
    print(f"Terminal FCF (Year 6): ₹{terminal_fcf:,.2f}")
    print(f"Terminal Value: ₹{terminal_value:,.2f}\n")

    print("--- Step 4: Discount FCFs and Terminal Value to Present Value ---")
    discounted_fcfs = []
    for year, fcf in enumerate(projected_fcfs, 1):
        discounted = fcf / ((1 + discount_rate) ** year)
        discounted_fcfs.append(discounted)
        print(f"Discounted FCF Year {year}: ₹{discounted:,.2f}")

    discounted_terminal_value = terminal_value / ((1 + discount_rate) ** 5)
    print(f"Discounted Terminal Value: ₹{discounted_terminal_value:,.2f}\n")

    total_pv_fcfs = sum(discounted_fcfs)
    enterprise_value = total_pv_fcfs + discounted_terminal_value
    print("--- Step 5: Calculate Equity Value ---")
    print(f"Present Value of Projected FCFs: ₹{total_pv_fcfs:,.2f}")
    print(f"Enterprise Value (EV): ₹{enterprise_value:,.2f}\n")

    intrinsic_value_per_share = enterprise_value / total_shares_outstanding
    print("--- Step 6: Determine Intrinsic Value per Share ---")
    print(f"Total Shares Outstanding: {total_shares_outstanding:,.2f}")
    print(f"Intrinsic Value per Share: ₹{intrinsic_value_per_share:,.2f}\n")

    # Append or update result in CSV file
    output_file = "dcf_valuations.csv"
    updated = False
    rows = []

    if os.path.isfile(output_file):
        with open(output_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if row[0] == company_name:
                    rows.append([company_name, round(intrinsic_value_per_share, 2)])
                    updated = True
                else:
                    rows.append(row)

    if not updated:
        rows.append([company_name, round(intrinsic_value_per_share, 2)])

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "Intrinsic Value per Share (₹)"])
        writer.writerows(rows)

    print(f"Valuation result saved to {output_file}")
    return intrinsic_value_per_share

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DCF Valuation Calculator")
    parser.add_argument("--company", type=str, required=True, help="Company Name")
    parser.add_argument("--ocf", type=float, required=True, help="Operating Cash Flow (₹ million)")
    parser.add_argument("--capex", type=float, required=True, help="Capital Expenditures (₹ million)")
    parser.add_argument("--shares", type=float, required=True, help="Total Shares Outstanding (million)")
    parser.add_argument("--growth", type=float, default=0.05, help="Annual FCF Growth Rate (default: 0.05)")
    parser.add_argument("--discount", type=float, default=0.10, help="Discount Rate (default: 0.10)")
    parser.add_argument("--terminal", type=float, default=0.04, help="Terminal Growth Rate (default: 0.04)")

    args = parser.parse_args()

    dcf_valuation(
        company_name=args.company,
        operating_cash_flow=args.ocf,
        capex=args.capex,
        total_shares_outstanding=args.shares,
        annual_growth_rate=args.growth,
        discount_rate=args.discount,
        terminal_growth_rate=args.terminal
    )