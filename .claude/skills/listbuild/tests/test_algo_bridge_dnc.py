import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("algo_bridge", Path(__file__).resolve().parents[1] / "scripts" / "algo_bridge.py")
ab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ab)


def test_dnc_matches_on_domain_or_company_linkedin(tmp_path):
    d = tmp_path / "sourcing" / "data"
    d.mkdir(parents=True)
    (d / "dnc_clients.csv").write_text(
        "company_name,domains,company_linkedin_url,source,notes\n"
        "Brilliant Staffing,brilliantfs.com;brilliantstaffing.com,https://www.linkedin.com/company/brilliant-staffing/,x,\n"
        "No URL Co,noturl.com,,x,\n")
    doms, urls = ab.dnc_companies(tmp_path)
    assert ab.is_dnc({"company_domain": "www.BrilliantFS.com"}, doms, urls)
    assert ab.is_dnc({"company_domain": None, "company_linkedin_url": "linkedin.com/company/brilliant-staffing"}, doms, urls)
    assert ab.is_dnc({"domain": "noturl.com"}, doms, urls, domain_key="domain", url_key="linkedin_url")
    assert not ab.is_dnc({"company_domain": "brilliant.com", "company_linkedin_url": "https://linkedin.com/company/brilliant"}, doms, urls)


def test_no_dnc_file_means_nothing_excluded(tmp_path):
    assert ab.dnc_companies(tmp_path) == (set(), set())


def test_placeholder_employers_are_recognised():
    for name in ["Private Company", " private company ", "Self-employed", "Freelance", "Confidential", "Stealth Mode",
                 "Self-Employed Contractor", "Undisclosed", "Family Office"]:
        assert ab.is_placeholder_employer(name), name
    for name in ["Private Equity Partners", "Freelance Recruiters Ltd", "Hays", None, ""]:
        assert not ab.is_placeholder_employer(name), name
