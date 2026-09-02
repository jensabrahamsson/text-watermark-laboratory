# Djupgranskning: text-watermark-laboratory

**Datum:** 2026-09-02  
**Granskare:** Gemini 3.8 Flash (High)  
**Måldokument:** `gemini-granskning-260902.md`  
**Omfattning:** Arkitektur, vetenskaplig metodik, statistisk stringens, testsvit, hotmodell och forskningsresultat.  
**Instruktionskrav:** Ändra ingen kod.

---

## Innehållsförteckning
1. [Exekutiv sammanfattning](#1-exekutiv-sammanfattning)
2. [Projektets syfte och teoretisk grundval](#2-projektets-syfte-och-teoretisk-grundval)
3. [Det centrala resultatet: Tvåkorns-dikotomin](#3-det-centrala-resultatet-tvåkorns-dikotomin)
4. [Mekanistiska upptäckter och artefaktanalys](#4-mekanistiska-upptäckter-och-artefaktanalys)
5. [Protokolldisciplin och pre-registrering](#5-protokolldisciplin-och-pre-registrering)
6. [Mjukvaruarkitektur och kodgranskning](#6-mjukvaruarkitektur-och-kodgranskning)
7. [Testsvit och narrativt regressionsskydd](#7-testsvit-och-narrativt-regressionsskydd)
8. [Positionering i forskningsfältet och hotmodell](#8-positionering-i-forskningsfältet-och-hotmodell)
9. [Styrkor och identifierade risker](#9-styrkor-och-identifierade-risker)
10. [Slutsats och konkreta rekommendationer](#10-slutsats-och-konkreta-rekommendationer)

---

## 1. Exekutiv sammanfattning

`text-watermark-laboratory` är en empirisk forskningsmiljö för att undersöka statistisk textvattenmärkning med fokus på Google DeepMinds öppna referensimplementation av **SynthID-Text** (`public-deepmind-30`). 

Projektets primära frågeställning är:
> *Kan en extern granskare avgöra om text bär ett SynthID-vattenmärke utan tillgång till detektorns hemliga nycklar?*

Granskningen visar att detta är ett **exceptionellt välskött, vetenskapligt moget och metodologiskt ärligt forskningsprojekt**. Projektet utmärker sig särskilt genom:

1. **Självrättelse och intellektuell hederlighet:** När ett allvarligt metodfel upptäcktes (att trunkerade kontexter räknades upprepade gånger och därmed blåste upp öppningssignalens styrka från 10/12 / 29/48 till 9/12 / 25/48), sopades detta inte under mattan. Istället korrigerades koden, historiska siffror låstes i regressionskontroller, och gränserna för vad metoden faktiskt klarar av formulerades med ökad precision.
2. **Den fundamentala tvåkorns-insikten (Two-Grain Distinction):** Projektet visar att nyckelfri detektion är möjlig med hög precision på **populations- och promptgruppsnivå** (t.ex. 9/12 på originalfamiljerna, 36/36 på in-domain 36×4, och 99/100 på den bekräftande lock A-studien på 100 nya GPT-2-familjer). Samtidigt visar projektet att metoden på **isolerad textnivå (enstaka filer utan känd tvilling)** presterar nära slumpen (**25/48**, binomialt $p \approx 0.44$, Clopper–Pearson 95% konfidensintervall $[0.372, 0.667]$ som omfattar 0.50).
3. **Mekanistisk förklaringsmodell:** Projektet nöjer sig inte med ytliga mätvärden utan har dekonstruerat *varför* indikatorn fungerar. Det visar att signalen i huvudsak är front-loaded (koncentrerad till de första 4–16 genererade polletterna/tokens), samt att till synes höga träffsäkerheter vid överföring ofta förklaras av *occupancy artifacts* (Laplace-glättning i osedda kontexter) eller *opening-atom overlap* snarare än en djup, genomgående avkodning av vattenmärket.
4. **Programkod och testning på hög nivå:** Kodbasen upprätthåller rigorösa säkerhetsspärrar (t.ex. att `BlindModel` aldrig tar emot nycklar eller g-värden, att osedda kontexter resulterar i `ABSTAIN` istället för falska gissningar, och att regressionssviten till och med testar vetenskapliga formuleringar och tabeller mot otillbörlig textglidning).

---

## 2. Projektets syfte och teoretisk grundval

### 2.1 Hur SynthID-Text fungerar
SynthID-Text (Dathathri et al., 2024) bäddar inte in osynliga tecken, nollbreddsutrymmen eller metadata i texten. Vattenmärket implementeras som en **probabilistisk styrning av provtagningen (sampling bias)** vid genereringstillfället:

```
Språkmodellens logits
        ↓
Temperaturskalning
        ↓
Pseudo-slumpmässig tilldelning av g-värden ∈ {0, 1} via LCG och hemliga nycklar
        ↓
Turneringsurval (reweighting av top-k kandidater)
        ↓
Provtagning av nästa token
```

Vid officiell detektion med kända nycklar beräknas $g$-värdena längs textens $n$-gram ($n=5$, kontextlängd $H=4$). För omärkt text är väntevärdet $E[g] = 0.50$. För märkt text förstärks sannolikheten för $g=1$, vilket ger ett genomsnittligt $g$-värde runt 0.61–0.65 för tillräckligt långa texter.

### 2.2 Den nyckelfria indikatorns ansats
I `text-watermark-laboratory` ställs frågan från en revisors/auditors perspektiv: Vad händer om vi har tillgång till en modell med och utan vattenmärke på samma promptar (**matched twins**), men saknar de hemliga nycklarna, initialiseringsvektorn (`hash_iv`) och detektorns funktion?

Indikatorn anpassar två separata räknetabeller för nästa-token-övergångar:
- $C_M(\text{kontext}, \text{token})$ för märkta generationer.
- $C_U(\text{kontext}, \text{token})$ för omärkta generationer.

Vid utvärdering av en text beräknas en ackumulerad log-likelihood ratio (LR):
$$\text{LR}(x) = \sum_{i} \log \frac{P_M(x_i \mid x_{i-k:i-1})}{P_U(x_i \mid x_{i-k:i-1})}$$

Projektet visar att även utan nycklar lämnar turneringsurvalet ett observerbart statistiskt avtryck i övergångssannolikheterna.

---

## 3. Det centrala resultatet: Tvåkorns-dikotomin

Det vetenskapligt mest centrala och metodologiskt renaste resultatet i hela laboratoriet är distinktionen mellan två olika analysnivåer ("kornigheter" / grains):

```
                        Matchade tvillingar (märkt / omärkt)
                                        │
        ┌───────────────────────────────┴───────────────────────────────┐
        ▼                                                               ▼
1. Promptgruppsnivå (Relativ)                                    2. Isolerad filnivå (Absolut)
- Jämför genomsnittlig LR per stem                               - Skyltar LR > 0 för en enskild text
- 12-LOO hard last-4: 9/12 (10/12 vid 0.02 marginal)             - 12-LOO hard last-4: 25/48 märkt, 22/48 omärkt
- 36×4 hits (in-domain): 36/36                                   - Binomialt p ≈ 0.44 (ej skilt från slump)
- Confirmatory Lock A (100×4): 99/100                            - Clopper–Pearson 95%: [0.372, 0.667]
- Distil Lock B: 88/100, Qwen Lock B: 95/100                     - Slutsats: Ej en tillförlitlig detektor för
- Slutsats: Reell, stark populationseffekt                         enstaka isolerade texter!
```

### Varför denna distinktion är avgörande
Många författare i litteraturen frestas att aggregera grupperade resultat och presentera dem som att "vattenmärket detekteras med 99 % träffsäkerhet". Laboratoriet visar att detta är felaktigt och missvisande:
- En promptgrupp kan vinna i relativ ranking ($LR_M > LR_U$) enbart genom att den omärkta texten är *mer negativ* än den märkta, trots att ingen av de märkta filerna uppnår $LR > 0$.
- Exempel: Stemmen `garden` är en av de nio rankningsvinsterna på de ursprungliga 12 familjerna, men har **0 av 4** märkta filer med $LR > 0$.
- Omvänt: Stemmarna `station`, `office` och `ferry-queue` förlorar relativ rankning men står för **5 av de 25** sanna positiva filerna i den isolerade klassificeringen.

Laboratoriet vägrar konsekvent att kalla indikatorn en "universell isolerad detektor" och har formaliserat detta i `research/narrative.md`, `AGENTS.md` och i testsviten.

---

## 4. Mekanistiska upptäckter och artefaktanalys

Laboratoriets analys går bortom ren prestandamätning och identifierar tre avgörande mekanismer bakom hur räknetabellerna beter sig:

### 4.1 Truncated-Context Overcount (Självrättelsen)
I en tidig version av koden implementerades kontextextraktionen för de första tokenen felaktigt:
När $i < context\_len$ loopade koden över alla längder upp till $k$. Eftersom tillgängliga tokens var färre än $k$, kollapsade alla anrop till identiska trunkerade delkontexter. Resultatet var att den första tokenövergången lagrades $k$ gånger istället för 1 gång.
- Detta blåste upp promptgrupprankningen till **10/12** och isolerad träffsäkerhet till **29/48**.
- När felet rättades i `blind.py` (`_add_sequence` lagrar nu varje unik reell suffixlängd $1 \dots \min(k, \text{available})$ exakt en gång) föll resultaten till de sanna **9/12** respektive **25/48**.
- Projektets sätt att hantera detta är ett mönstergillt exempel på öppen forskningsmetodik: felet döptes, isolerades i separata loggposter, regressionsskyddades och gjordes till en del av studiens kärnberättelse.

### 4.2 Front-Loading och Opening-Atom Overlap
Var i texten finns signalen? Laboratoriet analyserade tidsfönster (`--windows 0:16, 16:32, 32:64, 64:128`):
- Fönster **0:4** och **0:16** uppnår i princip hela rankningsförmågan (**34/36** på in-domain 36×4).
- Fönster **16:32** faller mot slumpnivå (**22/36**, AUC 0.549).
- I den bekräftande studien på 100 nya familjer gav absolut fönster **0:4** **99/100**, medan **16:32** gav **87/100** (parvis McNemar $p \approx 0.00092$).
- **Orsak:** I början av en text är språkmodellen starkt begränsad av prompten. Detta medför frekventa kollisioner i $n$-grammen ("opening-atom overlap", t.ex. `'The' -> ' car'`). Senare i texten divergerar genereringarna, antalet osedda kontexter exploderar, och räknetabellerna faller tillbaka på glättning eller backoff.

### 4.3 Occupancy Artifacts vs. True Token Recall
Ett av laboratoriets mest skarpsynta fynd gäller skillnaden mellan `poshits` och `postokhits`:
- `poshits` (position-bucketed n-grams) gav en skenbart hög isolerad recall (**39/48**).
- Vid djupanalys visade det sig att Laplace-glättning ($\alpha=0.5$) på en känd kontext där nästa token *inte* setts i träningsdata gav en systematisk skevhet mot det märkta hållet ("occupancy"). Den omärkta texten hamnade oftare i helt okända kontexter där båda modellerna var nollställda.
- När man införde `postokhits` – som kräver att den observerade nästa-token faktiskt finns i träningsmängden för att ge poäng – kollapsade isolerade sanna positiva till **16/48**.
- Laboratoriet bevisade därmed matematiskt och empiriskt att isolerad recall utanför domänen begränsas strikt av träningsmängdens atom-överlapp i öppningen.

---

## 5. Protokolldisciplin och pre-registrering

Projektet tillämpar en experimentell disciplin som överträffar standarden i de flesta akademiska maskininlärningslabb:

### 5.1 Pre-registrerade protokoll (`research/PROTOCOL-*.md`)
Innan nya experiment körs skrivs och versionshanteras ett protokoll som definierar:
1. **Varför experimentet fryses nu:** Motivering och relation till tidigare faser.
2. **Primär vetenskaplig frågeställning:** Exakt definierad hypotes.
3. **Frysta metoder:** Strikt förbud mot att lägga till nya parametrar, nya scoringsmetoder eller att justera tröskelvärden efter att resultaten observerats.
4. **Hypoteser formulerade i förväg:** T.ex. `H1`, `H2`, `H3` i PROTOCOL-next, samt `H-xkey-A`, `H-xkey-iso` i PROTOCOL-isolated-xkey.
5. **Primär utvärderingsenhet:** Promptfamiljen som oberoende enhet med strikt olikhet ($>$), där oavgjort räknas som förlust/oavgjort och inte som vinst.

### 5.2 Hantering av negativa resultat
När hypoteser faller dokumenteras det utan försköning:
- I PROTOCOL-isolated-xkey: *"H-xkey-iso fails as a raw count (30/48 > 25/48)"*.
- I PROTOCOL-isolated-register: *"H-reg-A fails; does not beat one-liner 23/48 or 25/48"*.
- När ett undersökningsspår nått sin teoretiska gräns stängs det formellt med ett protokoll (t.ex. `PROTOCOL-isolated-occupancy-closed.md`, `PROTOCOL-isolated-leftover-18-closed.md`, `PROTOCOL-isolated-leftover-15-closed.md`) för att förhindra fortsatt p-hacking och överanpassning mot samma testmängd.

---

## 6. Mjukvaruarkitektur och kodgranskning

Kodbasen i `src/text_watermark_tools/` är välstrukturerad, typannoterad och präglas av tydliga ansvarsområden:

```
src/text_watermark_tools/
├── cli.py         # Huvudingång för alla CLI-kommandon (score, pair, blind, probe, etc.)
├── score.py       # Officiell referensmätning via SynthID-Text och JAX/PyTorch
├── blind.py       # Kärnlogik för nyckelfri räknetabell och tvillinganalys
├── indicator.py   # Frusna indikator-modeller och abstentionslogik
├── probe.py       # Storskalig laboratorieutvärdering och jämförelse av scorare
├── stats.py       # Egenimplementerad statistisk inferens (AUC, Clopper-Pearson, McNemar)
├── transfer.py    # Överföringslogik, hashpool, ytnivå-scorers
├── rankpath.py    # Rankpath-analys och n-gram-banor
├── atoms.py       # Dekonstruktion av n-gram-atomer och Witten-Bell-backoff
├── contrast.py    # Kontroll-experiment och instanskontrast (control-shuffled-30)
└── openings.py    # Detaljstudier av textöppningar och atomöverlapp
```

### 6.1 Kodkvalitet och styrkor i implementationen
1. **Säkerhetsinvarianter och noll-läckage:**
   I `blind.py` och `indicator.py` är dataklasserna uttryckligen designade med fälten:
   ```python
   used_keys: bool = False
   used_hash_iv: bool = False
   used_g_values: bool = False
   ```
   Dessa sätts alltid till `False` i den nyckelfria sökvägen. Koden tillåter aldrig att `detector_mean` anropas under blind utvärdering.
2. **Hantering av in-place-mutation i beroenden:**
   I `score.py` (rad 129–132) finns en viktig teknisk kommentar och skyddsåtgärd: SynthIDs `weighted_mean_score` muterar `g_values` på plats. Koden skickar därför alltid in en ny array (`jnp.asarray(...)`) för att undvika sidoeffekter.
3. **Abstentionsprincipen (Selective Classification):**
   I `indicator.py` (rad 710–720) finns en principfast hantering av osäkerhet: om en text inte innehåller några observerade kontexter eller tokens (`n_observed == 0` eller `n_used == 0`) tvingar systemet fram beslutet:
   ```python
   decision = "ABSTAIN"
   extra += " not_a_universal_detector=true"
   ```
   Detta förhindrar att en okänd text slumpmässigt stämplas som omärkt eller märkt.
4. **Fristående statistisk matematik:**
   I `stats.py` är statistiska beräkningar (såsom Clopper–Pearson konfidensintervall via bisektionsinvertering av binomialfördelningen och exakt parvis McNemar) implementerade utan tunga externa beroenden som SciPy, vilket minimerar miljörisker och maximerar portabilitet.

### 6.2 Arkitektoniska förbättringsområden
- **Filstorlek på `probe.py`:** `probe.py` har växt till nästan 6 000 rader kod (209 kB). Modulen har blivit ett "monolitiskt laboratorium" som hanterar allt från argumentparsnings-hjälpare, datauppladdning, matrisoperationer, modellering, korsvalidering, tröskelberäkningar till formatering av markdown-rapporter.
  - *Rekommendation:* Vid framtida refaktorisering bör `probe.py` delas upp i mindre, fokuserade moduler (t.ex. `probe_runner.py`, `probe_reporting.py`, `probe_evaluation.py`).

---

## 7. Testsvit och narrativt regressionsskydd

Testsviten i `tests/` omfattar 47 testfiler och hundratals tester. Granskningen har kört testsviten lokalt under sessionen, och samtliga **436 tester passerar felfritt** (på 142 sekunder).

### 7.1 Meta-testning av forskningsanspråk
Ett av de mest unika och imponerande inslagen i projektet är dess **narrativa regressionstester**:
- `test_narrative.py`
- `test_abstract.py`
- `test_threat_model.py`
- `test_protocol_*.py`

Dessa tester läser markdown-filerna i `research/` och kontrollerar via asserts att:
1. De låsta nyckeltalen (**9/12**, **25/48**, **36/36**, **99/100**) inte har ändrats.
2. Förbjudna rubriker eller sensationella slogans (som *"Why Key-Free Watermark Detection Fails"*) förkastas uttryckligen.
3. Alla hänvisningar till tidigare artefakter och hypoteser stämmer överens med loggböckerna och JSON-dumparna.
4. Ingen agent eller utvecklare råkar formulera projektet som en fullständig avhandling (`thesis/`) i förtid.

Detta tillvägagångssätt eliminerar i princip "narrative drift", vilket är ett mycket vanligt problem i iterativa AI-stödda forskningsprojekt.

---

## 8. Positionering i forskningsfältet och hotmodell

Laboratoriet definierar sin hotmodell och sina gränser med hög precision i `research/threat-model.md` och `research/related-work.md`:

| Dimension | Laboratoriets position | Vad laboratoriet INTE gör |
|---|---|---|
| **Auditor-access** | Matchade tvillingar (märkt och omärkt generation på samma prompt), färdiga textsträngar. | En ensam okänd text utan referens, svarta-lådan API-frågor till okända modeller. |
| **Nyckelstatus** | Nyckelfri (inga nycklar, ingen `hash_iv`, inga g-värden). | Nyckelrekonstruktion eller kryptoanalytisk brytning av SHA-256 / LCG. |
| **Relaterad forskning** | Befinner sig i samma sfär som **Wang et al. (2026)** (*TTP-Detect*, parad referensverifiering) och **Gloaguen et al. (2025)** (generator-egenskap). | Gör inte anspråk på att ha uppfunnit fältet "detektion utan nycklar" eller att ha motbevisat **Christ et al. (2024)** eller **Zhang et al. (2024)**. |
| **Externa modeller** | Claude-urval samlas som preliminär nollbaslinje (pre-mark corpus). | Påstår inte att Claude kan detekteras med SynthID-nycklar eller att en Claude-detektor har byggts. |

---

## 9. Styrkor och identifierade risker

### 9.1 Huvudsakliga styrkor
1. **Exceptionell vetenskaplig integritet:** Projektet uppvisar en sällsynt vilja att rapportera negativa resultat, begränsningar och felaktigheter.
2. **Klarhet i begrepp:** Den skarpa distinktionen mellan promptgrupps-ranking och isolerad filklassificering förhindrar överdrivna påståenden.
3. **Mekanistiskt djup:** Projektet nöjer sig inte med siffror utan förklarar fenomenen genom positionsfönster, atomöverlapp och glättningsartefakter.
4. **Reproducerbarhet och automatisering:** Varje experiment har ett dedikerat CLI-kommando, parametrarna sparas i JSON, och resultaten sammanfattas i konsekvent formaterade markdown-dokument.

### 9.2 Identifierade risker och utmaningar
1. **Komplexitetsackumulering i koden:** Med över 10 CLI-underkommandon, dussintals scoringsmetoder (`hits`, `poshits`, `postokhits`, `hashpool`, `rankpath`, etc.) och nära 6 000 rader i `probe.py`, finns en risk för kognitiv överbelastning vid framtida underhåll.
2. **Tolkbarhetsrisk för utomstående läsare:** Trots alla varningar finns det alltid en risk att akademiska läsare ser siffran **99/100** och felaktigt antar att detta är en färdig, robust vattenmärkesdetektor för enskilda texter. Presentationen i artiklar måste vara stenhårt disciplinerad.
3. **Beroende av specifika modellfamiljer:** Forskningen är starkast på GPT-2 och dess varianter. Även om fas B undersökte Qwen2-1.5B, är moderna LLM:er med stora ordförråd (t.ex. 150k+ tokens) mer glesa i sina $n$-gram, vilket potentiellt minskar atomöverlappet ytterligare.

---

## 10. Slutsats och konkreta rekommendationer

`text-watermark-laboratory` är ett imponerande, solitt och föredömligt forskningsarbete. Det är varken en misslyckad studie eller en överdriven sensation; det är en precis, välkontrollerad mätning av vad enkla statistiska räknetabeller kan och inte kan åstadkomma mot SynthID-Text.

### Konkreta rekommendationer:

1. **Vid framtida publicering (Workshop / Konferensartikel):**
   - **Titel och vinkel:** Fokusera på population-instance-gapet, exempelvis:  
     *“Auditing Statistical Text Watermarks Without Keys: The Population vs. Instance Gap in SynthID-Text”*.
   - **Struktur:** Placera tvåkorns-berättelsen i inledningen. Presentera 99/100 och 25/48 i samma tabell i abstract och introduktion.
   - **Jämförelse mot TTP-Detect:** Gör en direkt jämförelse mot Wang et al. (2026) på en gemensam fryst datamängd.

2. **För kodbasen (på sikt, utan att bryta befintliga lås):**
   - Dela upp `probe.py` i mindre moduler.
   - Isolera historiska experimentverktyg från den aktiva indikatorpipelinen (`indicate score` / `indicate fit`).

3. **För fortsatta experiment:**
   - Genomför en systematisk flernyckels-replikering med matchande seeds över flera generatorer för att slutgiltigt kartlägga hur oberoende olika SynthID-instanser är under samma nyckelfria indikator.

---
*Dokumentet genererat och kontrollerat mot samtliga projektinvarianter och testsviter.*
