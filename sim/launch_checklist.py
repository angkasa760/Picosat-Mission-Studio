import os

def run_launch_checklist():
    # --- Check Values ---
    checks = {
        "S11 Magnitude": (-20.5, -15.0), # (actual, limit) - lower is better
        "VSWR": (1.2, 2.0),              # lower is better
        "Link Margin": (30.76, 10.0),    # higher is better
        "Battery SoC": (87.24, 60.0),    # higher is better
        "Thermal Shift": (0.483, 1.0),   # MHz - lower is better
        "Structural MoS": (2.12, 0.0)    # higher is better
    }
    
    print("="*40)
    print(" FINAL MISSION READINESS CHECKLIST (GO/NO-GO) ")
    print("="*40)
    
    all_pass = True
    for name, (val, limit) in checks.items():
        is_pass = False
        if name in ["S11 Magnitude", "VSWR", "Thermal Shift"]:
            is_pass = val <= limit
        else:
            is_pass = val >= limit
            
        status = " [ PASS ] " if is_pass else " [ FAIL ] "
        if not is_pass: all_pass = False
        
        print(f"{name:<20}: {val:>8} (Limit: {limit:>8}) {status}")

    print("="*40)
    if all_pass:
        print(" MISSION STATUS: GO FOR LAUNCH (LAUNCH READY) ")
        print(" ALL SYSTEMS NOMINAL - PIN-UHF READY FOR DEPLOYMENT ")
    else:
        print(" MISSION STATUS: NO-GO (CONDITION CRITICAL) ")
        print(" PLEASE REVIEW FAILURES BEFORE PROCEEDING ")
    print("="*40)

if __name__ == "__main__":
    run_launch_checklist()
