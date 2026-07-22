"""
HAI-SOC Attack Injection Pipeline 

Input:
    datasets/processed/features.csv

Output:
    datasets/processed/ml_dataset.csv
"""

from pathlib import Path
import random
import uuid
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "processed"

INPUT_FILE = PROCESSED_DIR / "features.csv"
OUTPUT_FILE = PROCESSED_DIR / "ml_dataset.csv"

random.seed(42)

ATTACK_COUNTS = {
    "BRUTE_FORCE": 40,
    "INSIDER_THREAT": 40,
    "PORT_SCAN": 40,
    "DATA_EXFILTRATION": 40,
    "PRIVILEGE_ESCALATION": 40,
}

MITRE = {
    "BRUTE_FORCE": ("Credential Access", "T1110"),
    "INSIDER_THREAT": ("Collection", "T1005"),
    "PORT_SCAN": ("Reconnaissance", "T1046"),
    "DATA_EXFILTRATION": ("Exfiltration", "T1048"),
    "PRIVILEGE_ESCALATION": ("Privilege Escalation", "T1078"),
}

used_indices = set()


def available_indices(df):
    return list(set(df.index) - used_indices)


def select_indices(df_subset, count):
    candidates = [i for i in df_subset.index if i not in used_indices]
    count = min(count, len(candidates))
    chosen = random.sample(candidates, count)
    used_indices.update(chosen)
    return chosen


def mark_attack(df, idx, attack):
    tactic, technique = MITRE[attack]
    df.loc[idx, "label"] = 1
    df.loc[idx, "attack_type"] = attack
    df.loc[idx, "attack_id"] = "ATT-" + uuid.uuid4().hex[:8].upper()
    df.loc[idx, "mitre_tactic"] = tactic
    df.loc[idx, "mitre_technique"] = technique


def inject_bruteforce(df):
    vpn = df[df["source"] == "VPN"]
    for idx in select_indices(vpn, ATTACK_COUNTS["BRUTE_FORCE"]):
        df.loc[idx, "event_type"] = "VPN_LOGIN"
        df.loc[idx, "status"] = "FAILED"
        df.loc[idx, "status_score"] = 1
        df.loc[idx, "severity"] = "HIGH"
        df.loc[idx, "severity_score"] = 3
        mark_attack(df, idx, "BRUTE_FORCE")


def inject_insider(df):
    ehr = df[df["source"] == "EHR"]
    for idx in select_indices(ehr, ATTACK_COUNTS["INSIDER_THREAT"]):
        df.loc[idx, "event_type"] = "VIEW_RECORD"
        df.loc[idx, "severity"] = "HIGH"
        df.loc[idx, "severity_score"] = 3
        df.loc[idx, "is_business_hours"] = 0
        mark_attack(df, idx, "INSIDER_THREAT")


def inject_portscan(df):
    fw = df[df["source"] == "FIREWALL"]
    for idx in select_indices(fw, ATTACK_COUNTS["PORT_SCAN"]):
        df.loc[idx, "event_type"] = "BLOCKED_PORT_SCAN"
        df.loc[idx, "status"] = "BLOCKED"
        df.loc[idx, "status_score"] = 1
        df.loc[idx, "severity"] = "CRITICAL"
        df.loc[idx, "severity_score"] = 4
        mark_attack(df, idx, "PORT_SCAN")


def inject_exfiltration(df):
    fw = df[df["source"] == "FIREWALL"]
    for idx in select_indices(fw, ATTACK_COUNTS["DATA_EXFILTRATION"]):
        if "bytes_sent" in df.columns:
            df.loc[idx, "bytes_sent"] = random.randint(5_000_000, 20_000_000)
        if "destination_port" in df.columns:
            df.loc[idx, "destination_port"] = 443
        df.loc[idx, "severity"] = "CRITICAL"
        df.loc[idx, "severity_score"] = 4
        mark_attack(df, idx, "DATA_EXFILTRATION")


def inject_privilege_escalation(df):
    ehr = df[df["source"] == "EHR"]
    for idx in select_indices(ehr, ATTACK_COUNTS["PRIVILEGE_ESCALATION"]):
        df.loc[idx, "role"] = "ADMIN"
        df.loc[idx, "severity"] = "CRITICAL"
        df.loc[idx, "severity_score"] = 4
        mark_attack(df, idx, "PRIVILEGE_ESCALATION")


def main():
    print("=" * 60)
    print("Healthcare Attack Injector V1.1")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    df["label"] = 0
    df["attack_type"] = "NORMAL"
    df["attack_id"] = ""
    df["mitre_tactic"] = ""
    df["mitre_technique"] = ""

    inject_bruteforce(df)
    inject_insider(df)
    inject_portscan(df)
    inject_exfiltration(df)
    inject_privilege_escalation(df)

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nDataset Size : {len(df)}")
    print("\nAttack Summary")
    print(df["attack_type"].value_counts())
    print(f"\nSaved to\n{OUTPUT_FILE}")
    print("\nAttack injection completed successfully.")


if __name__ == "__main__":
    main()
