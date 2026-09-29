"""Guards added for Algo Acquisition after the 2026-09-17 Blitz incident (see sourcing/TOOLS.md)."""
import pytest

from listbuild.identity import normalize_company_linkedin_url
from listbuild.providers import blitz as B


def test_company_linkedin_url_normalisation():
    assert normalize_company_linkedin_url("https://www.linkedin.com/company/Robert-Half-International/") == "linkedin.com/company/robert-half-international"
    assert normalize_company_linkedin_url("linkedin.com/company/acme/about?x=1") == "linkedin.com/company/acme"
    assert normalize_company_linkedin_url("https://www.linkedin.com/in/jane") is None
    assert normalize_company_linkedin_url(None) is None


def test_canary_builds_one_single_filter_body_per_icp_filter(icp):
    icp = {**icp, "company_type_exclude": ["Nonprofit"]}
    checks = B.canary_checks(icp)
    names = {(ep, n) for ep, n, _ in checks}
    assert ("people", "company.industry") in names and ("people", "people.job_level") in names
    assert ("people", "company.type") in names and ("companies", "company.revenue") in names
    for _, name, body in checks:
        group, key = name.split(".")
        assert list(body[group]) == [key]   # exactly one filter per check


def test_ignored_filter_is_detected_when_count_equals_the_database():
    totals = {"people": 454_021_881, "companies": 68_363_495}
    results = [("people", "company.industry", 2_135_366), ("people", "company.bogus", 454_021_881),
               ("companies", "company.linkedin_url", 68_363_495), ("people", "company.type", 437_010_796)]
    assert B.ignored_filters(totals, results) == ["people:company.bogus", "companies:company.linkedin_url"]


class _FakeBlitz(B.BlitzClient):
    def __init__(self, ignore):
        self.ignore, self.records_used = ignore, 0

    def _total(self, body, db):
        filters = {f"{g}.{k}" for g in ("company", "people") for k in (body.get(g) or {})}
        if not filters or filters & self.ignore:
            return {"total_results": db}
        return {"total_results": db // 10}

    def search_people(self, body):
        return self._total(body, 454_021_881)

    def search_companies(self, body):
        return self._total(body, 68_363_495)


def test_canary_raises_when_any_filter_is_ignored(icp):
    _FakeBlitz(set()).canary(icp)
    with pytest.raises(B.FilterIgnored):
        _FakeBlitz({"company.revenue"}).canary(icp)


def test_company_type_exclude_reaches_both_bodies(icp):
    icp = {**icp, "company_type_exclude": ["Nonprofit", "Government Agency"]}
    assert B.build_people_body(icp, {}, 1)["company"]["type"] == {"exclude": ["Nonprofit", "Government Agency"]}
    assert B.build_company_body(icp, {}, 1)["company"]["type"] == {"exclude": ["Nonprofit", "Government Agency"]}


def test_percent_encoded_and_double_encoded_slugs_share_one_key():
    from listbuild.identity import normalize_linkedin_url as n
    plain = n("https://www.linkedin.com/in/øistein-kleven-578534179")
    assert n("https://www.linkedin.com/in/%c3%b8istein-kleven-578534179/") == plain
    assert n("https://www.linkedin.com/in/%25c3%25b8istein-kleven-578534179") == plain
    assert n("https://www.linkedin.com/in/%2525C3%2525B8istein-kleven-578534179") == plain


def test_clay_person_location_uses_its_own_country_spelling():
    from listbuild.icp_gen import build_icp
    from listbuild.providers.clay import build_people_query
    icp = build_icp("t", ["Staffing and Recruiting"], ["CZ", "MK", "GB"], 1_000_000)
    q = build_people_query(icp, {})
    assert 'location_country in ("Czech Republic", "North Macedonia", "United Kingdom")' in q
    assert 'country_name in ("Czechia", "Macedonia", "United Kingdom")' in q


def test_algo_shorthand_expands_to_the_full_geo_list():
    from listbuild.icp_gen import ALGO_GEOS, build_icp
    icp = build_icp("t", ["Staffing and Recruiting"], ["ALGO"], 1_000_000)
    assert icp["company_hq_countries"] == ALGO_GEOS and icp["person_countries"] == ALGO_GEOS
