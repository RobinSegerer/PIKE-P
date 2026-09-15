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
    <li>Klicke auf <b>Auswerten</b>, um deinen Gesamtscore zu erhalten.</li>
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
     "2) Die folgenden fünf Punkte beschreiben einzelne Schritte bei der Vorbereitung einer Literatursuche:\n"
     "1. Ermitteln von (zusätzlichen) Suchbegriffen …\n"
     "2. Lesen der Aufgabenstellung …\n"
     "3. Verknüpfen der Suchbegriffe und Eingabe der Suchphrase in die Suchmaske …\n"
     "4. Kurze, einfache Suchen …\n"
     "5. Identifikation wichtiger Konzepte …\n\n"
     "Bitte geben Sie für jede der folgenden vier Abfolgen der fünf Schritte an, für wie geeignet Sie sie halten.",
     (
        "A) Ich gehe vor nach der Reihenfolge: 2 – 5 – 4 – 1 – 3.",
        "B) Ich gehe vor nach der Reihenfolge: 2 – 5 – 1 – 4 – 3.",
        "C) Ich gehe vor nach der Reihenfolge: 2 – 1 – 4 – 5 – 3.",
        "D) Ich gehe vor nach der Reihenfolge: 2 – 1 – 5 – 4 – 3."
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
     "4) Sie möchten eine Hausarbeit über den Erwerb von Ängsten schreiben. Der folgende, soeben erschienene Artikel liegt Ihnen vor:\n\n"
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
        "A) Ich verwende die Fachdatenbank PsycINFO.",
        "B) Ich verwende die Fachdatenbank PSYNDEX.",
        "C) Ich recherchiere im Bibliothekskatalog.",
        "D) Ich recherchiere mit Google Scholar."
     )
    ),
    ("pp12_s1_f6",
     "12) Sie suchen einen Artikel von Richard S. Lazarus, kennen aber nicht mehr den genauen Titel. Wie geeignet sind die folgenden Hilfsmittel?",
     (
        "A) Ich nutze die Autorensuche im Datenbank-Infosystem (DBIS).",
        "B) Ich nutze die Autorensuche in Google Scholar.",
        "C) Ich nutze die Autorensuche im Bibliothekskatalog.",
        "D) Ich nutze die Autorensuche in PsycINFO."
     )
    ),
    ("pp13_s1_f6",
     "13) Sie benötigen mehrere empirische Arbeiten zu Lernstrategien („Learning Strategies“) von Schulkindern im Alter von 6 bis 12 Jahren. Wie geeignet sind die folgenden Hilfsmittel?",
     (
        "A) Ich suche im Bibliothekskatalog.",
        "B) Ich recherchiere in der Fachdatenbank PsycINFO.",
        "C) Ich recherchiere mit Google Scholar.",
        "D) Ich recherchiere in der Fachdatenbank PSYNDEX."
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
        "B) Ich kläre zunächst anhand eines Fachwörterbuchs, welcher der Begriffe am verbreitetsten ist und vermutlich als Schlagwort genutzt wird.",
        "C) Ich führe eine einfache Suche mit einem der drei Begriffe durch und verlasse mich darauf, dass Synonyme automatisch einbezogen werden.",
        "D) Ich prüfe im Thesaurus der Fachdatenbank, mit welchen Schlagworten die Begriffe verknüpft sind, und nutze diese gezielt."
     )
    ),
    ("pp17_s2_f2",
     "17) Sie suchen Längsschnittstudien („longitudinal study“) zur Wirksamkeit der kognitiven Verhaltenstherapie. Wie gehen Sie vor, um möglichst wenige Studien zu übersehen?",
     (
        "A) Ich starte zwei Thesaurus-Suchen nach „cognitive behavior therapy“ und „longitudinal studies“ und verknüpfe die Suchen anschließend mit UND.",
        "B) Ich gebe die freie Suchphrase „cognitive behavior therapy longitudinal“ ein.",
        "C) Ich suche nach dem Schlagwort „cognitive behavior therapy“ und kombiniere es mit dem Datenbankfeld „Methodology“ = „Longitudinal Empirical Study“ (UND-Verknüpfung).",
        "D) Ich suche nach dem Schlagwort „longitudinal study“ und kombiniere es mit dem Feld „Classification Codes“ = „Cognitive Therapy“ (UND-Verknüpfung)."
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
     "20) Wie geeignet sind folgende Suchanfragen, die Sie in die Suchmaske des Bibliothekskatalogs eingeben, um den Bibliotheksstandort der folgenden Publikation zu finden?\n\n"
     "Mönks, F. J.; van Boxtel, H.; Roelofs, J.; Sanders, M. (1986). The identification of gifted children in secondary education and a description of their situation in Holland. "
     "In: Heller, K. A.; Feldhusen, J. F. (Hrsg.), Identifying and nurturing the gifted: An international perspective. Toronto: Verlag Hans Huber. ISBN 0-920887-11-2 (auch: ISBN 3-456-81523-9).",
     (
        "A) Ich suche direkt mit der ISBN „0-920887-11-2“ im Bibliothekskatalog.",
        "B) Ich suche mit der Zeichenkette „Mönks The identification of gifted children in secondary education“.",
        "C) Ich gebe das vollständige Zitat wie oben in die Suchmaske ein.",
        "D) Ich suche mit der Zeichenkette „Heller Identifying and nurturing the gifted“."
     )
    ),
    ("pp21_s2_f4",
     "21) Wie geeignet sind folgende Suchanfragen, die Sie in die Suchmaske des Bibliothekskatalogs eingeben, um den Bibliotheksstandort der Publikation Schachter, S., & Singer, J. E. (1962) zu finden?",
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
        "A) Ich suche im Bibliothekskatalog nach der Zeichenkette „Lazarus Stress Appraisal Coping“.",
        "B) Ich suche in einer Fachdatenbank nach „Lazarus Stress Appraisal Coping“, da viele Bücher dort erfasst sind.",
        "C) Ich recherchiere die ISBN des Buches und gebe diese in den Bibliothekskatalog ein.",
        "D) Ich suche in einer Internet-Suchmaschine, ob das Buch online verfügbar ist."
     )
    ),
]

# ===== Bewertung erfassen (Radio, ohne Default; Pflichtfeld-Check möglich) =====
responses: dict[str, dict[str, int | None]] = {}

for item_id, title, choices in items:
    with st.expander(title, expanded=(layout_mode == "Untereinander")):
        if layout_mode == "Kompakt (2 Spalten)":
            cols = st.columns(2)
            for col_i in range(2):
                with cols[col_i]:
                    for row_i in range(2):
                        idx = col_i * 2 + row_i  # 0..3
                        label = chr(65 + idx)     # A..D
                        st.markdown(f"**{choices[idx]}**")
                        responses.setdefault(item_id, {})[label] = st.radio(
                            label=f"{item_id}_{label}",
                            options=[1, 2, 3, 4, 5],
                            index=None,                 # kein Default -> Pflichtfeld möglich
                            horizontal=True,
                            label_visibility="collapsed",
                            key=f"{item_id}_{label}"
                        )
                        st.markdown(SCALE_HINT_HTML, unsafe_allow_html=True)
                        st.markdown("<div style='height:0.35rem'></div>", unsafe_allow_html=True)
        else:
            for idx in range(4):
                label = chr(65 + idx)  # A..D
                st.markdown(f"**{choices[idx]}**")
                responses.setdefault(item_id, {})[label] = st.radio(
                    label=f"{item_id}_{label}",
                    options=[1, 2, 3, 4, 5],
                    index=None,
                    horizontal=True,
                    label_visibility="collapsed",
                    key=f"{item_id}_{label}"
                )
                st.markdown(SCALE_HINT_HTML, unsafe_allow_html=True)
                st.markdown("<div style='height:0.35rem'></div>", unsafe_allow_html=True)

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

# ===== Auswertung =====
if st.button("Auswerten", type="primary"):
    # Für den Norm-/Referenzvergleich sollte der Test vollständig bearbeitet sein.
    missing = []
    for item_id, title, _ in items:
        ans = responses.get(item_id, {})
        if len(ans) < 4 or any(v is None for v in ans.values()):
            missing.append(title)

    if missing and not ALLOW_PARTIAL:
        st.warning("Bitte alle Antworten vergeben. Noch offen:\n- " + "\n- ".join(missing))
        st.stop()

    rows = []
    total = 0
    answered_items = 0

    for item_id, title, _ in items:
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
    complete_test = (answered_items == len(items))

    if complete_test:
        pct_max = 100 * total / 86
        z = (total - STUDENT_M) / STUDENT_SD
        perc = approx_percentile(z)
        band, band_expl = classify_score(total)

        st.subheader("Ergebnis")

        c1, c2, c3, c4 = st.columns(4)
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
            f"Teil-Auswertung: {answered_items} von {len(items)} Items vollständig beantwortet. "
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
      Version v1.1 · 2026-09-15
    </div>
    """,
    unsafe_allow_html=True
)
