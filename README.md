# ARTVERC 
## (AntiRetroviral Therapy guidelines VERsion Control)
ARTVERC aims at tracking down Antiretroviral Therapy (ART) guideline mismatches across governments. The goal is to learn to recognize authoritative ART guidelines and flag deviating ones in various types of publications. By doing so, outdated guidelines can be detected, flagged, and updated accordingly. ARTVERC can be an important support tool in preventing HIV from becoming drug resistant, by monitoring treatment programs at the policy-making level.

The project was pitched and developed during the DigitYser [#HIVHack Hackathon](https://hivhack.org/).

Background information on the use case can be found [here](https://docs.google.com/presentation/d/e/2PACX-1vSMyoM2RIIuoWTr8z1BFCQmWwZ2h6YLTMb-UoDrvgLlyp7z6ofKkIgNrKB2ftt4Te_7Nh_CiwthMczt/pub?start=false&loop=false&delayms=3000&slide=id.p9) 

# Problem
## Example document
The following page summarizes the contents of a guideline document: [Updated recommendations on first-line and second-line antiretroviral regimens and post-exposure prophylaxis and recommendations on early infant diagnosis of HIV: interim guidance](http://www.who.int/hiv/pub/guidelines/ARV2018update/en/):

> Update on antiretroviral regimens for treating and preventing HIV infection: Since 2016, WHO has recommended tenofovir disoproxil fumarate (TDF) + lamivudine (3TC) (or emtricitabine, FTC) + efavirenz (EFV) 600 mg as the preferred first- line antiretroviral therapy (ART) regimen for adults and adolescents. WHO recommended dolutegravir (DTG) as an alternative option to EFV for first-line ART because of the uncertainty regarding the safety and efficacy of DTG during pregnancy and among people living with HIV receiving rifampicin-based tuberculosis (TB) treatment. New WHO interim guidelines contain recommendations regarding preferred first-line regimens for adults, adolescents and children initiating ART, which now include DTG and RAL.

> Update on early infant diagnosis of HIV: In 2016, WHO recommended that HIV virological testing be used to diagnose HIV infection among infants and children younger than 18 months and that ART be started without delay while a second specimen is collected to confirm the initial positive virological test result.

## Research questions
- Can we find this information in the full document (which can be found [here](http://apps.who.int/iris/bitstream/handle/10665/273632/WHO-CDS-HIV-18.18-eng.pdf?ua=1))?
- Can we find comparable information and infer which information was first?
- Can we find this information in legal documents, originating from governments in various countries?

## Potential sub-problems
### Formatting
Pre-processing the data will be an important task, as most of the documents that we will be dealing with are avaiable in PDF-format only.
- We must be able to extract data from the PDFs.
- We must be able to extract tables and the information they contain

For example, [this PDF, page 34](http://www.who.int/hiv/pub/guidelines/kenya_art.pdf?ua=1) contains the following data:

| Generic name | Form | Dosing recommendation | Food effect |
| ------------ | ---- | --------------------- | ----------- |
| Didanosine|Enteric coated(EC): 125, 200, 250 or 400 mgBuffered tabs: 25, 50, 100, 150, 200 mg | Body weight >60: 400 mg OD (buffered or EC capsules) or 200 mg BD (Buffered tabs)Body weight < 60 kg: 250 mg OD (Buffered tabs or EC capsule) or 125 mg BD (buffered tabs) | Take 1/2 -1 hour before or 2 hours after meal. Levels decrease 55%; |
| Abacavir | 300mg tablets | 300mg BD | Take without regard to meals.Alcohol increases ABC levels to 41% |

While [Apache Tika]() extracts it as:

> Generic name Form Dosing recommendation Food effect 

> Didanosine Enteric coated(EC): 

> 125, 200, 250 or 400 

> mgBuffered tabs: 25, 

> Body weight >60: 400 mg OD

> (buffered or EC capsules) or 

> 200 mg BD (Buffered 

> Take 1/2 -1 hour before or 

> 2 hours after meal. Levels 

> decrease 55%; 

> 50, 100, 150, 200 mg tabs)Body weight < 60 kg: 

> 250 mg OD (Buffered tabs or 

> EC capsule) or 125 mg BD 

> (buffered tabs) 

> Abacavir 300mg tablets 300mg BD Take without regard to 

> meals.Alcohol increases 

> ABC levels to 41% 

### Linguistic data
Depending on the techniques that we are going to use:
- We must be able to recognize:
  - drugs (e.g. `tenofovir disoproxil fumarate (TDF)`)
  - doses (e.g. `efavirenz (EFV) 600 mg`)
  - dates (to reconstruct a timeline, e.g. `Since 2016, WHO has recommended ...`)
  - references (e.g. `Consolidated guidelines on the use of antiretroviral drugs for treating and preventing HIV infection: recommendations for a public health approach. 2nd ed. Geneva: World Health Organization; 2016 (http://www.who.int/hiv/pub/arv/arv2016/en, accessed 6 July 2018).`)
  - legal texts that contain ART guidelines
  - legal texts in languages other than English that contain ART guidelines

# Related work
## Database of national HIV and TB guidelines, 2005-2011
Apparently, the World Health Organisation aleady has a database of HIV guidelines, it can be found [here](http://www.who.int/hiv/pub/national_guidelines/en/).
- There are links for a large number of countries, including [Kenya](http://www.who.int/hiv/pub/guidelines/kenya_art.pdf?ua=1) and [Tanzania](http://www.who.int/hiv/pub/guidelines/tanzania_art.pdf?ua=1).
- 

