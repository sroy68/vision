from datetime import datetime

def generate_report(target, issues, outfile="vision_report.txt"):
    with open(outfile, "w") as f:
        f.write("VISION BUG BOUNTY REPORT\n")
        f.write("="*30 + "\n")
        f.write(f"Target: {target}\n")
        f.write(f"Date  : {datetime.now()}\n\n")

        if not issues:
            f.write("No security issue found.\n")
        else:
            for i, r in enumerate(issues, 1):
                f.write(f"[{i}] Problem : {r[0]}\n")
                f.write(f"    Where  : {r[1]}\n")
                f.write(f"    Impact : {r[2]}\n")
                f.write(f"    Fix    : {r[3]}\n\n")

        f.write("Note: Analysis-only, no exploitation performed.\n")

    print(f"[VISION] Report generated → {outfile}")
