import streamlit as st
import pandas as pd
from datetime import datetime

# 1) Konfiguration und Pakete
ENABLE_CSV_EXPORT = False  # Setze auf True, um CSV-Export zu ermöglichen
st.set_page_config(layout="wide")

# 2) Kopf + Instruktionen + Skala
st.markdown("""
<style>
.pike-box{border:1px solid #ddd;border-radius:8px;padding:14px;margin:10px 0;background:#fafafa}
.pike-kicker{font-size:14px;color:#666;margin:0}
.pike-h1{margin:.2rem 0 .6rem 0}
.pike-ul{margin:.2rem 0 .2rem 1.2rem}
.pike-scale{display:flex;gap:10px;flex-wrap:wrap;margin-top:.4rem}
.pike-pill{border:1px solid #ddd;border-radius:999px;padding:4px 10px;background:white}
</style>

<div class="pike-box">
  <p class="pike-kicker">Inoffizielle Selbstlern-Version – bitte Originalquelle (CC BY-SA 4.0) zitieren:
  Rosman, Mayer &amp; Krampen (2019), Open Test Archive (ZPID).</p>
  <h2 class="pike-h1">PIKE-P Selbstlerntest</h2>
  <div class="pike-box" style="background:#fff">
    <b>Instruktionen:</b>
    <ul class="pike-ul">
      <li>Zu jedem Item werden <b>vier Vorgehensweisen (A–D)</b> gezeigt.</li>
      <li>Bewerte <b>jede</b> der vier Vorgehensweisen auf einer Skala von <b>1 bis 5</b>
          (wie geeignet für die Aufgabe?).</li>
      <li>Klicke danach auf <b>Auswerten</b>, um deinen Gesamtscore zu erhalten.
          Optional kannst du die Tabelle als <b>CSV</b> herunterladen.</li>
    </ul>
    <div><b>Antwortskala (1–5):</b></div>
    <div class="pike-scale">
      <span class="pike-pill">1 = völlig ungeeignet</span>
      <span class="pike-pill">2 = eher ungeeignet</span>
      <span class="pike-pill">3 = teils/teils</span>
      <span class="pike-pill">4 = eher geeignet</span>
      <span class="pike-pill">5 = sehr gut geeignet</span>
    </div>
  </div>
</div>
<hr>
""", unsafe_allow_html=True)

# 3) Skala (Labels → Werte 1..5)
SCALE = [
    ('1 – völlig ungeeignet', 1),
    ('2 – eher ungeeignet', 2),
    ('3 – teils/teils', 3),
    ('4 – eher geeignet', 4),
    ('5 – sehr gut geeignet', 5)
]

# 4) Items (Volltexte: Frage + vier Optionen A–D)
items = [
    ("pp01_s1_f1", "1) In einem Vertiefungsseminar sollen Sie eine 10-seitige Hausarbeit zum Thema „Die Entwicklung des Selbstwertgefühls im Jugendalter“ schreiben. Wie beginnen Sie Ihre Vorbereitung?", ("A) Ich lese ein Einführungslehrbuch über die Entwicklung im Jugendalter, weil man diese spezifische Fragestellung nur beantworten kann, wenn man genug über die allgemeine Entwicklung weiß.", "B) Ich kläre zuerst einmal ganz genau, was man unter „Selbstwertgefühl“ versteht, und beschaffe mir dazu mehrere einführende Buchkapitel zum Thema.", "C) Ich überlege, was ich bereits zum Thema weiß und was in anderen Lehrveranstaltungen dazu behandelt wurde.", "D) Ich schreibe mir auf, welche Synonyme bzw. welche verwandten Begriffe es zu den zentralen Konzepten des Themas gibt (z.B. zu Selbstwertgefühl auch „Selbstwert“, „Selbstsicherheit“; zu Jugendalter auch „Adoleszenz“) und wie diese im Englischen lauten.")),
    ("pp02_s1_f1", "2) Die folgenden fünf Punkte beschreiben einzelne Schritte bei der Vorbereitung einer Literatursuche. Bitte geben Sie für jede der folgenden vier Abfolgen der fünf Schritte an, für wie geeignet Sie sie halten.", ("A) 2 – 5 – 4 – 1 – 3: Lesen der Aufgabenstellung – Identifikation wichtiger Konzepte – Kurze, einfache Suchen – Ermitteln von (zusätzlichen) Suchbegriffen – Verknüpfen der Suchbegriffe und Eingabe der Suchphrase in die Suchmaske", "B) 2 – 5 – 1 – 4 – 3: Lesen der Aufgabenstellung – Identifikation wichtiger Konzepte – Ermitteln von (zusätzlichen) Suchbegriffen – Kurze, einfache Suchen – Verknüpfen der Suchbegriffe und Eingabe der Suchphrase in die Suchmaske", "C) 2 – 1 – 4 – 5 – 3: Lesen der Aufgabenstellung – Ermitteln von (zusätzlichen) Suchbegriffen – Kurze, einfache Suchen – Identifikation wichtiger Konzepte – Verknüpfen der Suchbegriffe und Eingabe der Suchphrase in die Suchmaske", "D) 2 – 1 – 5 – 4 – 3: Lesen der Aufgabenstellung – Ermitteln von (zusätzlichen) Suchbegriffen – Identifikation wichtiger Konzepte – Kurze, einfache Suchen – Verknüpfen der Suchbegriffe und Eingabe der Suchphrase in die Suchmaske")),
    ("pp03_s1_f2", "3) Sie möchten ein Referat über die Intelligenzmessung bei schizophrenen Patienten vorbereiten. Der folgende, ältere Artikel liegt Ihnen vor:\n\nLidz, T., Gay, J. R., & Tietze, C. (1942). Intelligence in cerebral deficit states and schizophrenia measured by Kohs Block Test. Archives of Neurology and Psychiatry, 48(4), 568–582.\n\nWie gehen Sie vor, um weitere Artikel zu finden?", ("A) Ich extrahiere die Schlagwörter des Artikels und nutze diese als Ausgangspunkt für weitere Suchen (z. B. in einer Fachdatenbank).", "B) Ich suche nach weiteren Artikeln von diesen Autoren, da viele Autoren oft mehrere Artikel zum gleichen Thema publizieren.", "C) Ich suche in einer Fachdatenbank oder bei Google Scholar nach Artikeln, welche den Artikel zitiert haben.", "D) Ich suche im Literaturverzeichnis des Artikels.")),
    ("pp04_s1_f2", "4) Sie möchten eine Hausarbeit über den Erwerb von Ängsten schreiben. Der folgende, soeben erschienene Artikel liegt Ihnen vor:\n\nWegerer, M., Blechert, J., & Wilhelm, F. H. (2013). Emotionales Lernen: Ein naturalistisches experimentelles Paradigma zur Untersuchung von Angsterwerb und Extinktion mittels aversiver Filme. Zeitschrift für Psychiatrie, Psychologie und Psychotherapie, 61(2), 93–103.\n\nWie gehen Sie vor, um nach weiterer Literatur zu suchen?", ("A) Ich extrahiere die Schlagwörter des Artikels und nutze diese als Ausgangspunkt für weitere Suchen (z. B. in einer Fachdatenbank).", "B) Ich suche nach weiteren Artikeln von diesen Autoren, da viele Autoren oft mehrere Artikel zum gleichen Thema publizieren.", "C) Ich suche in einer Fachdatenbank oder bei Google Scholar nach Artikeln, welche den Artikel zitiert haben.", "D) Ich suche im Literaturverzeichnis des Artikels.")),
    ("pp05_s1_f3", "5) Sie bereiten eine Hausarbeit vor. Der Arbeitstitel lautet: „Der Einfluss von Lebenszufriedenheit und Selbstwirksamkeitserwartungen auf psychosomatische Beschwerden“. Wie geeignet sind folgende Suchanfragen, um nach relevanter Fachliteratur zu suchen?", ("A) Einfluss Lebenszufriedenheit Selbstwirksamkeitserwartungen „psychosomatische Beschwerden“", "B) Lebenszufriedenheit Selbstwirksamkeitserwartungen „psychosomatische Beschwerden“", "C) Einfluss Lebenszufriedenheit Selbstwirksamkeitserwartungen auf psychosomatische Beschwerden", "D) Der Einfluss von Lebenszufriedenheit und Selbstwirksamkeitserwartungen auf psychosomatische Beschwerden")),
    ("pp06_s1_f3", "6) Sie bereiten ein Kurzreferat für ein Seminar vor. Der Arbeitstitel lautet: „Wirksamkeit der Therapietechnik ‚Flooding‘ bei Spinnenphobie“. Wie gut eignen sich folgende Suchbegriffe für die notwendige Literaturrecherche?", ("A) Wirksamkeit", "B) Spinnenphobie", "C) Therapietechnik", "D) Flooding")),
    ("pp07_s1_f4", "7) Im Rahmen eines Seminars zur Motivationspsychologie bereiten Sie eine Hausarbeit vor. Der Arbeitstitel lautet: „Willenstendenzen im Rubikonmodell der Handlungsphasen“. Eine Suche mit den Suchbegriffen „Willenstendenzen“ und „Rubikonmodell der Handlungsphasen“ hat bei Google Scholar lediglich einen Treffer erbracht. Wie beurteilen Sie die folgenden Änderungen der Suchanfrage? (Anm.: Die Suchbegriffe werden mit UND verknüpft.)", ("A) „Motivation“ „Wunsch“ „Volition“ „Wille“ „Rubikonmodell“", "B) „Rubikonmodell“ „Volition“", "C) „Rubikonmodell“ „Wille“", "D) „Handlungsphasen“ „Modell“ „Wille“")),
    ("pp08_s1_f4", "8) Im Rahmen eines Seminars zur Lernpsychologie bereiten Sie ein Referat vor. Der Arbeitstitel lautet: „Befunde zur Wirksamkeit von Belohnung und Bestrafung bei Kleinkindern“. Eine Suche mit den Suchbegriffen „Wirksamkeit“, „Belohnung“, „Bestrafung“ und „Kleinkinder“ ergab viele irrelevante Ergebnisse. Wie beurteilen Sie die folgenden Möglichkeiten, Ihre Suche abzuändern? (Anm.: Die Suchbegriffe werden mit UND verknüpft.)", ("A) „operante Konditionierung“ Kleinkinder", "B) „empirische Befunde“ Wirksamkeit Belohnung Bestrafung Kleinkinder", "C) Konditionierung Kleinkinder Verstärkung", "D) „klassische Konditionierung“ Kleinkinder")),
    ("pp09_s1_f5", "9) Sie planen eine Bachelorarbeit im Bereich der arbeitsbezogenen Stressforschung. Für wie geeignet halten Sie die folgenden Literaturarten, um sich in das für Sie neue Themengebiet einzuarbeiten?", ("A) empirische Arbeiten zu unterschiedlichen Aspekten des berufsbezogenen Stresserlebens", "B) populärpsychologische Ratgeber zu arbeitsbezogenem Stress", "C) Review-Artikel zur arbeitsbezogenen Stressforschung", "D) Metaanalysen zur arbeitsbezogenen Stressforschung")),
    ("pp10_s1_f5", "10) Nachdem Sie sich in das Themengebiet der arbeitsbezogenen Stressforschung eingearbeitet haben, postulieren Sie einen positiven Zusammenhang zwischen Zeitdruck und Burnout: Menschen, die häufig unter Zeitdruck stehen, sind anfälliger für Burnout. Für wie geeignet halten Sie folgende Arten von Literatur, um möglichst überzeugend zu begründen, warum ein solcher Zusammenhang anzunehmen ist?", ("A) Review-Artikel zum Zusammenhang zwischen Zeitdruck und Burnout", "B) Einzelne empirische Arbeiten zum Zusammenhang zwischen Zeitdruck und Burnout", "C) Metaanalysen zum Zusammenhang zwischen Zeitdruck und Burnout", "D) Veröffentlichungen eines statistischen Dienstes (z. B. statistisches Bundesamt)")),
    ("pp11_s1_f6", "11) Ihr Dozent hat Ihnen den Zeitschriftenartikel „Human agency in social cognitive theory“ von Albert Bandura (einem kanadischen Wissenschaftler) empfohlen. Wie geeignet sind folgende Hilfsmittel, um herauszufinden, in welcher Zeitschrift der Artikel erschienen ist?", ("A) Fachdatenbank PsycINFO", "B) Fachdatenbank PSYNDEX", "C) Bibliothekskatalog", "D) Google Scholar")),
    ("pp12_s1_f6", "12) Sie suchen einen bestimmten Zeitschriftenartikel des Autors Richard S. Lazarus, können sich aber nicht mehr an den genauen Titel erinnern. Wie geeignet sind folgende Hilfsmittel, um den Artikel ausfindig zu machen?", ("A) Autorensuche des Datenbank-Infosystems (DBIS)", "B) Autorensuche von Google Scholar", "C) Autorensuche des Bibliothekskatalogs", "D) Autorensuche von PsycINFO")),
    ("pp13_s1_f6", "13) Im Rahmen Ihrer Bachelorarbeit benötigen Sie mehrere empirische Arbeiten zu Lernstrategien („Learning Strategies“) von Schulkindern im Alter von 6 bis 12 Jahren. Wie geeignet sind folgende Hilfsmittel, um die Arbeiten ausfindig zu machen?", ("A) Bibliothekskatalog", "B) Fachdatenbank PsycINFO", "C) Google Scholar", "D) Fachdatenbank PSYNDEX")),
    ("pp14_s2_f1", "14) Sie suchen eine Studie, welche die Effekte von medikamentöser Therapie („Drug Therapy“) und Psychotherapie („Psychotherapy“) bei Kindern mit ADS („Attention Deficit Disorder“) miteinander vergleicht. Wie gut eignen sich hierfür die folgenden Verknüpfungen von Suchbegriffen in einer Fachdatenbank?", ("A) \"Attention Deficit Disorder\" UND \"Drug Therapy\" ODER \"Psychotherapy\"", "B) \"Attention Deficit Disorder\" UND \"Drug Therapy\" UND \"Psychotherapy\"", "C) \"Drug Therapy\" ODER \"Psychotherapy\" BEI \"Attention Deficit Disorder\"", "D) \"Attention Deficit Disorder\" UND \"Drug Therapy\" NICHT \"Psychotherapy\"")),
    ("pp15_s2_f1", "15) Sie suchen eine Studie zur Diagnostik von Hochbegabung bei Kindern. Wie gut eignen sich hierfür die folgenden Verknüpfungen von Suchbegriffen in einer Fachdatenbank?", ("A) „Diagnostik“ ODER „Hochbegabung“ ODER „Kinder“", "B) „Diagnostik“ UND „Hochbegabung“ UND „Kinder“", "C) „Diagnostik“ UND „Hochbegabung“ NICHT „Jugendliche“ NICHT „Erwachsene“", "D) „Diagnostik“ UND „Hochbegabung“ ODER „Kinder“")),
    ("pp16_s2_f2", "16) In Ihrer Bachelorarbeit möchten Sie das Thema „Zeitdruck am Arbeitsplatz“ behandeln. Schnell stellt sich heraus, dass es in der englischen Fachliteratur keine einheitliche Terminologie gibt: Für „Zeitdruck“ werden sowohl die Begriffe „Work Load“ als auch „Time Pressure“ und „Work Pressure“ verwendet. Wie geeignet sind die folgenden Vorgehensweisen für die Literatursuche in einer Fachdatenbank?", ("A) Ich führe drei Suchen nach den Begriffen „Work Load“, „Time Pressure“ und „Work Pressure“ aus und verknüpfe diese miteinander.", "B) Ich finde zunächst anhand eines Fachwörterbuchs heraus, welcher der drei Begriffe am verbreitetsten ist und daher vermutlich in der Fachdatenbank als Schlagwort verwendet wird.", "C) Ich führe eine einfache Suche nach einem der drei englischen Begriffe durch, da alle verwandten Begriffe automatisch in die Suche einbezogen werden.", "D) Ich überprüfe innerhalb des Thesaurus der Fachdatenbank, mit welchen Schlagworten die Begriffe verknüpft sind.")),
    ("pp17_s2_f2", "17) Sie suchen in einer Fachdatenbank nach Längsschnittstudien („longitudinal study“) zur Wirksamkeit der kognitiven Verhaltenstherapie („cognitive behavior therapy“). Wie gehen Sie vor, um möglichst wenige Studien zu übersehen?", ("A) Ich führe zwei Suchen nach den Schlagworten (Thesaurusbegriffen) „cognitive behavior therapy“ und „longitudinal studies“ und verknüpfe diese Suchen mit UND.", "B) Ich gebe „cognitive behavior therapy longitudinal“ in die Suchmaske ein.", "C) Ich suche nach dem Schlagwort (Thesaurusbegriff) „cognitive behavior therapy“ und im Datenbankfeld, das die Information über die Untersuchungsmethode enthält (Methodology) nach „Longitudinal Empirical Study“. Dann verknüpfe ich die beiden Suchen mit UND.", "D) Ich suche nach dem Schlagwort (Thesaurusbegriff) „longitudinal study“ und im Datenbankfeld, das die Information über den Forschungsbereich enthält (Classification Codes) nach „Cognitive Therapy“. Dann verknüpfe ich die beiden Suchen mit UND.")),
    ("pp18_s2_f3", "18) Sie suchen in einer Fachdatenbank einen bestimmten Artikel von Heinz Heckhausen aus dem Jahre 1964. Der Name des Artikels ist Ihnen leider entfallen. Wie gehen Sie vor, um den Artikel möglichst schnell zu finden?", ("A) Ich gebe „Heckhausen“ UND „1964“ in die Suchmaske ein.", "B) Ich führe eine Autorensuche nach „Heckhausen“ durch, lasse die Ergebnisse nach dem Erscheinungsjahr sortieren und durchsuche sie per Hand nach einem Artikel von 1964.", "C) Ich gebe „Heckhausen“ in das Suchfeld der Autorensuche ein und schränke meine Suche auf das Veröffentlichungsjahr 1964 ein.", "D) Ich suche nach dem Thesaurusbegriff „Erscheinungsjahr“ und trage danach „1964“ in das entsprechende Feld ein. Dann gebe ich „Heckhausen“ in das Suchfeld der Autorensuche ein und verknüpfe die beiden Suchen mit UND.")),
    ("pp19_s2_f3", "19) Sie möchten mithilfe einer Fachdatenbank herausfinden, ob es Dissertationen (Doktorarbeiten) gibt, in denen das Freiburger Persönlichkeits-Inventar in seiner revidierten Fassung (FPI-R) angewandt wurde. Wie gehen Sie vor?", ("A) Ich gebe „Freiburger Persoenlichkeits-Inventar“ UND „revidierte Fassung“ in die Suchmaske ein und schränke meine Suche im Datenbankfeld, das die Information über die Art der Veröffentlichung enthält („Publication Type“) auf „Dissertation“ ein.", "B) Ich führe eine Thesaurussuche nach „Dissertation“ durch, gebe anschließend FPI-R in die Suchmaske ein und verknüpfe die beiden Suchen mit UND.", "C) Ich gebe „Freiburger Persoenlichkeits-Inventar“ UND „Dissertation“ in die Suchmaske ein.", "D) Ich gebe „FPI-R“ in die Suchmaske ein und schränke meine Suche im Datenbankfeld, das die Information über die Art der Veröffentlichung enthält („Publication Type“), auf „Dissertation“ ein.")),
    ("pp20_s2_f4", "20) Wie geeignet sind folgende Suchanfragen, die Sie in die Suchmaske des Bibliothekskatalogs eingeben, um den Bibliotheksstandort der folgenden Publikation zu finden?\n\nMönks, F. J.; van Boxtel, H.; Roelofs, J.; Sanders, M. (1986). The identification of gifted children in secondary education and a description of their situation in Holland. In: Heller, K. A.; Feldhusen, J. F. (Hrsg.), Identifying and nurturing the gifted: An international perspective. Toronto: Hans Huber. ISBN 0-920887-11-2 (auch: ISBN 3-456-81523-9).", ("A) 0-920887-11-2 (die ISBN-Nummer, welche Sie zunächst recherchiert haben)", "B) Mönks The identification of gifted children in secondary education", "C) Vollständiges Zitat (wie angegeben)", "D) Heller Identifying and nurturing the gifted")),
    ("pp21_s2_f4", "21) Wie geeignet sind folgende Suchanfragen, die Sie in die Suchmaske des Bibliothekskatalogs eingeben, um den Bibliotheksstandort der Publikation Schachter, S., & Singer, J. E. (1962) zu finden?", ("A) Psychological Review", "B) Schachter, S., & Singer, J. E. (1962). Cognitive, social, and physiological determinants of emotional state. Psychological Review, 69(5), 379–399.", "C) 0033-295X (die ISSN-Nummer, welche Sie zunächst recherchiert haben)", "D) Schachter Cognitive social and physiological determinants of emotional state")),
    ("pp22_s2_f4", "22) Sie benötigen das folgende Buch: „Richard S. Lazarus - Stress, Appraisal, and Coping“. Wie gehen Sie vor?", ("A) Ich suche im Bibliothekskatalog nach „Lazarus Stress Appraisal Coping“.", "B) Ich suche in einer Fachdatenbank nach „Lazarus Stress Appraisal Coping“, da viele Bücher darin online verfügbar sind.", "C) Ich recherchiere die ISBN-Nummer und gebe diese in den Bibliothekskatalog ein.", "D) Ich suche in einer Internet-Suchmaschine, ob das Buch online verfügbar ist.")),
]

# 5) UI bauen: Container pro Item
responses = {}
for item_id, title, choices in items:
    with st.expander(title):
        cols = st.columns(4)
        responses[item_id] = {}
        for i, txt in enumerate(choices):
            with cols[i]:
                st.markdown(txt)
                responses[item_id][chr(65+i)] = st.slider(f"Bewertung {chr(65+i)}", 1, 5, 3)

# 6) Scoring-Logik
def score_item(item_id, r):
    s = 0
    A, B, C, D = r.get("A", 3), r.get("B", 3), r.get("C", 3), r.get("D", 3)
    if item_id == "pp01_s1_f1":
        s += (B >= A) + (C >= A) + (D >= B) + (D > A)
    elif item_id == "pp02_s1_f1":
        s += (A > C) + (A > D) + (D > C)
    elif item_id == "pp03_s1_f2":
        s += (A > D) + (B >= D) + (C >= D)
    elif item_id == "pp04_s1_f2":
        s += (A > C) + (B > C) + (D > C)
    elif item_id == "pp05_s1_f3":
        s += (B > A) + (B > C) + (B > D)
    elif item_id == "pp06_s1_f3":
        s += (B > A) + (B > C) + (D > C)
    elif item_id == "pp07_s1_f4":
        s += (B > A) + (D >= A) + (B >= C) + (B > D) + (C > A)
    elif item_id == "pp08_s1_f4":
        s += (A > B) + (A > D) + (C >= B) + (C > D)
    elif item_id == "pp09_s1_f5":
        s += (A > B) + (C >= A) + (C > B) + (D > B) + (C >= D)
    elif item_id == "pp10_s1_f5":
        s += (A > D) + (C >= B) + (B > D) + (C > D)
    elif item_id == "pp11_s1_f6":
        s += (A > B) + (A > C) + (A >= D) + (D >= C)
    elif item_id == "pp12_s1_f6":
        s += (A >= C) + (B >= C) + (D > B) + (D > C)
    elif item_id == "pp13_s1_f6":
        s += (B > A) + (C > A) + (D > A) + (B > C) + (D >= C)
    elif item_id == "pp14_s2_f1":
        s += (B > A) + (B > C) + (B > D) + (A >= C)
    elif item_id == "pp15_s2_f1":
        s += (B > A) + (C > A) + (B > C) + (B > D) + (C > D)
    elif item_id == "pp16_s2_f2":
        s += (A >= B) + (D >= A) + (D > B) + (D > C)
    elif item_id == "pp17_s2_f2":
        s += (A > B) + (C > B) + (C > D) + (A > D)
    elif item_id == "pp18_s2_f3":
        s += (C > A) + (C > B) + (C > D)
    elif item_id == "pp19_s2_f3":
        s += (A > B) + (A >= C) + (D >= A) + (D > B) + (D > C)
    elif item_id == "pp20_s2_f4":
        s += (A > B) + (A > C) + (D > B) + (D > C)
    elif item_id == "pp21_s2_f4":
        s += (A > B) + (A > D) + (C >= B) + (D >= B)
    elif item_id == "pp22_s2_f4":
        s += (A > B) + (A > D) + (C > B)
    return int(s)


# 7) Klick-Handler (Auswerten)
if st.button("Auswerten", type="primary"):
    st.subheader("Ergebnis")
    
    rows = []
    total = 0
    for item_id, title, _ in items:
        s = score_item(item_id, responses[item_id])
        total += s
        rows.append({"Item": title, "Score": s})

    df = pd.DataFrame(rows)
    pcnt = round((total / 86) * 100, 2)

    st.markdown(f"### Gesamtscore (PIKE): **{total}** / **86**")
    st.markdown(f"PIKE_PCNT: **{pcnt}%**")

    st.dataframe(df, use_container_width=True)

    # Optionaler CSV-Export
    if ENABLE_CSV_EXPORT:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"pike_result_{now}.csv"
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Ergebnisse als CSV",
            data=csv,
            file_name=fname,
            mime="text/csv",
        )
