# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# ===== Einstellungen =====
ENABLE_CSV_EXPORT = False  # auf True setzen, um CSV-Download zu zeigen

st.set_page_config(page_title="PIKE-P Selbstlerntest", layout="wide")
st.title("PIKE-P Selbstlerntest (Informationskompetenzen für Psycholog:innen)")
st.caption("Inoffizielle Selbstlern-Version – bitte Originalquelle (CC BY-SA 4.0) zitieren: "
           "Rosman, Mayer & Krampen (2019), Open Test Archive (ZPID).")

# ===== Instruktionen + Skala =====
st.markdown("""
<div style='border:1px solid #ddd;border-radius:8px;padding:14px;background:#fafafa'>
  <b>Instruktionen</b>
  <ul>
    <li>Zu jedem Item werden <b>vier Vorgehensweisen (A–D)</b> gezeigt.</li>
    <li>Bewerte <b>jede</b> der vier Vorgehensweisen auf einer Skala von <b>1 bis 5</b> (Wie geeignet?).</li>
    <li>Klicke auf <b>Auswerten</b>, um deinen Gesamtscore zu erhalten.</li>
  </ul>
  <div><b>Antwortskala (1–5):</b> 1 = völlig ungeeignet · 2 = eher ungeeignet · 3 = teils/teils · 4 = eher geeignet · 5 = sehr gut geeignet</div>
</div>
""", unsafe_allow_html=True)

# ===== Sidebar: Anzeigeoptionen =====
with st.sidebar:
    st.header("Anzeige")
    layout_mode = st.radio("Layout", ["Untereinander", "Kompakt (2 Spalten)"], index=0)
    base_font = st.slider("Schriftgröße (px)", 14, 22, 17)
    st.markdown(
        f"<style>html, body, [class*='css']{{font-size:{base_font}px}}</style>",
        unsafe_allow_html=True
    )
QUESTION_FONT_PX = 22  # z.B. 22px
st.markdown(
    f"""
    <style>
    /* Expander-Überschriften (Fragen) größer darstellen */
    div[data-testid="stExpander"] div[role="button"] p {{
        font-size: {QUESTION_FONT_PX}px !important;
        font-weight: 600 !important;
        line-height: 1.35 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ===== Items =====
items = [
    ("pp01_s1_f1",
     "1) In einem Vertiefungsseminar sollen Sie eine 10-seitige Hausarbeit zum Thema „Die Entwicklung des Selbstwertgefühls im Jugendalter“ schreiben. Wie beginnen Sie Ihre Vorbereitung?",
     (
         "A) Ich lese ein Einführungslehrbuch über die Entwicklung im Jugendalter, weil man diese spezifische Fragestellung nur beantworten kann, wenn man genug über die allgemeine Entwicklung weiß.",
         "B) Ich kläre zuerst einmal ganz genau, was man unter „Selbstwertgefühl“ versteht, und beschaffe mir dazu mehrere einführende Buchkapitel zum Thema.",
         "C) Ich überlege, was ich bereits zum Thema weiß und was in anderen Lehrveranstaltungen dazu behandelt wurde.",
         "D) Ich schreibe mir auf, welche Synonyme bzw. welche verwandten Begriffe es zu den zentralen Konzepten des Themas gibt (z. B. zu Selbstwertgefühl „Selbstwert“, „Selbstsicherheit“; zu Jugendalter „Adoleszenz“) und wie diese im Englischen lauten."
     )
    ),
    ("pp02_s1_f1",
     "2) Die folgenden fünf Punkte beschreiben einzelne Schritte bei der Vorbereitung einer Literatursuche. Bitte geben Sie für jede der folgenden vier Abfolgen der fünf Schritte an, für wie geeignet Sie sie halten.",
     (
         "A) 2–5–4–1–3: Lesen der Aufgabenstellung – Identifikation wichtiger Konzepte – Kurze, einfache Suchen – Ermitteln (zusätzlicher) Suchbegriffe – Verknüpfen/Eingabe der Suchphrase",
         "B) 2–5–1–4–3: Lesen der Aufgabenstellung – Identifikation wichtiger Konzepte – Ermitteln (zusätzlicher) Suchbegriffe – Kurze, einfache Suchen – Verknüpfen/Eingabe der Suchphrase",
         "C) 2–1–4–5–3: Lesen der Aufgabenstellung – Ermitteln (zusätzlicher) Suchbegriffe – Kurze, einfache Suchen – Identifikation wichtiger Konzepte – Verknüpfen/Eingabe der Suchphrase",
         "D) 2–1–5–4–3: Lesen der Aufgabenstellung – Ermitteln (zusätzlicher) Suchbegriffe – Identifikation wichtiger Konzepte – Kurze, einfache Suchen – Verknüpfen/Eingabe der Suchphrase"
     )
    ),
    ("pp03_s1_f2",
     "3) Sie möchten ein Referat über die Intelligenzmessung bei schizophrenen Patienten vorbereiten. Der folgende, ältere Artikel liegt Ihnen vor:\n\nLidz, T., Gay, J. R., & Tietze, C. (1942). Intelligence in cerebral deficit states and schizophrenia measured by Kohs Block Test. Archives of Neurology and Psychiatry, 48(4), 568–582.\n\nWie gehen Sie vor, um weitere Artikel zu finden?",
     (
         "A) Schlagwörter des Artikels extrahieren und als Ausgangspunkt für weitere Suchen (z. B. Fachdatenbank) nutzen.",
         "B) Nach weiteren Artikeln derselben Autor:innen suchen.",
         "C) In einer Fachdatenbank/Google Scholar nach Artikeln suchen, die den Artikel zitiert haben.",
         "D) Im Literaturverzeichnis des Artikels recherchieren."
     )
    ),
    ("pp04_s1_f2",
     "4) Sie möchten eine Hausarbeit über den Erwerb von Ängsten schreiben. Der folgende, soeben erschienene Artikel liegt Ihnen vor:\n\nWegerer, M., Blechert, J., & Wilhelm, F. H. (2013). Emotionales Lernen: Ein naturalistisches experimentelles Paradigma zur Untersuchung von Angsterwerb und Extinktion mittels aversiver Filme. Zeitschrift für Psychiatrie, Psychologie und Psychotherapie, 61(2), 93–103.\n\nWie gehen Sie vor, um nach weiterer Literatur zu suchen?",
     (
         "A) Schlagwörter extrahieren und als Ausgangspunkt für weitere Suchen nutzen.",
         "B) Nach weiteren Artikeln derselben Autor:innen suchen.",
         "C) Zitationssuche (Fachdatenbank/Google Scholar).",
         "D) Literaturverzeichnis des Artikels durchsuchen."
     )
    ),
    ("pp05_s1_f3",
     "5) Sie bereiten eine Hausarbeit vor. Der Arbeitstitel lautet: „Der Einfluss von Lebenszufriedenheit und Selbstwirksamkeitserwartungen auf psychosomatische Beschwerden“. Wie geeignet sind folgende Suchanfragen?",
     (
         "A) Einfluss Lebenszufriedenheit Selbstwirksamkeitserwartungen „psychosomatische Beschwerden“",
         "B) Lebenszufriedenheit Selbstwirksamkeitserwartungen „psychosomatische Beschwerden“",
         "C) Einfluss Lebenszufriedenheit Selbstwirksamkeitserwartungen auf psychosomatische Beschwerden",
         "D) Der Einfluss von Lebenszufriedenheit und Selbstwirksamkeitserwartungen auf psychosomatische Beschwerden"
     )
    ),
    ("pp06_s1_f3",
     "6) Kurzreferat: „Wirksamkeit der Therapietechnik ‚Flooding‘ bei Spinnenphobie“. Wie gut eignen sich folgende Suchbegriffe?",
     ("A) Wirksamkeit", "B) Spinnenphobie", "C) Therapietechnik", "D) Flooding")
    ),
    ("pp07_s1_f4",
     "7) Hausarbeit: „Willenstendenzen im Rubikonmodell der Handlungsphasen“. Google Scholar liefert nur 1 Treffer. Wie beurteilen Sie folgende Änderungen (Begriffe mit UND verknüpft)?",
     (
         "A) „Motivation“ „Wunsch“ „Volition“ „Wille“ „Rubikonmodell“",
         "B) „Rubikonmodell“ „Volition“",
         "C) „Rubikonmodell“ „Wille“",
         "D) „Handlungsphasen“ „Modell“ „Wille“"
     )
    ),
    ("pp08_s1_f4",
     "8) Referat: „Wirksamkeit von Belohnung und Bestrafung bei Kleinkindern“. Suche mit „Wirksamkeit“, „Belohnung“, „Bestrafung“, „Kleinkinder“ ergibt viele irrelevante Ergebnisse. Wie beurteilen Sie folgende Änderungen (UND-Verknüpfung)?",
     (
         "A) „operante Konditionierung“ Kleinkinder",
         "B) „empirische Befunde“ Wirksamkeit Belohnung Bestrafung Kleinkinder",
         "C) Konditionierung Kleinkinder Verstärkung",
         "D) „klassische Konditionierung“ Kleinkinder"
     )
    ),
    ("pp09_s1_f5",
     "9) Einstiegslektüre zur arbeitsbezogenen Stressforschung – wie geeignet sind folgende Literaturarten?",
     (
         "A) Empirische Arbeiten zu unterschiedlichen Aspekten",
         "B) Populärpsychologische Ratgeber",
         "C) Review-Artikel",
         "D) Metaanalysen"
     )
    ),
    ("pp10_s1_f5",
     "10) Zusammenhang Zeitdruck ↔ Burnout begründen – wie geeignet sind folgende Literaturarten?",
     (
         "A) Review-Artikel",
         "B) Einzelne empirische Arbeiten",
         "C) Metaanalysen",
         "D) Veröffentlichungen statistischer Dienste"
     )
    ),
    ("pp11_s1_f6",
     "11) Bandura-Artikel „Human agency in social cognitive theory“ – wo erschien er? Wie geeignet sind folgende Hilfsmittel?",
     ("A) PsycINFO", "B) PSYNDEX", "C) Bibliothekskatalog", "D) Google Scholar")
    ),
    ("pp12_s1_f6",
     "12) Lazarus-Artikel, Titel vergessen – wie geeignet sind folgende Hilfsmittel?",
     ("A) DBIS-Autorensuche", "B) Google Scholar (Autorensuche)", "C) Bibliothekskatalog (Autorensuche)", "D) PsycINFO (Autorensuche)")
    ),
    ("pp13_s1_f6",
     "13) Empirische Arbeiten zu „Learning Strategies“ (6–12 Jahre) – wie geeignet sind folgende Hilfsmittel?",
     ("A) Bibliothekskatalog", "B) PsycINFO", "C) Google Scholar", "D) PSYNDEX")
    ),
    ("pp14_s2_f1",
     "14) Studie: Vergleich „Drug Therapy“ vs. „Psychotherapy“ bei ADS-Kindern – wie gut eignen sich folgende Verknüpfungen?",
     (
         "A) \"Attention Deficit Disorder\" UND \"Drug Therapy\" ODER \"Psychotherapy\"",
         "B) \"Attention Deficit Disorder\" UND \"Drug Therapy\" UND \"Psychotherapy\"",
         "C) \"Drug Therapy\" ODER \"Psychotherapy\" BEI \"Attention Deficit Disorder\"",
         "D) \"Attention Deficit Disorder\" UND \"Drug Therapy\" NICHT \"Psychotherapy\""
     )
    ),
    ("pp15_s2_f1",
     "15) Studie zur Diagnostik von Hochbegabung bei Kindern – wie gut eignen sich folgende Such-Formulierungen?",
     (
         "A) „Diagnostik“ ODER „Hochbegabung“ ODER „Kinder“",
         "B) „Diagnostik“ UND „Hochbegabung“ UND „Kinder“",
         "C) „Diagnostik“ UND „Hochbegabung“ NICHT „Jugendliche“ NICHT „Erwachsene“",
         "D) „Diagnostik“ UND „Hochbegabung“ ODER „Kinder“"
     )
    ),
    ("pp16_s2_f2",
     "16) Thema „Zeitdruck am Arbeitsplatz“ – uneinheitliche englische Begriffe. Wie geeignet sind folgende Vorgehensweisen?",
     (
         "A) Drei Suchen („Work Load“, „Time Pressure“, „Work Pressure“) und verknüpfen",
         "B) Zuerst im Fachwörterbuch verbreitetsten Begriff ermitteln",
         "C) Einfache Suche – Synonyme automatisch einbezogen",
         "D) Thesaurus der Fachdatenbank prüfen (verknüpfte Schlagworte)"
     )
    ),
    ("pp17_s2_f2",
     "17) Längsschnittstudien zur Wirksamkeit der kognitiven Verhaltenstherapie – Vorgehen, um wenig zu übersehen?",
     (
         "A) Zwei Thesaurus-Suchen („cognitive behavior therapy“ UND „longitudinal studies“), dann UND",
         "B) „cognitive behavior therapy longitudinal“ in die Suchmaske",
         "C) Schlagwort „cognitive behavior therapy“ UND Feld „Methodology: Longitudinal Empirical Study“",
         "D) Schlagwort „longitudinal study“ UND Feld „Classification Codes: Cognitive Therapy“"
     )
    ),
    ("pp18_s2_f3",
     "18) Heckhausen-Artikel (1964) – Titel entfallen. Wie am schnellsten finden?",
     (
         "A) „Heckhausen“ UND „1964“ in die Suchmaske",
         "B) Autorensuche „Heckhausen“, Ergebnisse nach Jahr sortieren",
         "C) Autorensuche „Heckhausen“ + Filter Erscheinungsjahr 1964",
         "D) Thesaurus „Erscheinungsjahr“ = 1964 UND Autor „Heckhausen“"
     )
    ),
    ("pp19_s2_f3",
     "19) Dissertationen mit FPI-R finden – Vorgehen?",
     (
         "A) „Freiburger Persoenlichkeits-Inventar“ UND „revidierte Fassung“ + Publikationstyp „Dissertation“",
         "B) Thesaurus-Suche „Dissertation“ UND FPI-R",
         "C) „Freiburger Persoenlichkeits-Inventar“ UND „Dissertation“",
         "D) „FPI-R“ + Publikationstyp „Dissertation“"
     )
    ),
    ("pp20_s2_f4",
     "20) Wie geeignet sind folgende Suchanfragen, um den Bibliotheksstandort der Publikation zu finden?\n\n"
     "Mönks, F. J.; van Boxtel, H.; Roelofs, J.; Sanders, M. (1986). The identification of gifted children in secondary education and a description of their situation in Holland. "
     "In: Heller, K. A.; Feldhusen, J. F. (Hrsg.), Identifying and nurturing the gifted: An international perspective. Toronto: Hans Huber. ISBN 0-920887-11-2 (auch: ISBN 3-456-81523-9).",
     (
         "A) ISBN (0-920887-11-2)",
         "B) Mönks The identification of gifted children in secondary education",
         "C) Vollständiges Zitat (wie oben)",
         "D) Heller Identifying and nurturing the gifted"
     )
    ),
    ("pp21_s2_f4",
     "21) Wie geeignet sind folgende Suchanfragen, um den Bibliotheksstandort von Schachter & Singer (1962) zu finden?",
     (
         "A) Psychological Review",
         "B) Schachter, S., & Singer, J. E. (1962). Cognitive, social, and physiological determinants of emotional state. Psychological Review, 69(5), 379–399.",
         "C) 0033-295X (ISSN)",
         "D) Schachter Cognitive social and physiological determinants of emotional state"
     )
    ),
    ("pp22_s2_f4",
     "22) Sie benötigen: „Richard S. Lazarus – Stress, Appraisal, and Coping“. Wie gehen Sie vor?",
     (
         "A) OPAC: „Lazarus Stress Appraisal Coping“",
         "B) Fachdatenbank-Suche",
         "C) ISBN recherchieren und im OPAC eingeben",
         "D) Internet-Suchmaschine (online verfügbar?)"
     )
    ),
]

# ===== Bewertung erfassen (Radio, ohne Default; Pflichtfeld-Check möglich) =====
responses: dict[str, dict[str, int | None]] = {}

for item_id, title, choices in items:
    with st.expander(title, expanded=(layout_mode == "Untereinander")):
        if layout_mode == "Kompakt (2 Spalten)":
            cols = st.columns(2)
            for i in range(2):
                with cols[i]:
                    for j in range(2):
                        idx = i*2 + j
                        label = chr(65+idx)  # A-D
                        st.markdown(f"**{choices[idx]}**")
                        responses.setdefault(item_id, {})[label] = st.radio(
                            f"{item_id}_{label}",
                            options=[1, 2, 3, 4, 5],
                            index=None,  # kein Default -> Pflichtfeld möglich
                            horizontal=True,
                            label_visibility="collapsed",
                            key=f"{item_id}_{label}"
                        )
                        st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)
        else:
            for idx in range(4):
                label = chr(65+idx)
                st.markdown(f"**{choices[idx]}**")
                responses.setdefault(item_id, {})[label] = st.radio(
                    f"{item_id}_{label}",
                    options=[1, 2, 3, 4, 5],
                    index=None,
                    horizontal=True,
                    label_visibility="collapsed",
                    key=f"{item_id}_{label}"
                )
                st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)

st.markdown("---")

# ===== Scoring-Logik =====
def score_item(item_id: str, r: dict[str, int]) -> int:
    s=0
    A,B,C,D = r["A"], r["B"], r["C"], r["D"]
    if item_id=="pp01_s1_f1":
        s += (B>=A) + (C>=A) + (D>=B) + (D>A)
    elif item_id=="pp02_s1_f1":
        s += (A>C) + (A>D) + (D>C)
    elif item_id=="pp03_s1_f2":
        s += (A>D) + (B>=D) + (C>=D)
    elif item_id=="pp04_s1_f2":
        s += (A>C) + (B>C) + (D>C)
    elif item_id=="pp05_s1_f3":
        s += (B>A) + (B>C) + (B>D)
    elif item_id=="pp06_s1_f3":
        s += (B>A) + (B>C) + (D>C)
    elif item_id=="pp07_s1_f4":
        s += (B>A) + (D>=A) + (B>=C) + (B>D) + (C>A)
    elif item_id=="pp08_s1_f4":
        s += (A>B) + (A>D) + (C>=B) + (C>D)
    elif item_id=="pp09_s1_f5":
        s += (A>B) + (C>=A) + (C>B) + (D>B) + (C>=D)
    elif item_id=="pp10_s1_f5":
        s += (A>D) + (C>=B) + (B>D) + (C>D)
    elif item_id=="pp11_s1_f6":
        s += (A>B) + (A>C) + (A>=D) + (D>=C)
    elif item_id=="pp12_s1_f6":
        s += (A>=C) + (B>=C) + (D>B) + (D>C)
    elif item_id=="pp13_s1_f6":
        s += (B>A) + (C>A) + (D>A) + (B>C) + (D>=C)
    elif item_id=="pp14_s2_f1":
        s += (B>A) + (B>C) + (B>D) + (A>=C)
    elif item_id=="pp15_s2_f1":
        s += (B>A) + (C>A) + (B>C) + (B>D) + (C>D)
    elif item_id=="pp16_s2_f2":
        s += (A>=B) + (D>=A) + (D>B) + (D>C)
    elif item_id=="pp17_s2_f2":
        s += (A>B) + (C>B) + (C>D) + (A>D)
    elif item_id=="pp18_s2_f3":
        s += (C>A) + (C>B) + (C>D)
    elif item_id=="pp19_s2_f3":
        s += (A>B) + (A>=C) + (D>=A) + (D>B) + (D>C)
    elif item_id=="pp20_s2_f4":
        s += (A>B) + (A>C) + (D>B) + (D>C)
    elif item_id=="pp21_s2_f4":
        s += (A>B) + (A>D) + (C>=B) + (D>=B)
    elif item_id=="pp22_s2_f4":
        s += (A>B) + (A>D) + (C>B)
    return int(s)

# ===== Auswertung =====
if st.button("Auswerten", type="primary"):
    # Pflichtfeld-Check
    missing = []
    for item_id, title, _ in items:
        ans = responses.get(item_id, {})
        if any(v is None for v in ans.values()):
            missing.append(title)
    if missing:
        st.warning("Bitte alle Antworten vergeben. Noch offen:\n- " + "\n- ".join(missing))
        st.stop()

    rows = []
    total = 0
    for item_id, title, _ in items:
        s = score_item(item_id, responses[item_id])  # type: ignore[arg-type]
        total += s
        rows.append({"Item": title, "Score": s})

    df = pd.DataFrame(rows)
    pcnt = round((total/86)*100, 2)

    st.success(f"Gesamtscore (PIKE): {total} / 86  ·  PIKE_PCNT: {pcnt}%")
    st.dataframe(df, use_container_width=True)

    if ENABLE_CSV_EXPORT:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Ergebnisse als CSV herunterladen",
                           data=csv,
                           file_name=f"pike_result_{now}.csv",
                           mime="text/csv")
