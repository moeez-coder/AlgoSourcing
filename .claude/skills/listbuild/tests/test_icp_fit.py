from listbuild.icp_fit import classify_company_fit
from listbuild.ledger import Ledger


def test_core_industry_is_fit(icp):
    assert classify_company_fit(icp, "Advertising Services", None) == ("fit", "core industry")
    assert classify_company_fit(icp, "ADVERTISING_AND_MARKETING,SAAS", None) == ("fit", "core industry")


def test_gated_industry_needs_keyword_flag(icp):
    assert classify_company_fit(icp, "Business Consulting and Services", True) == ("candidate", "consulting with marketing keywords")
    assert classify_company_fit(icp, "Business Consulting and Services", False) == ("unfit", "consulting without marketing keywords")
    assert classify_company_fit(icp, "Strategic Management Services", None) == ("unknown", "consulting, keywords not checked")


def test_unknown_or_foreign_industry(icp):
    assert classify_company_fit(icp, None, None) == ("unknown", "industry unknown")
    assert classify_company_fit(icp, "Oil and Gas", None) == ("unfit", "industry outside ICP")


def _row(**kw):
    base = dict(linkedin_url="https://linkedin.com/in/x", first_name="A", last_name="B", full_name="A B", job_title="Director",
                seniority="Director", company_name="X", company_domain="x.com", company_linkedin_url="https://www.linkedin.com/company/x",
                industry=None, revenue_hint=None, person_country="US", company_country="US", source="blitz", cost_usd=0.0)
    base.update(kw)
    return base


def test_apply_fit_uses_company_table_then_contact_industry(tmp_path, icp):
    lg = Ledger(tmp_path / "l.sqlite")
    lg.upsert_contact(_row(linkedin_url="https://linkedin.com/in/a", company_domain="agency.com"))
    lg.upsert_contact(_row(linkedin_url="https://linkedin.com/in/b", company_domain="energy.com"))
    lg.upsert_contact(_row(linkedin_url="https://linkedin.com/in/c", company_domain="brandco.com"))
    lg.upsert_contact(_row(linkedin_url="https://linkedin.com/in/d", company_domain=None, company_linkedin_url=None, industry="Marketing Services", source="clay"))
    lg.upsert_contact(_row(linkedin_url="https://linkedin.com/in/e", company_domain=None, company_linkedin_url=None, industry="Business Consulting and Services", source="clay"))
    lg.upsert_company({"domain": "agency.com", "name": "Agency", "industry": "Advertising Services", "source": "blitz"})
    lg.upsert_company({"domain": "energy.com", "name": "Energy", "industry": "Business Consulting and Services", "source": "blitz"})
    lg.upsert_company({"domain": "brandco.com", "name": "BrandCo", "industry": "Business Consulting and Services", "source": "blitz"})
    lg.set_keyword_fit(["brandco.com"], checked_domains=["brandco.com", "energy.com"])
    counts = lg.apply_fit(icp)
    assert counts == {"fit": 1, "candidate": 1, "unfit": 1, "unknown": 2}
    assert lg.get_contact("li:linkedin.com/in/b")["icp_fit"] == "unfit"
    assert lg.get_contact("li:linkedin.com/in/c")["icp_fit"] == "candidate"
    # Clay/Blitz row industries are the search filter, so with no verified company they stay 'unknown'
    assert lg.get_contact("li:linkedin.com/in/d")["icp_fit"] == "unknown"
    assert lg.get_contact("li:linkedin.com/in/e")["icp_fit"] == "unknown"
    # the authoritative company-table industry is written back onto the contact
    assert lg.get_contact("li:linkedin.com/in/a")["industry"] == "Advertising Services"


def test_filter_inferred_industry_never_marks_an_unverified_company_fit(tmp_path, icp):
    """A provider that ignores a filter returns people at companies outside the ICP, tagged with the filter's industry."""
    lg = Ledger(tmp_path / "l.sqlite")
    lg.upsert_contact(_row(linkedin_url="https://linkedin.com/in/f", company_domain="outside.com", industry="Marketing Services", source="blitz"))
    lg.upsert_contact(_row(linkedin_url="https://linkedin.com/in/g", company_domain="inside.com", industry="Marketing Services", source="blitz"))
    lg.upsert_company({"domain": "inside.com", "name": "Inside", "industry": "Marketing Services", "source": "blitz_companies"})
    lg.apply_fit(icp)
    assert lg.get_contact("li:linkedin.com/in/f")["icp_fit"] == "unknown"   # company never verified by company search
    assert lg.get_contact("li:linkedin.com/in/g")["icp_fit"] == "fit"
    ind = lg.conn.execute("SELECT industry FROM companies WHERE domain = 'outside.com'").fetchone()[0]
    assert ind is None   # the filter label was not written onto the company


def test_record_level_industry_fallback_still_applies(tmp_path, icp):
    lg = Ledger(tmp_path / "l.sqlite")
    lg.upsert_contact(_row(linkedin_url="https://linkedin.com/in/h", company_domain=None, company_linkedin_url=None,
                           industry="ADVERTISING_AND_MARKETING", source="discolike"))
    lg.apply_fit(icp)
    assert lg.get_contact("li:linkedin.com/in/h")["icp_fit"] == "fit"
