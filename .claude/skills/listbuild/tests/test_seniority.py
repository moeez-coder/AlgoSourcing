import pytest
from listbuild.seniority import classify_title


@pytest.mark.parametrize("title", [
    "Director of Marketing", "Account Director", "Managing Director", "VP Sales", "SVP, Growth",
    "Vice President of Operations", "Head of Strategy", "Chief Executive Officer", "CEO & Founder",
    "CMO", "Co-Founder", "Owner", "Partner", "Managing Partner", "Principal", "President",
    "Executive Director", "Director, Account Management", "Directrice générale", "Président",
])
def test_director_plus_titles_pass(title):
    assert classify_title(title) == "pass"


@pytest.mark.parametrize("title", [
    "Marketing Manager", "Account Executive", "Senior Consultant", "Account Coordinator",
    "Assistant to the Director", "Executive Assistant to CEO", "Assistant Director of Sales",
    "Marketing Specialist", "Analyst", "Intern",
])
def test_sub_director_titles_fail(title):
    assert classify_title(title) == "fail"


def test_missing_title_is_unknown_not_dropped():
    assert classify_title(None) == "unknown"
    assert classify_title("   ") == "unknown"


@pytest.mark.parametrize("title", ["Chair", "Board Chair", "Vice Chair", "Executive Chair", "Partner & Senior Consultant",
                                   "Diretor administrativo", "Directeur général"])
def test_additional_director_plus_variants_pass(title):
    assert classify_title(title) == "pass"


@pytest.mark.parametrize("title", ["Product Owner", "Business Success Partner - Business Consultant", "Partner Manager",
                                   "Mr. Moritz", "Committee Member"])
def test_additional_sub_director_variants_fail(title):
    assert classify_title(title) == "fail"


@pytest.mark.parametrize("title", ["Member Board of Directors", "V.P. Manufacturing", "Managing Member", "Entrepreneur",
                                   "Executive Search Consultant - Partner", "Sr. Director of Planning"])
def test_board_and_abbreviated_variants_pass(title):
    assert classify_title(title) == "pass"


@pytest.mark.parametrize("title", ["Advisory Board", "Member, Strategic Advisory Board", "Executive Business Partner", "Managing Editor"])
def test_advisory_and_compound_variants_fail(title):
    assert classify_title(title) == "fail"


@pytest.mark.parametrize("title", ["Advisory Board Member", "Member of the Advisory Board", "Board Advisor", "Advisor to the Board"])
def test_advisory_board_roles_fail(title):
    assert classify_title(title) == "fail"


@pytest.mark.parametrize("title", ["Director, Advisory Services", "Partner - Deal Advisory", "Board Member"])
def test_advisory_practice_leaders_still_pass(title):
    assert classify_title(title) == "pass"


# Algo Acquisition's exclude list (sourcing/icp-overview.md): these fail even with an include word in the title.
@pytest.mark.parametrize("title", ["Associate Director", "Associate Director, Talent", "Associate Partner", "AVP Sales",
                                   "Assistant Vice President", "Business Development Representative", "BDR Team Lead",
                                   "Senior SDR", "Director, Account Executive Team", "Coordinator, Office of the CEO",
                                   "Head Analyst", "Specialist Director", "Associate Vice President",
                                   "Talent Acquisition Partner | Sr Recruiter", "Executive & Leadership Talent Partner I Global TA Lead",
                                   "Assistant to the CEO", "Executive Assistant to the Founder"])
def test_algo_exclude_list_overrides_include_words(title):
    assert classify_title(title) == "fail"


@pytest.mark.parametrize("title", ["Director of Business Development", "VP Business Development", "Head of Recruitment",
                                   "Managing Director", "Founder & CEO", "Senior Director, Sales"])
def test_algo_director_plus_titles_still_pass(title):
    assert classify_title(title) == "pass"


# Seen wrongly dropped in the 2026-09-29 Vertical 1 preview sample (DE/AT/CH/LI/NL/NO/CY recruiters).
@pytest.mark.parametrize("title", ["Geschäftsführender Gesellschafter", "Geschäftsführer", "Inhaber/Geschäftsführer",
                                   "Gründer und Personalberater für spezialisierte Fachkräfte", "Mede-eigenaar", "Oprichter",
                                   "Executive Search & Talent Aquisition Specialist | Founder",
                                   "Founder & Specialist Recruiter, FinTech", "Socio Director", "Fundadora y CEO",
                                   "Amministratore Delegato", "Titolare", "Vorstandsvorsitzender", "President & Associate Recruiter"])
def test_top_tier_and_non_english_senior_titles_pass(title):
    assert classify_title(title) == "pass"


@pytest.mark.parametrize("title", ["Associate Vice President", "Vice President, Associate Relations", "Gesellschafter | Recruiter"])
def test_vice_president_is_not_top_tier(title):
    assert classify_title(title) == "fail"


@pytest.mark.parametrize("title", [
    "Assistent to the Managing Director", "Assistentin der Geschäftsführung", "Assistente del Direttore Generale",
    "Asistente de Dirección", "Praktikant Geschäftsführung", "Stagiaire Directeur Commercial", "Werkstudent Vertrieb",
])
def test_non_english_assistant_intern_always_fail(title):
    assert classify_title(title) == "fail"


@pytest.mark.parametrize("title", [
    "PRESIDENTE", "Presidente e Amministratore Delegato", "Proprietario", "Koncern-VD", "VD", "Dyrektor HR",
    "Prezes Zarządu", "Direktor", "Administrerende direktør", "Adm. direktør", "Daglig leder", "Toimitusjohtaja",
    "Direttore Generale", "Direttrice Commerciale", "Jednatel", "Ügyvezető igazgató", "Ředitel", "Directora General",
    "Vicepresidente", "Vicepresidenta Comercial",
])
def test_senior_titles_in_more_european_languages_pass(title):
    assert classify_title(title) == "pass"


@pytest.mark.parametrize("title", [
    "Koordinator, Office of the VD", "Assistente del Presidente", "Specialist to the Prezes",
])
def test_rank_words_still_fail_when_the_top_word_is_someone_else(title):
    assert classify_title(title) == "fail"
