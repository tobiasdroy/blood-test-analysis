import hashlib
import json
import logging
from datetime import datetime, timezone

import requests
import streamlit as st
from simple_salesforce import Salesforce, SalesforceExpiredSession

logger = logging.getLogger(__name__)

# ── Change this if your object has a different API name ──────────────────────
_SF_OBJECT = "App_Submission__c"


@st.cache_resource(ttl=3000)  # Re-authenticate every 50 min (tokens last ~60 min)
def _get_sf_client() -> Salesforce:
    resp = requests.post(
        f"{st.secrets['sf_instance_url']}/services/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": st.secrets["sf_consumer_key"],
            "client_secret": st.secrets["sf_consumer_secret"],
        },
        timeout=10,
    )
    resp.raise_for_status()
    token = resp.json()
    return Salesforce(instance_url=token["instance_url"], session_id=token["access_token"])


def _make_external_id(results: dict, sex: str) -> str:
    """SHA-256 hash of results + sex + UTC date. Same submission same day → same ID."""
    payload = {
        "results": {k: v.get("value") for k, v in sorted(results.items())},
        "sex": sex,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:40]


def _do_upsert(sf: Salesforce, ext_id: str, record: dict) -> None:
    getattr(sf, _SF_OBJECT).upsert(f"External_ID__c/{ext_id}", record)


def submit_results(results: dict, sex: str) -> bool:
    """
    Upsert a blood test submission to Salesforce.
    Returns True on success, False if the call fails (app continues either way).
    Skips silently if the same results were already submitted this session.
    """
    ext_id = _make_external_id(results, sex)

    # In-session deduplication: don't re-submit identical results twice in one session
    if st.session_state.get("sf_submitted_hash") == ext_id:
        return True

    record = {
        "Submission_Time__c": datetime.now(timezone.utc).isoformat(),
        "Sex__c": sex,
        "Consent_Improve__c": st.session_state.get("consent_improve", True),
        "Consent_Research__c": st.session_state.get("consent_research", False),
        "Consent_Insights__c": st.session_state.get("consent_insights", False),
        "Results_JSON__c": json.dumps(
            {k: v.get("value") for k, v in results.items()},
            sort_keys=True,
        ),
    }

    try:
        sf = _get_sf_client()
        _do_upsert(sf, ext_id, record)
        st.session_state.sf_submitted_hash = ext_id
        return True
    except SalesforceExpiredSession:
        # Token expired mid-session — clear cache and retry once
        _get_sf_client.clear()
        try:
            sf = _get_sf_client()
            _do_upsert(sf, ext_id, record)
            st.session_state.sf_submitted_hash = ext_id
            return True
        except Exception as exc:
            logger.error("Salesforce retry failed: %s", exc)
            return False
    except Exception as exc:
        logger.error("Salesforce submission failed: %s", exc)
        return False
