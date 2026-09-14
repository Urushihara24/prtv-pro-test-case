# 🎯 PRTV.pro — Commercial QA Project

> Paid commercial QA engagement covering release readiness across web, mobile and Android TV, including billing, integrations and data migration.

<p align="center">
  <img src="https://img.shields.io/badge/Web-Chrome_DevTools-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Chrome DevTools">
  <img src="https://img.shields.io/badge/Mobile-iOS_%2B_Android-3DDC84?style=for-the-badge&logo=android&logoColor=white" alt="Mobile">
  <img src="https://img.shields.io/badge/Android_TV-Tested-3DDC84?style=for-the-badge&logo=android&logoColor=white" alt="Android TV">
  <img src="https://img.shields.io/badge/Python-Reporting_Automation-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

| Coverage | Execution snapshot | Result |
|---|---|---|
| 18 of 20 modules across 5 environments | 228-case suite: 204 completed, 5 blocked, 19 not tested | 45 defects documented with business impact and supporting analysis |

**Start here:** [planning](PLANNING/) · [analytics](ANALYTICS/) · [test scripts](SCRIPTS/) · [key findings](#-key-findings)

## 📌 Project summary

This repository documents production QA work delivered to a real product team for a SaaS platform used to build Smart TV slideshows.

**Period:** July–August 2026  
**Role:** QA Engineer, sole tester  
**Product:** PRTV.pro, an online Smart TV slideshow builder

---

## 🎯 Project context

### What PRTV.pro is
A SaaS platform for restaurants, hotels, and retail businesses to create digital menus and information screens for Smart TV.

**Core modules:**
- Drag-and-drop slideshow editor
- POS integrations: R_Keeper, iiko, QuickResto
- Informers/widgets: VK, Telegram, RSS, weather, exchange rates
- Billing and licenses
- Android TV application
- Mobile version
- Data migration between domains

### Business goals of testing
1. **Prepare the product for release** by identifying high-impact defects.
2. **Assess mobile quality** and responsive behavior.
3. **Validate integrations** against real external systems where access was available.
4. **Validate migration** so data is not lost during transfer.

---

## 📊 Results in numbers

### Test coverage
| Metric | Value |
|---|---|
| Test cases in suite | 228 |
| Completed with Pass / Fail | 204 |
| Blocked | 5 |
| Not tested | 19 |
| Modules covered | 18 of 20, 90% |
| Environments tested | 5: Chrome, Yandex Browser, Mobile iOS, Mobile Android, TV |

### Product quality snapshot
| Status | Count | Percentage |
|---|---:|---:|
| ✅ Passed | 177 | 77.6% |
| ❌ Failed | 27 | 11.8% |
| 🚫 Blocked | 5 | 2.2% |
| ⏸️ Not Tested | 19 | 8.3% |

### Defects found
| Severity | Count | Percentage |
|---|---:|---:|
| 🔴 High | 18 | 40% |
| 🟡 Medium | 14 | 31% |
| 🟢 Low | 13 | 29% |
| 💡 IMP, improvements | 4 | — |
| **Total** | **45** | **100%** |

---

## 🔍 What was tested

### Functional testing
- ✅ Navigation and authentication: registration, login, password recovery
- ✅ Slideshow editor and content behavior
- ✅ Informers: clock, weather, exchange rates, traffic, social networks, RSS
- ✅ Billing and licenses: card, QR/SBP, renewal
- ✅ Streams and collections: schedules, overlaps, drag-and-drop
- ✅ Templates: copying, purchasing, filtering
- ✅ Data migration: `prtv.su → prtv.pro`

### Integration testing
- ✅ VK OAuth and group connection
- ✅ Google OAuth and Google Drive
- ✅ Restaurant POS integrations: R_Keeper, QuickResto, iiko
- ✅ Social integrations: VK, Telegram, Odnoklassniki
- ✅ RSS feeds such as lenta.ru

### Cross-platform testing
- ✅ Desktop: Chrome 151, Yandex Browser 26.6
- ✅ Mobile: iOS Safari, Android Chrome
- ✅ TV: TCL Smart TV, application version `prtv-2.0.102`

### Non-functional testing
- ✅ UX/UI: responsiveness, contrast, localization
- ✅ Basic security checks: XSS and SQL-injection attempts
- ✅ Performance-oriented checks: 50+ slides in one slideshow
- ✅ Browser compatibility

---

## 🐛 Key findings

### Critical blockers — High Severity

#### 1. Integrations do not work reliably
**PRD-002, PRD-003, PRD-004, PRD-039, PRD-040**
- Google OAuth does not complete successfully after the full flow.
- Restaurant menus are unavailable through R_Keeper, QuickResto, and iiko.
- Social/RSS integrations fail to return content.
- Credential validation is missing and arbitrary values can be accepted.

**Business impact:** a key feature for restaurant customers is unusable.

#### 2. Mobile version is not practically usable
**PRD-010, PRD-011, PRD-046**
- Main page is not properly responsive.
- Editor is functionally broken on mobile; widgets cannot be configured reliably.
- Text and controls overflow their containers.

**Business impact:** mobile users cannot reliably use the product.

#### 3. TV application does not launch slideshows
**PRD-008, PRD-009**
- Slideshow by ID does not open.
- Background/password-protected slideshow does not start.
- Streams do not play.

**Business impact:** the primary TV consumption scenario is broken.

#### 4. Forum is trapped in a redirect loop
**PRD-007**
- `prtv.pro → prtv.su/forum → prtv.pro → prtv.su` indefinitely.

**Business impact:** the support/community section is inaccessible.

---

## 📈 Analytics

### Defect distribution by module
```text
Integrations:     ████████████████████ 10 defects (22%)
Mobile:           ██████████████       6 defects (13%)
Editor:           ████████████         5 defects (11%)
TV:               ████████             4 defects (9%)
Billing:          ██████               3 defects (7%)
Authentication:   ████                 2 defects (4%)
Other:            ███████████████████  15 defects (34%)
```

### Working hypotheses from the observed failure patterns
These are investigation hypotheses, not claimed source-code root causes unless directly supported by evidence.

**Integration failures may be related to:**
- missing backend validation;
- OAuth-token handling;
- the absence of mocks for isolated integration testing.

**Mobile failures point toward:**
- responsive behavior not being treated as a first-class product surface;
- insufficient dedicated mobile coverage before this run;
- styles that did not adapt reliably at ≤768 px.

**TV failures may be related to:**
- API/client contract drift;
- missing automated TV regression coverage;
- irregular TV-side regression execution.

[Read the detailed analysis → ANALYTICS/root-cause-analysis.md]

---

## 🛠 Methodology

### Test design
- **Equivalence partitioning:** valid vs invalid data
- **Boundary values:** 10 MB images, 1000+ characters, 50+ slides
- **Pairwise:** widget-setting combinations
- **State Transition:** license and stream statuses

### Defect prioritization
The project used a **Severity × Priority** model:
- **High × High:** blocks a core scenario; release cannot proceed safely
- **High × Medium:** severe impact with an available workaround
- **Medium × Medium:** affects UX but does not fully block the user
- **Low × Low:** cosmetic or low-impact issues

---

## 📁 Repository structure

```text
PLANNING/          # Test strategy and planning
ANALYTICS/         # Investigation hypotheses and conclusions
SCRIPTS/           # Python reporting automation
README.md          # Project overview
```

The artifacts are intended to answer not only *what* was tested, but *why* scope and priorities were selected.

---

## 🧭 QA scope and delivered work

- [x] Test design: equivalence classes, boundaries, pairwise
- [x] Test cases with preconditions and expected results
- [x] Defect localization and reproducible bug reporting
- [x] Evidence work using screenshots, video, and DevTools
- [x] Integration testing across OAuth and REST-backed flows
- [x] Cross-platform testing across Web / Mobile / TV
- [x] Reporting automation with Python
- [x] Risk-based prioritization and business-impact reasoning
- [x] Working with incomplete requirements and broad product scope

---

## 💡 Technical and process observations

### Technical observations
1. **Integrations were the most defect-heavy area in this run.** 22% of the documented defects were related to external services; mocks and contract testing would reduce this risk.
2. **Mobile is effectively a separate product surface.** Desktop responsiveness alone is not a substitute for dedicated mobile testing.
3. **TV requires its own testing approach.** Debugging and iteration differ significantly from browser-based products.

### Process observations
1. **Earlier testing reduces rework.** Several integration defects could likely have been detected closer to implementation.
2. **Reporting automation matters.** Python scripts reduced repetitive report preparation during the engagement.
3. **Documentation prevents coverage gaps.** Structured cases helped keep a wide product surface under control.

---

## 🗺 Repository map

1. Start with **README.md** for the execution snapshot and key findings.
2. Open **PLANNING/** for scope, test strategy, and prioritization.
3. Open **ANALYTICS/** for investigation notes and pattern analysis.
4. Open **SCRIPTS/** for the reporting automation used around the project.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for reuse terms.

---

**Author:** Vsevolod  
**Date:** August 2026  
**Contact:** @urushihara24

---

## 🙏 Acknowledgements

Thanks to the PRTV.pro product team for the opportunity to perform the testing and document the engagement.

---

*This repository documents paid commercial QA work delivered against a real product.*
