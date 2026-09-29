"""Title-level guard for 'director and above'.

Provider seniority enums leak a few percent of sub-director titles. This classifier looks at
the raw title and returns 'pass', 'fail' or 'unknown' (no title to judge). Unknown rows are
kept; failing rows are dropped from the export.
"""
import re
import unicodedata

_STRONG = re.compile(
    r"\b(directors?|directeur|directrice|diretor|diretora|directora|vp|svp|evp|vice[- ]?president[ea]?|head|chief|c[a-z]{1,2}o|"
    r"president|owner|founder|co[- ]?founder|proprietor|board member|chair|chairman|chairwoman|chairperson|"
    r"general manager|managing member|entrepreneur|fondateur|fondatrice|proprietaire|"
    # German / Dutch / Spanish / Italian senior titles (text is accent-folded first: geschaftsfuhrer = Geschäftsführer)
    r"geschaftsfuhrer(?:in)?|geschaftsfuhrend(?:e|er)?|inhaber(?:in)?|(?:mit)?grunder(?:in)?|vorstand\w*|"
    r"(?:mede-?)?eigenaar|(?:mede-?)?oprichter|fundador(?:a)?|cofundador(?:a)?|propietari[oa]|"
    r"(?:co)?fondatore|fondatrice|titolare|amministratore delegato|"
    # Italian / Spanish / Polish / Nordic / Czech / Slovak / Hungarian (accent-folded; Nordic ø does not fold)
    r"presidente|proprietari[oa]|direttore|direttrice|dyrektor|prezes|direkt(?:or|ør)(?:in)?|vd|toimitusjohtaja|"
    r"daglig leder|jednatel(?:ka)?|reditel(?:ka)?|riaditel(?:ka)?|ugyvezeto|igazgato)\b"
)
# Top-tier titles: pass even when a rank word from Algo's exclude list is present ("Founder & Specialist Recruiter").
_TOP = re.compile(
    r"\b(owner|founder|co[- ]?founder|cofounder|proprietor|managing director|managing partner|ceo|c[a-z]{1,2}o|"
    r"chief\b.*\bofficer|chair(?:man|woman|person)?|geschaftsfuhrer(?:in)?|geschaftsfuhrend(?:e|er)?|inhaber(?:in)?|"
    r"(?:mit)?grunder(?:in)?|(?:mede-?)?eigenaar|(?:mede-?)?oprichter|fondateur|fondatrice|fundador(?:a)?|"
    r"cofundador(?:a)?|(?:co)?fondatore|titolare|amministratore delegato|directeur general|directora? general|"
    r"proprietari[oa]|prezes|vd|verkstallande direktor|adm(?:inistrerende|\.)? direkt(?:or|ør)|daglig leder|"
    r"toimitusjohtaja|direttore generale|dyrektor generalny|jednatel(?:ka)?|ugyvezeto)\b"
    r"|(?<!vice )(?<!vice-)\bpresident(?:e|a)?\b"
)
# Weak positives pass only when no individual-contributor / manager word is present.
# "socio" = partner (ES/IT/PT) only as a role, not in "socio-sanitario" (care worker), "socio-educative" etc.
_WEAK = re.compile(r"\b(partner|principal|md|gesellschafter(?:in)?)\b"
                   r"|\bsoci[oa]\b(?![- ]?(?:sanitari|educ|assist|profession|cultur|econom|politi|sanitair))")
_IC_WORDS = re.compile(
    r"\b(manager|coordinator|specialist|associate|analyst|executive|representative|consultant|engineer|recruiter|"
    r"assistant|intern|trainee|student|apprentice)\b"
)
# Always fail, whatever else the title says ("Assistant to the CEO", "AVP" = assistant vice president).
_HARD_FAIL = re.compile(
    r"\b(assistant|intern|trainee|student|apprentice|avp|"
    # non-English equivalents (accent-folded): DE / NL / FR / ES / IT / PT
    r"assistent(?:in)?|assistente|asistente|praktikant(?:in)?|werkstudent(?:in)?|auszubildende[r]?|stagiair[e]?|"
    r"tirocinante|becari[oa]|estagiari[oa])\b|advisory board|board advisor|advisor to the board"
)
# Algo Acquisition's exclude list (sourcing/icp-overview.md, "Seniority filter"): fail unless the title is top-tier, so
# "Associate Director" / "Business Development Representative" fail but "Founder & Specialist Recruiter" passes.
_RANK_FAIL = re.compile(
    r"\b(associate|coordinator|koordinator(?:in)?|coordinatore|coordinador(?:a)?|specialist|analyst|representative|bdr|sdr|account executive|"
    r"talent (?:acquisition )?partner|acquisition partner)\b"
)
_TOKEN = re.compile(r"[a-z0-9]+|[&,/|-]")
_PARTNER_QUALIFIERS = {"&", ",", "/", "|", "-", "and", "senior", "managing", "general", "equity", "founding", "salaried", "associate", "junior", "name"}
_PARTNER_COMPOUNDS = {"manager", "management", "marketing", "success", "relations", "program", "programs", "development", "sales",
                      "specialist", "coordinator", "enablement", "operations", "support", "engineer", "executive"}
_DOTTED_ABBREV = re.compile(r"\b(?:[a-z]\.\s?){2,}")  # v.p. / s.v.p. / c.e.o.


def _fold(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).lower()


def _standalone_partner(tokens):
    """'Partner' is a role of its own at the start / after a separator or qualifier and not part of a compound noun."""
    for i, tok in enumerate(tokens):
        if tok != "partner":
            continue
        prev = tokens[i - 1] if i > 0 else "&"
        nxt = tokens[i + 1] if i + 1 < len(tokens) else None
        if prev in _PARTNER_QUALIFIERS and nxt not in _PARTNER_COMPOUNDS:
            return True
    return False


def classify_title(title):
    if not title or not isinstance(title, str) or not title.strip():
        return "unknown"
    t = _fold(title)
    t = _DOTTED_ABBREV.sub(lambda m: m.group(0).replace(".", "").replace(" ", "") + " ", t)
    t = re.sub(r"\bproduct owner\b", "productowner", t)  # an IC role, not an owner
    if _HARD_FAIL.search(t):
        return "fail"
    # a top-tier word only counts if it is the person's own role, not "Coordinator, Office of the CEO"
    own_role = re.sub(r"\b(?:of|to|for)\s+(?:the\s+)?\w+", " ", t)
    if _RANK_FAIL.search(t) and not _TOP.search(own_role):
        return "fail"
    if _STRONG.search(t):
        return "pass"
    if _standalone_partner(_TOKEN.findall(t)):
        return "pass"
    if _WEAK.search(t) and not _IC_WORDS.search(t):
        return "pass"
    return "fail"
