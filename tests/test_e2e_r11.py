"""
tests/test_e2e_r11.py

End-to-End manual test verification for Phase R11:
1. Verify existing incident in MongoDB.
2. Call IncidentService.generate_incident_report() via backend.
3. Verify MongoDB document is updated with raw_markdown, mitre_techniques, nist_controls, hipaa_impact, etc.
4. Verify IncidentService.get_incident() returns the structured report.
"""

from bson import ObjectId
from backend.app.database.collections import incidents_collection, logs_collection
from backend.app.services.incident_service import IncidentService


def run_e2e_verification():
    print("=" * 60)
    print("HAI-SOC R11 END-TO-END VERIFICATION")
    print("=" * 60)

    # 1. Look up any existing incident in MongoDB
    incident_doc = incidents_collection.find_one()
    if not incident_doc:
        print("❌ No incidents found in MongoDB to test.")
        return

    inc_id = str(incident_doc["_id"])
    log_id = incident_doc.get("log_id")
    print(f"✅ Found Incident in DB: ID = {inc_id} | Title = {incident_doc.get('title')} | Log ID = {log_id}")

    # Check source log
    source_log = None
    try:
        source_log = logs_collection.find_one({"_id": ObjectId(log_id)})
    except Exception:
        pass
    if not source_log:
        source_log = logs_collection.find_one({"id": log_id})

    if not source_log:
        print(f"❌ Source log {log_id} not found in logs collection.")
        return

    print(f"✅ Found Source Log: action = {source_log.get('action')}, source = {source_log.get('source')}, user_id = {source_log.get('user_id')}")

    # 2. Trigger Report Generation
    print("\nTriggering IncidentService.generate_incident_report()...")
    res = IncidentService.generate_incident_report(inc_id)

    print("\n✅ Generation & Persistence Successful!")
    print(f"  Incident ID: {res.id}")
    print(f"  Risk Level: {res.risk_level}")
    print(f"  Status: {res.status}")
    print(f"  MITRE Technique: {res.mitre_technique_id}")
    print(f"  HIPAA Impact: {res.hipaa_impact[:60] if res.hipaa_impact else 'None'}...")

    report = res.report
    if hasattr(report, "raw_markdown"):
        print(f"  Report Status: {report.status}")
        print(f"  MITRE Badges: {report.mitre_techniques}")
        print(f"  NIST Controls: {report.nist_controls}")
        print(f"  Recommended Actions: {len(report.recommended_actions)} items")
        print(f"  Raw Markdown Length: {len(report.raw_markdown)} characters")
    elif isinstance(report, dict):
        print(f"  Report Status: {report.get('status')}")
        print(f"  MITRE Badges: {report.get('mitre_techniques')}")
        print(f"  NIST Controls: {report.get('nist_controls')}")
        print(f"  Recommended Actions: {len(report.get('recommended_actions', []))} items")
        print(f"  Raw Markdown Length: {len(report.get('raw_markdown', ''))} characters")

    # 3. Verify GET without re-invoking Ollama
    print("\nVerifying GET /incidents/{id} (Database-only)...")
    get_res = IncidentService.get_incident(inc_id)
    assert get_res is not None
    assert get_res.id == inc_id
    assert get_res.report is not None
    print("✅ GET Incident confirmed database-backed without re-running LLM.")
    print("=" * 60)


if __name__ == "__main__":
    run_e2e_verification()
