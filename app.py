# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# ===== Einstellungen =====
ENABLE_CSV_EXPORT = False
ALLOW_PARTIAL = False  # Normvergleich nur bei vollständiger Bearbeitung; keine implizite Mittelwert-Imputation


st.set_page_config(page_title="PIKE-P Selbstlerntest", layout="wide")
st.title("PIKE-P Selbstlerntest (Informationskompetenzen für Psycholog:innen)")
st.caption("Inoffizielle Selbstlern-Version – bitte Originalquelle (CC BY-SA 4.0) zitieren: "
           "Rosman, Mayer & Krampen (2019), Open Test Archive (ZPID).")

st.info(
    "Hinweis zur Fassung 2026: Einige Formulierungen wurden behutsam an heutige Rechercheoberflächen angepasst. "
    "Itemstruktur, Antwortreihenfolge und das originale Pairwise-Scoring bleiben unverändert. "
    "Die publizierten Vergleichswerte sind daher weiterhin als Orientierung nutzbar, aber nicht als neu validierte Normwerte."
)

st.caption("Neu: Wahlweise Vollversion (22 Situationen) oder didaktische Kurzversion (11 Situationen).")

# ===== Instruktionen + Skala =====
partial_hint = (
    "Teilbearbeitung ist aktiviert. Ein Normvergleich wird nur angezeigt, wenn alle vier Antworten eines Items vorliegen."
    if ALLOW_PARTIAL
    else "Bitte alle Antworten vergeben. Für eine faire Auswertung und den Referenzvergleich ist eine vollständige Bearbeitung erforderlich."
)

st.markdown(f"""
<div style='border:1px solid #ddd;border-radius:8px;padding:14px;background:#fafafa'>
  <b>Instruktionen</b>
  <ul>
    <li>Zu jedem Item werden <b>vier Vorgehensweisen (A–D)</b> gezeigt.</li>
    <li>Bewerte <b>jede</b> der vier Vorgehensweisen auf einer Skala von <b>1 bis 5</b> (Wie geeignet?).</li>
    <li>Der Test ist in <b>fünf kurze Abschnitte</b> gegliedert. Bearbeite jeweils alle vier Bewertungen einer Situation.</li>
    <li>Am Ende des fünften Abschnitts kannst du deinen Gesamtscore und dein Lernprofil anzeigen.</li>
    <li>Plane für die vollständige Bearbeitung ungefähr <b>20–25 Minuten</b> ein.</li>
    <li><b>Hinweis:</b> {partial_hint}</li>
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

QUESTION_FONT_PX = 22  # gewünschte Größe in px

st.markdown(
    f"""
    <style>
    /* Robuste Overrides für verschiedene Streamlit-Versionen */
    div[data-testid="stExpander"] > details > summary,
    div[data-testid="stExpander"] > details > summary * ,
    div[data-testid="stExpander"] .streamlit-expanderHeader {{
        font-size: {QUESTION_FONT_PX}px !important;
        font-weight: 700 !important;
        line-height: 1.35 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
.pike-scale-hint{
  font-size: 0.9rem; 
  opacity: 0.8; 
  margin-top: 0.15rem; 
  margin-bottom: 0.35rem;
}
</style>
""", unsafe_allow_html=True)

SCALE_HINT = "1 = völlig ungeeignet · 2 = eher ungeeignet · 3 = teils/teils · 4 = eher geeignet · 5 = sehr gut geeignet"
SCALE_HINT_HTML = f"<div class='pike-scale-hint'>{SCALE_HINT}</div>"
# ===== Items =====

items = [
    ("pp01_s1_f1",
     "1) In einem Vertiefungsseminar sollen Sie eine 10-seitige Hausarbeit zum Thema „Die Entwicklung des Selbstwertgefühls im Jugendalter“ schreiben. Wie beginnen Sie Ihre Vorbereitung?",
     (
        "A) Ich lese zunächst ein Einführungslehrbuch über die Entwicklung im Jugendalter, weil man diese spezifische Fragestellung nur beantworten kann, wenn man genug über die allgemeine Entwicklung weiß.",
        "B) Ich kläre zuerst ganz genau, was man unter „Selbstwertgefühl“ versteht, und beschaffe mir dazu mehrere einführende Buchkapitel zum Thema.",
        "C) Ich überlege, was ich bereits zum Thema weiß und was in anderen Lehrveranstaltungen dazu behandelt wurde, um darauf aufzubauen.",
        "D) Ich schreibe mir Synonyme bzw. verwandte Begriffe zu den zentralen Konzepten des Themas (z. B. zu „Selbstwertgefühl“ auch „Selbstwert“, „Selbstsicherheit“; zu „Jugendalter“ auch „Adoleszenz“) auf und recherchiere auch die entsprechenden englischen Begriffe."
     )
    ),
    ("pp02_s1_f1",
     "2) Vorbereitung einer Literatursuche: Welche Reihenfolge ist geeignet?",
     (
        "A) Reihenfolge: 2 – 5 – 4 – 1 – 3",
        "B) Reihenfolge: 2 – 5 – 1 – 4 – 3",
        "C) Reihenfolge: 2 – 1 – 4 – 5 – 3",
        "D) Reihenfolge: 2 – 1 – 5 – 4 – 3"
     )
    ),
    ("pp03_s1_f2",
     "3) Sie möchten ein Referat über die Intelligenzmessung bei schizophrenen Patientinnen und Patienten vorbereiten. Der folgende, ältere Artikel liegt Ihnen vor:\n\n"
     "Lidz, T., Gay, J. R., & Tietze, C. (1942). Intelligence in cerebral deficit states and schizophrenia measured by Kohs Block Test. Archives of Neurology and Psychiatry, 48(4), 568–582.\n\n"
     "Wie gehen Sie vor, um weitere Artikel zu finden?",
     (
        "A) Ich extrahiere die Schlagwörter des Artikels und nutze diese als Ausgangspunkt für weitere Suchen, zum Beispiel in einer Fachdatenbank.",
        "B) Ich suche gezielt nach weiteren Artikeln dieser Autorinnen und Autoren, da viele Forschende mehrere Beiträge zum gleichen Thema publizieren.",
        "C) Ich recherchiere in einer Fachdatenbank oder bei Google Scholar nach Artikeln, die diesen Artikel zitiert haben (Zitationssuche).",
        "D) Ich suche im Literaturverzeichnis des Artikels nach weiteren relevanten Quellen."
     )
    ),
    ("pp04_s1_f2",
     "4) Sie möchten eine Hausarbeit über den Erwerb von Ängsten schreiben. Für diese Aufgabe versetzen Sie sich in das Erscheinungsjahr 2013: Der folgende Artikel ist gerade erschienen.\n\n"
     "Wegerer, M., Blechert, J., & Wilhelm, F. H. (2013). Emotionales Lernen: Ein naturalistisches experimentelles Paradigma zur Untersuchung von Angsterwerb und Extinktion mittels aversiver Filme. Zeitschrift für Psychiatrie, Psychologie und Psychotherapie, 61(2), 93–103.\n\n"
     "Wie gehen Sie vor, um nach weiterer Literatur zu suchen?",
     (
        "A) Ich extrahiere die Schlagwörter des Artikels und nutze diese als Ausgangspunkt für weitere Suchen in Fachdatenbanken.",
        "B) Ich suche nach weiteren Artikeln derselben Autorinnen und Autoren, da diese häufig mehrfach zum Thema publizieren.",
        "C) Ich nutze eine Zitationssuche in einer Fachdatenbank oder bei Google Scholar, um Arbeiten zu finden, die diesen Artikel zitiert haben.",
        "D) Ich werte das Literaturverzeichnis des Artikels systematisch aus."
     )
    ),
    ("pp05_s1_f3",
     "5) Sie bereiten eine Hausarbeit vor. Der Arbeitstitel lautet: „Der Einfluss von Lebenszufriedenheit und Selbstwirksamkeitserwartungen auf psychosomatische Beschwerden“. Wie geeignet sind folgende Suchanfragen, um nach relevanter Fachliteratur zu suchen?",
     (
        "A) Ich formuliere die Suche so: Einfluss Lebenszufriedenheit Selbstwirksamkeitserwartungen „psychosomatische Beschwerden“.",
        "B) Ich formuliere die Suche so: Lebenszufriedenheit Selbstwirksamkeitserwartungen „psychosomatische Beschwerden“.",
        "C) Ich formuliere die Suche als vollständigen Satz: Einfluss Lebenszufriedenheit Selbstwirksamkeitserwartungen auf psychosomatische Beschwerden.",
        "D) Ich formuliere die Suche noch ausführlicher als Titel: Der Einfluss von Lebenszufriedenheit und Selbstwirksamkeitserwartungen auf psychosomatische Beschwerden."
     )
    ),
    ("pp06_s1_f3",
     "6) Sie bereiten ein Kurzreferat mit dem Arbeitstitel „Wirksamkeit der Therapietechnik ‚Flooding‘ bei Spinnenphobie“ vor. Wie gut eignen sich die folgenden Suchbegriffe?",
     (
        "A) Ich verwende nur den allgemeinen Suchbegriff „Wirksamkeit“.",
        "B) Ich verwende den spezifischen Suchbegriff „Spinnenphobie“ (bzw. „arachnophobia“).",
        "C) Ich verwende den allgemeinen Suchbegriff „Therapietechnik“.",
        "D) Ich verwende den spezifischen Suchbegriff „Flooding“."
     )
    ),
    ("pp07_s1_f4",
     "7) Im Rahmen eines Seminars zur Motivationspsychologie bereiten Sie eine Hausarbeit vor. Der Arbeitstitel lautet: „Willenstendenzen im Rubikonmodell der Handlungsphasen“. Eine Suche mit den Suchbegriffen „Willenstendenzen“ und „Rubikonmodell der Handlungsphasen“ hat nur einen Treffer ergeben. Wie beurteilen Sie die folgenden Änderungen der Suchanfrage? (Die Suchbegriffe werden jeweils mit UND verknüpft.)",
     (
        "A) Ich suche mit den Begriffen „Motivation“, „Wunsch“, „Volition“, „Wille“ und „Rubikonmodell“.",
        "B) Ich suche mit den Begriffen „Rubikonmodell“ und „Volition“.",
        "C) Ich suche mit den Begriffen „Rubikonmodell“ und „Wille“.",
        "D) Ich suche mit den Begriffen „Handlungsphasen“, „Modell“ und „Wille“."
     )
    ),
    ("pp08_s1_f4",
     "8) Im Rahmen eines Seminars zur Lernpsychologie bereiten Sie ein Referat vor. Der Arbeitstitel lautet: „Befunde zur Wirksamkeit von Belohnung und Bestrafung bei Kleinkindern“. Eine Suche mit den Suchbegriffen „Wirksamkeit“, „Belohnung“, „Bestrafung“ und „Kleinkinder“ ergab viele irrelevante Ergebnisse. Wie beurteilen Sie die folgenden Möglichkeiten, Ihre Suche abzuändern? (Die Suchbegriffe werden jeweils mit UND verknüpft.)",
     (
        "A) Ich suche mit den Begriffen „operante Konditionierung“ und „Kleinkinder“.",
        "B) Ich suche mit den Begriffen „empirische Befunde“, „Wirksamkeit“, „Belohnung“, „Bestrafung“ und „Kleinkinder“.",
        "C) Ich suche mit den Begriffen „Konditionierung“, „Kleinkinder“ und „Verstärkung“.",
        "D) Ich suche mit den Begriffen „klassische Konditionierung“ und „Kleinkinder“."
     )
    ),
    ("pp09_s1_f5",
     "9) Sie planen eine Bachelorarbeit im Bereich der arbeitsbezogenen Stressforschung. Für wie geeignet halten Sie die folgenden Literaturarten, um sich in das neue Themengebiet einzuarbeiten?",
     (
        "A) Ich nutze empirische Arbeiten zu unterschiedlichen Aspekten des berufsbezogenen Stresserlebens.",
        "B) Ich nutze populärpsychologische Ratgeber zu arbeitsbezogenem Stress.",
        "C) Ich nutze Überblicksarbeiten im Sinne von Review-Artikeln zur arbeitsbezogenen Stressforschung.",
        "D) Ich nutze Metaanalysen zur arbeitsbezogenen Stressforschung."
     )
    ),
    ("pp10_s1_f5",
     "10) Nachdem Sie sich in das Themengebiet der arbeitsbezogenen Stressforschung eingearbeitet haben, postulieren Sie einen positiven Zusammenhang zwischen Zeitdruck und Burnout. Welche Literaturarten eignen sich, um dies möglichst überzeugend zu begründen?",
     (
        "A) Ich stütze mich auf Review-Artikel zum Zusammenhang zwischen Zeitdruck und Burnout.",
        "B) Ich stütze mich auf einzelne empirische Arbeiten zum Zusammenhang zwischen Zeitdruck und Burnout.",
        "C) Ich stütze mich auf Metaanalysen zum Zusammenhang zwischen Zeitdruck und Burnout.",
        "D) Ich stütze mich auf Veröffentlichungen eines statistischen Dienstes (z. B. Statistisches Bundesamt)."
     )
    ),
    ("pp11_s1_f6",
     "11) Ihr Dozent hat Ihnen den Artikel „Human agency in social cognitive theory“ von Albert Bandura empfohlen. Wie geeignet sind die folgenden Hilfsmittel, um herauszufinden, in welcher Zeitschrift der Artikel erschienen ist?",
     (
        "A) Ich recherchiere in der psychologischen Fachdatenbank PsycINFO.",
        "B) Ich recherchiere in der psychologischen Fachdatenbank PSYNDEX.",
        "C) Ich recherchiere im Bibliothekskatalog bzw. in der lokalen Titelsuche.",
        "D) Ich recherchiere in Google Scholar."
     )
    ),
    ("pp12_s1_f6",
     "12) Sie suchen einen Artikel von Richard S. Lazarus, kennen aber nicht mehr den genauen Titel. Wie geeignet sind die folgenden Hilfsmittel?",
     (
        "A) Ich nutze das Datenbank-Infosystem (DBIS), um eine geeignete Datenbank zu finden, und suche dort nach dem Autor.",
        "B) Ich suche in Google Scholar gezielt nach dem Autor.",
        "C) Ich suche im Bibliothekskatalog gezielt nach dem Autor.",
        "D) Ich suche in PsycINFO gezielt nach dem Autor."
     )
    ),
    ("pp13_s1_f6",
     "13) Sie benötigen mehrere empirische Arbeiten zu Lernstrategien („Learning Strategies“) von Schulkindern im Alter von 6 bis 12 Jahren. Wie geeignet sind die folgenden Hilfsmittel?",
     (
        "A) Ich suche im Bibliothekskatalog (vor allem Titel- und Bestandsnachweise).",
        "B) Ich recherchiere in der psychologischen Fachdatenbank PsycINFO.",
        "C) Ich recherchiere mit Google Scholar.",
        "D) Ich recherchiere in der psychologischen Fachdatenbank PSYNDEX."
     )
    ),
    ("pp14_s2_f1",
     "14) Sie suchen eine Studie, die medikamentöse Therapie („Drug Therapy“) und Psychotherapie („Psychotherapy“) bei Kindern mit ADS vergleicht. Wie gut eignen sich die folgenden Verknüpfungen?",
     (
        "A) Ich formuliere die Suche als: \"Attention Deficit Disorder\" UND \"Drug Therapy\" ODER \"Psychotherapy\".",
        "B) Ich formuliere die Suche als: \"Attention Deficit Disorder\" UND \"Drug Therapy\" UND \"Psychotherapy\".",
        "C) Ich formuliere die Suche als: \"Drug Therapy\" ODER \"Psychotherapy\" BEI \"Attention Deficit Disorder\".",
        "D) Ich formuliere die Suche als: \"Attention Deficit Disorder\" UND \"Drug Therapy\" NICHT \"Psychotherapy\"."
     )
    ),
    ("pp15_s2_f1",
     "15) Sie suchen eine Studie zur Diagnostik von Hochbegabung bei Kindern. Wie gut eignen sich die folgenden Suchanfragen?",
     (
        "A) Ich verknüpfe die Begriffe mit ODER: „Diagnostik“ ODER „Hochbegabung“ ODER „Kinder“.",
        "B) Ich verknüpfe die Begriffe mit UND: „Diagnostik“ UND „Hochbegabung“ UND „Kinder“.",
        "C) Ich schränke ein: „Diagnostik“ UND „Hochbegabung“ NICHT „Jugendliche“ NICHT „Erwachsene“.",
        "D) Ich formuliere: „Diagnostik“ UND „Hochbegabung“ ODER „Kinder“."
     )
    ),
    ("pp16_s2_f2",
     "16) In Ihrer Bachelorarbeit möchten Sie das Thema „Zeitdruck am Arbeitsplatz“ behandeln. Für „Zeitdruck“ existieren verschiedene englische Begriffe. Wie geeignet sind die folgenden Vorgehensweisen?",
     (
        "A) Ich führe drei separate Suchen nach „Work Load“, „Time Pressure“ und „Work Pressure“ aus und verknüpfe die Ergebnisse.",
        "B) Ich kläre zunächst anhand eines Fachwörterbuchs bzw. einer Terminologiehilfe, welcher Begriff fachlich üblich ist und vermutlich als Schlagwort genutzt wird.",
        "C) Ich führe eine einfache Suche mit einem der drei Begriffe durch und verlasse mich darauf, dass Synonyme automatisch einbezogen werden.",
        "D) Ich prüfe im Thesaurus bzw. kontrollierten Vokabular der Fachdatenbank, mit welchen Schlagworten die Begriffe verknüpft sind, und nutze diese gezielt."
     )
    ),
    ("pp17_s2_f2",
     "17) Sie suchen Längsschnittstudien („longitudinal study“) zur Wirksamkeit der kognitiven Verhaltenstherapie. Wie gehen Sie vor, um möglichst wenige Studien zu übersehen?",
     (
        "A) Ich starte zwei Thesaurus-Suchen nach „cognitive behavior therapy“ und „longitudinal studies“ und verknüpfe die Suchen anschließend mit UND.",
        "B) Ich gebe die freie Suchphrase „cognitive behavior therapy longitudinal“ ein.",
        "C) Ich suche nach dem Schlagwort „cognitive behavior therapy“ und kombiniere es – sofern die Datenbank dieses Feld anbietet – mit „Methodology“ = „Longitudinal Empirical Study“ (UND-Verknüpfung).",
        "D) Ich suche nach dem Schlagwort „longitudinal study“ und kombiniere es – sofern verfügbar – mit dem Feld „Classification Codes“ = „Cognitive Therapy“ (UND-Verknüpfung)."
     )
    ),
    ("pp18_s2_f3",
     "18) Sie suchen in einer Fachdatenbank einen bestimmten Artikel von Heinz Heckhausen aus dem Jahr 1964, kennen aber den Titel nicht. Wie gehen Sie vor?",
     (
        "A) Ich gebe „Heckhausen“ UND „1964“ direkt in die allgemeine Suchmaske ein.",
        "B) Ich führe eine Autorensuche nach „Heckhausen“ durch, sortiere die Ergebnisse nach Jahr und suche manuell den Jahrgang 1964.",
        "C) Ich nutze die Autorensuche nach „Heckhausen“ und schränke die Ergebnisse auf das Erscheinungsjahr 1964 ein.",
        "D) Ich verwende einen Thesaurus-Eintrag für „Erscheinungsjahr“ = 1964 und verknüpfe ihn mit der Autorensuche „Heckhausen“ über UND."
     )
    ),
    ("pp19_s2_f3",
     "19) Sie möchten herausfinden, ob es Dissertationen gibt, in denen das Freiburger Persönlichkeits-Inventar in der revidierten Fassung (FPI-R) angewandt wurde. Wie gehen Sie vor?",
     (
        "A) Ich suche nach „Freiburger Persönlichkeits-Inventar“ UND „revidierte Fassung“ und schränke den Publikationstyp auf „Dissertation“ ein.",
        "B) Ich starte eine Thesaurus-Suche nach „Dissertation“ und verknüpfe diese anschließend mit dem Begriff FPI-R über UND.",
        "C) Ich suche nach „Freiburger Persönlichkeits-Inventar“ UND „Dissertation“ ohne weitere Einschränkungen.",
        "D) Ich suche nach „FPI-R“ und schränke den Publikationstyp auf „Dissertation“ ein."
     )
    ),
    ("pp20_s2_f4",
     "20) Wie geeignet sind folgende Suchanfragen, die Sie in einen Bibliothekskatalog bzw. ein Discovery-System eingeben, um Bestand oder Zugang zur folgenden Publikation zu finden?\n\n"
     "Mönks, F. J.; van Boxtel, H.; Roelofs, J.; Sanders, M. (1986). The identification of gifted children in secondary education and a description of their situation in Holland. "
     "In: Heller, K. A.; Feldhusen, J. F. (Hrsg.), Identifying and nurturing the gifted: An international perspective. Toronto: Verlag Hans Huber. ISBN 0-920887-11-2 (auch: ISBN 3-456-81523-9).",
     (
        "A) Ich suche direkt mit der ISBN „0-920887-11-2“ im Bibliothekskatalog bzw. Discovery-System.",
        "B) Ich suche mit der Zeichenkette „Mönks The identification of gifted children in secondary education“.",
        "C) Ich gebe das vollständige Zitat wie oben in die Suchmaske ein.",
        "D) Ich suche mit der Zeichenkette „Heller Identifying and nurturing the gifted“."
     )
    ),
    ("pp21_s2_f4",
     "21) Wie geeignet sind folgende Suchanfragen, die Sie in einen Bibliothekskatalog bzw. ein Discovery-System eingeben, um Bestand oder Zugang zur Publikation Schachter, S., & Singer, J. E. (1962) zu finden?",
     (
        "A) Ich suche nur nach dem Zeitschriftentitel „Psychological Review“.",
        "B) Ich suche mit dem vollständigen Zitat: Schachter, S., & Singer, J. E. (1962). Cognitive, social, and physiological determinants of emotional state. Psychological Review, 69(5), 379–399.",
        "C) Ich suche mit der ISSN „0033-295X“ des Journals.",
        "D) Ich suche mit einer verkürzten Kombination: „Schachter Cognitive social and physiological determinants of emotional state“."
     )
    ),
    ("pp22_s2_f4",
     "22) Sie benötigen das folgende Buch: Lazarus, R. S., & Folkman, S. (1984). Stress, Appraisal, and Coping. New York: Springer Publishing Company. Wie gehen Sie vor?",
     (
        "A) Ich suche im Bibliothekskatalog bzw. Discovery-System nach „Lazarus Stress Appraisal Coping“.",
        "B) Ich suche in einer Fachdatenbank nach „Lazarus Stress Appraisal Coping“, da viele Bücher dort erfasst sind.",
        "C) Ich recherchiere die ISBN des Buches und gebe diese in den Bibliothekskatalog bzw. das Discovery-System ein.",
        "D) Ich suche mit einer allgemeinen Websuchmaschine, ob das Buch online verfügbar ist."
     )
    ),
]


# ===== Kurzversion (didaktisch, nicht separat validiert) =====
# Auswahl: je ein Item aus jedem der 10 Kompetenzbereiche + ein zusätzliches
# Beschaffungsitem. So bleibt die inhaltliche Breite der Originalfassung möglichst erhalten.
SHORT_ITEM_IDS = [
    "pp01_s1_f1",  # Planung
    "pp03_s1_f2",  # Pearl Growing
    "pp05_s1_f3",  # Suchbegriffe extrahieren
    "pp07_s1_f4",  # Suchbegriffe umformulieren
    "pp09_s1_f5",  # Publikationstypen
    "pp11_s1_f6",  # Suchwerkzeuge
    "pp14_s2_f1",  # Boolesche Operatoren
    "pp16_s2_f2",  # Thesaurus
    "pp18_s2_f3",  # Limiter / Suchfelder
    "pp20_s2_f4",  # Beschaffung
    "pp22_s2_f4",  # Beschaffung (zweites Item)
]

def get_active_items(all_items):
    if st.session_state.get("test_mode") == "short":
        return [item for item in all_items if item[0] in SHORT_ITEM_IDS]
    return all_items

# Zusatztexte, die innerhalb eines Items formatiert angezeigt werden.
ITEM_INTROS = {
    "pp02_s1_f1": """
Die folgenden fünf Punkte beschreiben einzelne Schritte bei der Vorbereitung einer Literatursuche:

1. **Ermitteln von (zusätzlichen) Suchbegriffen**  
   Zusätzliche Begriffe bestimmen, die die zentralen Konzepte der Fragestellung beschreiben.

2. **Lesen der Aufgabenstellung**  
   Die Aufgabenstellung aufmerksam und vollständig erfassen.

3. **Verknüpfen der Suchbegriffe und Eingabe der Suchphrase**  
   Die Suchbegriffe entsprechend der Fragestellung logisch miteinander verknüpfen und in die Suchmaske eingeben.

4. **Kurze, einfache Suchen**  
   Zunächst einfache Suchen mit einzelnen Konzepten oder Suchbegriffen durchführen.

5. **Identifikation wichtiger Konzepte**  
   Die zentralen Konzepte der Aufgabenstellung bestimmen und festhalten.

**Bitte geben Sie für jede der folgenden vier Abfolgen an, für wie geeignet Sie diese Reihenfolge halten.**
"""
}


# ===== Testmodus wählen =====
if "test_mode" not in st.session_state:
    st.session_state.test_mode = None

if st.session_state.test_mode is None:
    st.markdown("### Welche Version möchten Sie bearbeiten?")
    st.write(
        "Die Vollversion enthält alle 22 Situationen. "
        "Die Kurzversion enthält 11 ausgewählte Situationen und deckt weiterhin alle 10 Kompetenzbereiche ab."
    )
    c_full, c_short = st.columns(2)
    with c_full:
        if st.button("Vollversion · 22 Situationen", type="primary", use_container_width=True):
            st.session_state.test_mode = "full"
            st.session_state.page = 0
            st.session_state.answers = {}
            st.session_state.show_results = False
            st.rerun()
    with c_short:
        if st.button("Kurzversion · 11 Situationen", use_container_width=True):
            st.session_state.test_mode = "short"
            st.session_state.page = 0
            st.session_state.answers = {}
            st.session_state.show_results = False
            st.rerun()

    st.info(
        "Die Kurzversion ist eine didaktische Ableitung dieser App und wurde nicht als eigene Testform validiert. "
        "Der Kompetenzlevel wird deshalb aus dem Kurzscore linear auf die 0–86-Skala der Vollversion interpoliert."
    )
    st.stop()

ACTIVE_ITEMS = get_active_items(items)
ACTIVE_ITEM_IDS = {item[0] for item in ACTIVE_ITEMS}

# ===== Wizard / abschnittsweise Bearbeitung =====

SECTION_SPECS = [
    ("Recherche vorbereiten", "Grundlagen der Suchstrategie", {"pp01_s1_f1","pp02_s1_f1","pp03_s1_f2","pp04_s1_f2","pp05_s1_f3"}),
    ("Suchbegriffe & Evidenz", "Begriffe, Literaturarten und Evidenz auswählen", {"pp06_s1_f3","pp07_s1_f4","pp08_s1_f4","pp09_s1_f5","pp10_s1_f5"}),
    ("Suchwerkzeuge", "Geeignete Recherchewerkzeuge auswählen", {"pp11_s1_f6","pp12_s1_f6","pp13_s1_f6"}),
    ("Datenbanklogik", "Boolesche Logik, Thesaurus und Suchfelder", {"pp14_s2_f1","pp15_s2_f1","pp16_s2_f2","pp17_s2_f2","pp18_s2_f3","pp19_s2_f3"}),
    ("Zugang & Beschaffung", "Publikationen identifizieren und beschaffen", {"pp20_s2_f4","pp21_s2_f4","pp22_s2_f4"}),
]

# Pro Abschnitt die Indizes aus ACTIVE_ITEMS bestimmen; leere Abschnitte entfallen.
SECTIONS = []
for name, subtitle, ids in SECTION_SPECS:
    indices = [i for i, item in enumerate(ACTIVE_ITEMS) if item[0] in ids]
    if indices:
        SECTIONS.append((name, subtitle, indices))

if "page" not in st.session_state:
    st.session_state.page = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "show_results" not in st.session_state:
    st.session_state.show_results = False

def save_answer(item_id: str, label: str, widget_key: str):
    """Sichert Antworten unabhängig vom Lebenszyklus des sichtbaren Streamlit-Widgets."""
    st.session_state.answers.setdefault(item_id, {})[label] = st.session_state.get(widget_key)
    st.session_state.show_results = False

def item_complete(item_id: str) -> bool:
    r = st.session_state.answers.get(item_id, {})
    return all(r.get(label) is not None for label in ("A", "B", "C", "D"))

def section_complete(indices: list[int]) -> bool:
    return all(item_complete(ACTIVE_ITEMS[i][0]) for i in indices)

def go_prev():
    st.session_state.page = max(0, st.session_state.page - 1)
    st.session_state.show_results = False

def go_next():
    st.session_state.page = min(len(SECTIONS) - 1, st.session_state.page + 1)
    st.session_state.show_results = False

def restart_test():
    st.session_state.page = 0
    st.session_state.answers = {}
    st.session_state.show_results = False
    st.session_state.test_mode = None
    # Sichtbare Radiobutton-Zustände entfernen; persistente Antworten liegen separat.
    for key in list(st.session_state.keys()):
        if key.startswith("widget_"):
            del st.session_state[key]

# Neustartmöglichkeit in der Sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("Test neu starten", use_container_width=True):
        restart_test()
        st.rerun()

page = st.session_state.page
section_title, section_subtitle, section_indices = SECTIONS[page]

# Globaler Fortschritt über die 22 Situationen / 88 Einzelurteile
total_judgments = len(ACTIVE_ITEMS) * 4
answered_judgments = sum(
    1
    for item_answers in st.session_state.answers.values()
    for label in ("A", "B", "C", "D")
    if item_answers.get(label) is not None
)
completed_items = sum(1 for item_id, _, _ in ACTIVE_ITEMS if item_complete(item_id))
progress_value = answered_judgments / total_judgments if total_judgments else 0.0

st.markdown("---")
st.progress(progress_value)
st.caption(
    f"Fortschritt: **{completed_items} von {len(ACTIVE_ITEMS)} Situationen** vollständig "
    f"· {answered_judgments} von {total_judgments} Bewertungen"
)

# Kompakte Abschnittsnavigation
step_cols = st.columns(len(SECTIONS))
for i, (name, _, _) in enumerate(SECTIONS):
    with step_cols[i]:
        if i < page:
            st.markdown(f"**✓ {i+1}. {name}**")
        elif i == page:
            st.markdown(f"**→ {i+1}. {name}**")
        else:
            st.markdown(f"{i+1}. {name}")

st.subheader(f"Abschnitt {page + 1} von {len(SECTIONS)}: {section_title}")
st.caption(section_subtitle)

# Nur die Items des aktuellen Abschnitts anzeigen
responses: dict[str, dict[str, int | None]] = st.session_state.answers

def render_choice(item_id: str, choice_idx: int, choice_text: str):
    label = chr(65 + choice_idx)
    saved_value = st.session_state.answers.get(item_id, {}).get(label)
    widget_key = f"widget_{item_id}_{label}"
    default_index = [1, 2, 3, 4, 5].index(saved_value) if saved_value in [1, 2, 3, 4, 5] else None

    st.markdown(f"**{choice_text}**")
    st.radio(
        label=f"{item_id}_{label}",
        options=[1, 2, 3, 4, 5],
        index=default_index,
        horizontal=True,
        label_visibility="collapsed",
        key=widget_key,
        on_change=save_answer,
        args=(item_id, label, widget_key),
    )
    st.markdown(SCALE_HINT_HTML, unsafe_allow_html=True)
    st.markdown("<div style='height:0.35rem'></div>", unsafe_allow_html=True)

for idx in section_indices:
    item_id, title, choices = ACTIVE_ITEMS[idx]
    with st.expander(title, expanded=(layout_mode == "Untereinander")):
        if item_id in ITEM_INTROS:
            st.markdown(ITEM_INTROS[item_id])

        if layout_mode == "Kompakt (2 Spalten)":
            cols = st.columns(2)
            with cols[0]:
                render_choice(item_id, 0, choices[0])
                render_choice(item_id, 1, choices[1])
            with cols[1]:
                render_choice(item_id, 2, choices[2])
                render_choice(item_id, 3, choices[3])
        else:
            for choice_idx in range(4):
                render_choice(item_id, choice_idx, choices[choice_idx])

# Nach dem Rendern erneut prüfen (wichtig nach Antwortänderungen)
current_complete = section_complete(section_indices)
section_done = sum(1 for i in section_indices if item_complete(ACTIVE_ITEMS[i][0]))

if current_complete and page < len(SECTIONS) - 1:
    st.success(
        f"Abschnitt abgeschlossen: {len(section_indices)} von {len(section_indices)} Situationen bearbeitet. "
        "Du kannst mit dem nächsten Abschnitt fortfahren."
    )
elif not current_complete:
    st.caption(
        f"In diesem Abschnitt sind {section_done} von {len(section_indices)} Situationen vollständig. "
        "Der Weiter-Button wird aktiv, sobald alle Bewertungen gesetzt sind."
    )
else:
    st.success("Letzter Abschnitt vollständig bearbeitet. Die Auswertung ist jetzt verfügbar.")

# Vor / Weiter
nav_left, nav_mid, nav_right = st.columns([1, 2, 1])

with nav_left:
    if page > 0:
        st.button("← Zurück", on_click=go_prev, use_container_width=True)

with nav_mid:
    st.caption(
        "Deine bisherigen Antworten bleiben beim Wechsel zwischen den Abschnitten in dieser Sitzung erhalten."
    )

with nav_right:
    if page < len(SECTIONS) - 1:
        st.button(
            "Weiter →",
            on_click=go_next,
            disabled=not current_complete,
            type="primary",
            use_container_width=True,
        )

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




# ===== Referenzwerte und didaktische Einordnung =====
# Rosman, Mayer & Krampen (Validierungsstudie):
# Studierende: M = 53.06, SD = 9.82, N = 81
# Expertenstichprobe: M = 71.42, SD = 7.27, N = 14
# Diese Werte sind Forschungsstichproben, keine Normstichproben.
STUDENT_M = 53.06
STUDENT_SD = 9.82
EXPERT_M = 71.42
EXPERT_SD = 7.27

ITEM_MAX = {
    "pp01_s1_f1": 4, "pp02_s1_f1": 3,
    "pp03_s1_f2": 3, "pp04_s1_f2": 3,
    "pp05_s1_f3": 3, "pp06_s1_f3": 3,
    "pp07_s1_f4": 5, "pp08_s1_f4": 4,
    "pp09_s1_f5": 5, "pp10_s1_f5": 4,
    "pp11_s1_f6": 4, "pp12_s1_f6": 4, "pp13_s1_f6": 5,
    "pp14_s2_f1": 4, "pp15_s2_f1": 5,
    "pp16_s2_f2": 4, "pp17_s2_f2": 4,
    "pp18_s2_f3": 3, "pp19_s2_f3": 5,
    "pp20_s2_f4": 4, "pp21_s2_f4": 4, "pp22_s2_f4": 3
}

SKILL_LABELS = {
    "s1_f1": "Planung der Recherche",
    "s1_f2": "Pearl Growing / Ausgangsartikel nutzen",
    "s1_f3": "Suchbegriffe extrahieren",
    "s1_f4": "Suchbegriffe umformulieren/erweitern",
    "s1_f5": "Publikationstypen auswählen",
    "s1_f6": "Suchwerkzeuge auswählen",
    "s2_f1": "Boolesche Operatoren",
    "s2_f2": "Thesaurus / kontrolliertes Vokabular",
    "s2_f3": "Limiter / Suchfelder einsetzen",
    "s2_f4": "Volltexte beschaffen"
}

def short_equivalent_full_score(short_score: int, short_max: int) -> float:
    """
    Lineare Interpolation auf die 0–86-Skala der Vollversion.
    Dies ist nur eine didaktische Näherung, keine empirische Testverkürzung/Equating-Lösung.
    """
    if short_max <= 0:
        return 0.0
    return (short_score / short_max) * 86.0

def item_skill(item_id: str) -> str:
    # z.B. pp01_s1_f1 -> s1_f1
    return "_".join(item_id.split("_")[1:])

def classify_score(total: int) -> tuple[str, str]:
    """
    Didaktische, NICHT normativ validierte Einordnung.
    Grenzen orientieren sich an:
    - ca. 1 SD unter/über dem Mittelwert der Validierungsstichprobe
    - Expertenmittelwert als zusätzlichem Anker
    """
    if total <= 43:
        return (
            "Novizen-naher Bereich",
            "Der Wert liegt mehr als ungefähr eine Standardabweichung unter dem Mittelwert der Validierungsstichprobe."
        )
    elif total <= 62:
        return (
            "Typischer Studierendenbereich",
            "Der Wert liegt ungefähr innerhalb von ±1 Standardabweichung um den Mittelwert der Validierungsstichprobe."
        )
    elif total <= 70:
        return (
            "Fortgeschrittener Bereich",
            "Der Wert liegt deutlich über dem Mittelwert der Validierungsstichprobe, aber noch unter dem Mittelwert der Expertenstichprobe."
        )
    else:
        return (
            "Expertennaher Bereich",
            "Der Wert liegt ungefähr auf Höhe des Mittelwerts der Expertenstichprobe oder darüber."
        )

def approx_percentile(z: float) -> float:
    # Normalverteilungs-Näherung; rein deskriptiv, da keine Normtabellen publiziert wurden.
    from math import erf, sqrt
    return 100 * (0.5 * (1 + erf(z / sqrt(2))))


# ===== Didaktisches Item-Feedback (2026) =====
# Wichtig: Dieses Feedback verändert das originale Scoring NICHT.
# Es erklärt (1) die Logik des Originalitems und (2) was sich bis 2026 verändert hat.
ITEM_FEEDBACK = {
    "pp04_s1_f2": {
        "status": "Zeitkontext wichtig",
        "original": (
            "Im Original war der Artikel gerade erschienen. Deshalb war eine Vorwärts-Zitationssuche "
            "zu diesem Zeitpunkt naturgemäß noch wenig ergiebig; Rückwärtsrecherche und Schlagwortsuche "
            "waren unmittelbar nutzbarer."
        ),
        "today": (
            "Heute ist derselbe Artikel deutlich älter. Eine Vorwärts-Zitationssuche wäre inzwischen "
            "eine sehr sinnvolle Strategie. Für den PIKE-P-Score wird deshalb ausdrücklich der historische "
            "Kontext des Erscheinungsjahres beibehalten."
        ),
    },
    "pp05_s1_f3": {
        "status": "Suchsysteme haben sich verändert",
        "original": (
            "Das Item bevorzugt eine knappe, begriffsorientierte Suchanfrage gegenüber ganzen Sätzen "
            "oder zusätzlichen Funktionswörtern. Das entspricht klassischer Datenbanklogik."
        ),
        "today": (
            "In modernen Suchmaschinen, Discovery-Systemen und KI-gestützten Retrievalsystemen können "
            "auch natürlichsprachliche Anfragen gut funktionieren. Für reproduzierbare Fachdatenbankrecherchen "
            "bleibt die Zerlegung in zentrale Konzepte aber weiterhin wichtig."
        ),
    },
    "pp09_s1_f5": {
        "status": "Evidenztyp ≠ automatische Qualität",
        "original": (
            "Für den Einstieg in ein neues Themenfeld werden Überblicksarbeiten und Metaanalysen gegenüber "
            "populärpsychologischen Ratgebern und isolierten Einzelstudien bevorzugt."
        ),
        "today": (
            "Das Grundprinzip bleibt sinnvoll. Dennoch sollte man Publikationstyp und methodische Qualität trennen: "
            "Nicht jede Metaanalyse oder jedes Review ist automatisch hochwertige Evidenz."
        ),
    },
    "pp10_s1_f5": {
        "status": "Evidenzhierarchie mit Vorsicht",
        "original": (
            "Für die Begründung eines postulierten Zusammenhangs werden Synthesen mehrerer Studien höher gewichtet "
            "als einzelne Befunde oder fachfremde Statistiken."
        ),
        "today": (
            "Auch 2026 ist Evidenzsynthese zentral. Entscheidend ist jedoch, ob die zugrunde liegende Recherche, "
            "Studienqualität und Synthesemethode belastbar sind."
        ),
    },
    "pp11_s1_f6": {
        "status": "Werkzeuglandschaft gealtert",
        "original": (
            "Das Item prüft, welches Recherchewerkzeug für bibliografische Angaben zu einem psychologischen "
            "Zeitschriftenartikel besonders passend ist."
        ),
        "today": (
            "Heute liefern Google Scholar, Discovery-Systeme und Bibliothekskataloge bibliografische Angaben "
            "oft ebenfalls zuverlässig. Fachdatenbanken bleiben besonders dann wichtig, wenn strukturierte "
            "Felder, kontrolliertes Vokabular oder reproduzierbare Recherche gefragt sind."
        ),
    },
    "pp12_s1_f6": {
        "status": "DBIS funktional präzisiert",
        "original": (
            "Das Original kontrastiert verschiedene Wege, einen unbekannten Artikel eines bekannten Autors zu finden."
        ),
        "today": (
            "DBIS ist selbst keine bibliografische Autorendatenbank, sondern hilft dabei, geeignete Datenbanken "
            "zu identifizieren. Die Formulierung wurde deshalb funktional präzisiert, ohne die Antwortpositionen "
            "oder das Scoring zu verändern."
        ),
    },
    "pp13_s1_f6": {
        "status": "Google Scholar heute stärker",
        "original": (
            "Für eine komplexe fachliche Suche nach mehreren empirischen Arbeiten werden psychologische "
            "Fachdatenbanken gegenüber dem Bibliothekskatalog und Google Scholar bevorzugt."
        ),
        "today": (
            "Google Scholar ist heute für viele Themen sehr leistungsfähig. Für systematische, dokumentierbare "
            "und feldspezifisch filterbare Recherchen bieten Fachdatenbanken jedoch weiterhin methodische Vorteile."
        ),
    },
    "pp16_s2_f2": {
        "status": "Kontrolliertes Vokabular bleibt relevant",
        "original": (
            "Das Item prüft, ob Synonyme nicht nur frei ausprobiert, sondern anhand eines Thesaurus bzw. "
            "kontrollierten Vokabulars systematisch eingeordnet werden."
        ),
        "today": (
            "Dieses Prinzip bleibt aktuell. Moderne Systeme ergänzen automatische Termexpansion und semantische Suche; "
            "für transparente und reproduzierbare Strategien ist kontrolliertes Vokabular aber weiterhin wertvoll."
        ),
    },
    "pp17_s2_f2": {
        "status": "Datenbankfelder sind systemspezifisch",
        "original": (
            "Das Item prüft die Kombination von kontrollierten Schlagwörtern mit strukturierten Datenbankfeldern, "
            "um Längsschnittstudien möglichst vollständig zu identifizieren."
        ),
        "today": (
            "Konkrete Feldnamen unterscheiden sich zwischen Plattformen. Entscheidend ist heute das übergeordnete "
            "Prinzip: kontrolliertes Vokabular und verfügbare methodische Filter gezielt kombinieren."
        ),
    },
    "pp20_s2_f4": {
        "status": "Beschaffung ist heute oft Zugang statt Standort",
        "original": (
            "Das Item prüft, welche bibliografischen Angaben für die Suche nach einer Buchpublikation im Katalog "
            "besonders geeignet sind."
        ),
        "today": (
            "Heute geht es häufig nicht nur um einen physischen Standort, sondern um Bestand, Lizenz, E-Book-Zugang, "
            "Fernleihe oder andere Zugangswege. ISBN und prägnante Titeldaten bleiben trotzdem robuste Suchschlüssel."
        ),
    },
    "pp21_s2_f4": {
        "status": "Discovery-Systeme verändern die Praxis",
        "original": (
            "Das Item prüft, wie man einen Zeitschriftenartikel über bibliografische Identifikatoren und prägnante "
            "Titeldaten in einem Bibliothekssystem auffindet."
        ),
        "today": (
            "Moderne Discovery-Systeme finden einzelne Artikel häufig direkt. ISSN und Zeitschriftentitel sind "
            "weiterhin nützlich, dienen aber eher der Identifikation des Journals bzw. Zugangswegs."
        ),
    },
    "pp22_s2_f4": {
        "status": "Websuche ergänzt, ersetzt aber nicht Bibliothekszugang",
        "original": (
            "Das Item bevorzugt den gezielten bibliografischen Weg über Katalog/ISBN gegenüber einer allgemeinen Websuche."
        ),
        "today": (
            "Eine Websuche kann heute schnell zu Verlagsseiten, Open-Access-Versionen oder Google Books führen. "
            "Für verlässliche Bestands- und Zugangsprüfung bleibt der Bibliothekskatalog bzw. das Discovery-System zentral."
        ),
    },
}

# ===== Auswertung =====
if page == len(SECTIONS) - 1 and current_complete:
    if st.button("Auswertung anzeigen", type="primary", use_container_width=True):
        st.session_state.show_results = True

if page == len(SECTIONS) - 1 and st.session_state.show_results:
    responses = st.session_state.answers
    # Für den Norm-/Referenzvergleich sollte der Test vollständig bearbeitet sein.
    missing = []
    for item_id, title, _ in ACTIVE_ITEMS:
        ans = responses.get(item_id, {})
        if len(ans) < 4 or any(v is None for v in ans.values()):
            missing.append(title)

    if missing and not ALLOW_PARTIAL:
        st.warning("Bitte alle Antworten vergeben. Noch offen:\n- " + "\n- ".join(missing))
        st.stop()

    rows = []
    total = 0
    answered_items = 0

    for item_id, title, _ in ACTIVE_ITEMS:
        r = responses.get(item_id, {"A": None, "B": None, "C": None, "D": None})
        complete_item = all(v is not None for v in r.values())

        if not complete_item:
            # Bei Teilbearbeitung wird das Item NICHT künstlich mit 3 imputiert,
            # weil Gleichstände im Pairwise-Scoring Punkte erzeugen können.
            rows.append({
                "Item": title,
                "Score": None,
                "Maximum": ITEM_MAX[item_id],
                "Anteil (%)": None,
                "Kompetenzbereich": SKILL_LABELS[item_skill(item_id)]
            })
            continue

        s = score_item(item_id, r)
        max_s = ITEM_MAX[item_id]
        total += s
        answered_items += 1
        rows.append({
            "Item": title,
            "Score": s,
            "Maximum": max_s,
            "Anteil (%)": round(100 * s / max_s, 1),
            "Kompetenzbereich": SKILL_LABELS[item_skill(item_id)]
        })

    df = pd.DataFrame(rows)

    # Norm-/Referenzvergleich nur bei vollständiger Bearbeitung
    complete_test = (answered_items == len(ACTIVE_ITEMS))

    if complete_test:
        short_mode = (st.session_state.get("test_mode") == "short")
        active_max = sum(ITEM_MAX[item_id] for item_id, _, _ in ACTIVE_ITEMS)

        if short_mode:
            estimated_full = short_equivalent_full_score(total, active_max)
            pct_max = 100 * total / active_max
            z = (estimated_full - STUDENT_M) / STUDENT_SD
            perc = approx_percentile(z)
            band, band_expl = classify_score(round(estimated_full))
        else:
            estimated_full = float(total)
            pct_max = 100 * total / 86
            z = (total - STUDENT_M) / STUDENT_SD
            perc = approx_percentile(z)
            band, band_expl = classify_score(total)

        st.subheader("Ergebnis")

        c1, c2, c3, c4 = st.columns(4)
        if short_mode:
            c1.metric("Kurzscore", f"{total} / {active_max}")
            c2.metric("Interpolierter Vollscore", f"{estimated_full:.1f} / 86")
        else:
            c1.metric("PIKE-P", f"{total} / 86")
            c2.metric("Anteil Maximalpunktzahl", f"{pct_max:.1f}%")
        c3.metric("Abstand zu Studierenden-M", f"{z:+.2f} SD")
        c4.metric("ca. Perzentil", f"{perc:.0f}")

        if band == "Expertennaher Bereich":
            st.success(f"**Einordnung: {band}**")
        elif band == "Fortgeschrittener Bereich":
            st.info(f"**Einordnung: {band}**")
        elif band == "Typischer Studierendenbereich":
            st.info(f"**Einordnung: {band}**")
        else:
            st.warning(f"**Einordnung: {band}**")

        st.write(band_expl)

        if short_mode:
            st.warning(
                "Kurzversion: Der Kompetenzlevel wird aus dem Verhältnis von Kurzscore zu Kurz-Maximum "
                "linear auf die 0–86-Skala interpoliert. Das ist keine empirisch validierte Kurzform und "
                "kein psychometrisches Equating. Die Einordnung sollte deshalb nur als grobe Lernorientierung verwendet werden."
            )
            st.caption(
                f"Interpolation: {total}/{active_max} = {pct_max:.1f}% der Kurz-Maximalpunktzahl "
                f"→ geschätzter Vollscore {estimated_full:.1f}/86."
            )

        st.caption(
            "Wichtig: Diese Einordnung ist eine didaktische Orientierung und keine publizierte Normierung. "
            "Die Originalstudie berichtet Forschungsstichproben, aber keine validierten Cut-off-Werte. "
            "„Expertennah“ bedeutet daher nur: scoreseitig nahe an der Expertenstichprobe – nicht, dass damit "
            "individuelle Expertise diagnostiziert wird."
        )

        # Empirische Referenzanker
        ref_df = pd.DataFrame({
            "Referenz": [
                "Studierende – Validierungsstichprobe",
                "Studierende – Pilotstichprobe",
                "Studierende nach Informationskompetenz-Training",
                "Studierende ohne Training (Freshmen/Sophomores)",
                "Expert:innen"
            ],
            "Mittelwert": [53.06, 53.92, 60.81, 46.53, 71.42],
            "SD": [9.82, 10.41, 7.87, 9.20, 7.27]
        })
        st.markdown("#### Referenzwerte aus der PIKE-P-Studie")
        st.dataframe(ref_df, use_container_width=True, hide_index=True)

    else:
        max_answered = int(df["Maximum"][df["Score"].notna()].sum())
        st.warning(
            f"Teil-Auswertung: {answered_items} von {len(ACTIVE_ITEMS)} Items vollständig beantwortet. "
            f"Erreichte Punkte: {total} / {max_answered}. "
            "Eine Einordnung als Novize/Durchschnitt/expertennah wird erst bei vollständiger Bearbeitung angezeigt."
        )

    # Lernprofil nach den 10 Inhaltsbereichen
    skill_rows = []
    scored_df = df[df["Score"].notna()].copy()
    if not scored_df.empty:
        for skill, g in scored_df.groupby("Kompetenzbereich", sort=False):
            s = int(g["Score"].sum())
            m = int(g["Maximum"].sum())
            skill_rows.append({
                "Kompetenzbereich": skill,
                "Punkte": s,
                "Maximum": m,
                "Anteil (%)": round(100 * s / m, 1)
            })

    if skill_rows:
        st.markdown("#### Lernprofil nach Kompetenzbereichen")
        st.caption(
            "Dieses Profil dient der Lernrückmeldung. Die 10 Bereiche sind im Originaltest nur mit 2–3 Items vertreten; "
            "die Publikation weist deshalb keine separat reliabilitätsgeprüften Subskalen aus."
        )
        skill_df = pd.DataFrame(skill_rows).sort_values("Anteil (%)", ascending=False)
        st.dataframe(skill_df, use_container_width=True, hide_index=True)

    st.markdown("#### Itemübersicht")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Didaktisches Feedback zu zeitkritischen / modernisierten Items
    relevant_feedback = [
        (item_id, title, ITEM_FEEDBACK[item_id])
        for item_id, title, _ in ACTIVE_ITEMS
        if item_id in ITEM_FEEDBACK
    ]

    if relevant_feedback:
        st.markdown("#### Was bedeutet das heute?")
        st.caption(
            "Die Hinweise erklären, wo sich Recherchepraxis seit der Entwicklung des PIKE-P verändert hat. "
            "Sie verändern weder Ihre Antworten noch den originalen Pairwise-Score."
        )

        for item_id, title, fb in relevant_feedback:
            item_row = df[df["Item"] == title]
            item_score = None
            item_max = ITEM_MAX.get(item_id)
            if not item_row.empty and pd.notna(item_row.iloc[0]["Score"]):
                item_score = int(item_row.iloc[0]["Score"])

            score_suffix = (
                f" · Score: {item_score}/{item_max}"
                if item_score is not None and item_max is not None
                else ""
            )

            with st.expander(f"{title.split(')')[0]}) {fb['status']}{score_suffix}"):
                st.markdown("**Original-Logik**")
                st.write(fb["original"])
                st.markdown("**Einordnung 2026**")
                st.write(fb["today"])

    if ENABLE_CSV_EXPORT:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Ergebnisse als CSV herunterladen",
            data=csv,
            file_name=f"pike_result_{now}.csv",
            mime="text/csv"
        )

st.markdown(
    """
    <style>
    .pike-footer{
        position: fixed;
        left: 0; right: 0; bottom: 0;
        padding: 6px 10px;
        background: rgba(250,250,250,0.92);
        border-top: 1px solid #e6e6e6;
        font-size: 12px; color: #666;
        text-align: center;
        z-index: 9999;
    }
    </style>
    <div class="pike-footer">
      Dr. Robin Segerer · Universitätsbibliotheken Basel und Zürich·
      <a href="mailto:robin.segerer@unibas.ch">robin.segerer@unibas.ch</a> ·
      Version v1.7.1 · 2026-09-16
    </div>
    """,
    unsafe_allow_html=True
)
