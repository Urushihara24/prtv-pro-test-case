# Root Cause Analysis — Defect Patterns

## 📊 Overall statistics

**Total defects:** 45  
**High:** 18, 40%  
**Medium:** 14, 31%  
**Low:** 13, 29%

---

## 🔍 Analysis by category

### 1. Integrations — 10 defects, 22%

#### Symptoms
- Google OAuth does not complete successfully, PRD-002.
- Restaurant menus are unavailable, PRD-003 / PRD-039 / PRD-040.
- Social/RSS integrations do not return content, PRD-004.
- Credential validation is missing.

#### Root causes / working hypotheses
1. **Missing backend validation**  
   API accepts arbitrary data without adequate format checks.  
   **Example:** iiko accepts `TEST123@@` as an API key.

2. **Incorrect OAuth-token handling**  
   After authorization, the token is not stored or propagated correctly.  
   **Example:** after Google OAuth, the UI still shows `+ Connect`.

3. **No integration mocks for testing**  
   Important scenarios cannot be exercised without real credentials.

#### Recommendations
- ✅ Add API-level validation using DTOs/validators.
- ✅ Implement reliable OAuth-token persistence and propagation.
- ✅ Provide safe mocks for integration testing.
- ✅ Add contract testing, for example Pact.

---

### 2. Mobile version — 6 defects, 13%

#### Symptoms
- Main page is not responsive, PRD-010.
- Editor is broken on mobile, PRD-011 / PRD-046.
- Text and buttons overflow, PRD-033 / PRD-036.

#### Root causes / process hypotheses
1. **Responsiveness was not treated as a primary delivery target.**  
   Desktop styling dominated and mobile adaptation was left late.

2. **No dedicated mobile QA coverage before this engagement.**

3. **Styles do not adapt reliably at ≤768 px.**  
   Media queries are missing or incomplete in affected areas.

#### Recommendations
- ✅ Adopt a mobile-first approach for new UI work.
- ✅ Include dedicated mobile QA coverage.
- ✅ Use responsive layout primitives such as flexbox/grid consistently.
- ✅ Test on real devices, not emulation only.

---

### 3. Editor — 5 defects, 11%

#### Symptoms
- Long text overflows, PRD-016.
- Vertical video orientation is incorrect, PRD-017.
- Drag-and-drop fails, PRD-018.
- Video-add action does not work, PRD-045.

#### Root causes / hypotheses
1. **Edge cases are not handled consistently.** Long text and large files are not fully constrained.
2. **No automated regression around the UI behavior.** Defects are discovered manually late in the cycle.
3. **Complex drag-and-drop state handling.** Hover, active, disabled, and ordering states are difficult to keep consistent.

#### Recommendations
- ✅ Add explicit edge-case validation and limits.
- ✅ Add editor E2E tests with Playwright or Cypress.
- ✅ Reduce custom drag-and-drop complexity where practical.

---

### 4. TV application — 4 defects, 9%

#### Symptoms
- Slideshow by ID does not open, PRD-008.
- Streams do not play, PRD-009.

#### Root causes / hypotheses
1. **API changes were not synchronized with the TV client.**
2. **No automated TV regression coverage.**
3. **Insufficient production/runtime monitoring for TV failures.**

#### Recommendations
- ✅ Synchronize API/client version changes.
- ✅ Add automated TV coverage where technically feasible, for example Appium-based flows.
- ✅ Add error monitoring such as Sentry or an equivalent supported solution.

---

### 5. Billing — 3 defects, 7%

#### Symptoms
- License aggregation behavior is unclear, IMP-001.
- No sorting in relevant billing surfaces, PRD-028.

#### Root causes / hypotheses
1. **Business rules are not fully formalized.** License aggregation semantics are ambiguous.
2. **User expectations were not validated through dedicated UX research.**

#### Recommendations
- ✅ Document license and renewal business rules with examples/diagrams.
- ✅ Validate expected billing presentation with product/user research.

---

## 📈 Trends

### Defect distribution by module
```text
Integrations:     ████████████████████ 22%
Mobile:           ██████████████       13%
Editor:           ████████████         11%
TV:               ████████             9%
Billing:          ██████               7%
Authentication:   ████                 4%
Other:            ███████████████████  34%
```

### Severity distribution
```text
High:   ████████████████████ 40%
Medium: ██████████████       31%
Low:    ████████████         29%
```

### Conclusions
1. **Integrations are the most defect-heavy area**, 22% of findings.
2. **Mobile requires a separate strategy**, 13% of findings with a high share of severe defects.
3. **The High-severity share is large**, 40%, which supports the release-readiness concern.

---

## 💡 Systemic process risks

### 1. Limited automation
**Problem:** approximately 95% of checks were manual.  
**Impact:** slow regression and higher risk of repeated defects.  
**Recommendation:** introduce targeted E2E automation for stable core flows.

### 2. No test execution integrated into CI/CD
**Problem:** checks are run manually rather than as part of the delivery pipeline.  
**Impact:** defects are discovered later, when fixes are more expensive.  
**Recommendation:** integrate automated checks into GitHub Actions, GitLab CI, or the team's existing CI platform.

### 3. No contract testing
**Problem:** integrations break when API assumptions change.  
**Impact:** 22% of defects are integration-related.  
**Recommendation:** add contract tests such as Pact for the highest-risk boundaries.

### 4. Mobile QA coverage gap
**Problem:** mobile behavior appears to have been validated late.  
**Impact:** 13% of findings are mobile-related with a high share of severe issues.  
**Recommendation:** add regular mobile coverage to the regression cycle.

---

## 🎯 Priority actions

### Short term — before release
1. Fix the 18 High-severity issues based on business impact.
2. Add missing validation to integrations.
3. Stabilize the mobile experience.

### Medium term — 1–3 months
1. Add targeted E2E automation.
2. Add contract testing for integrations.
3. Establish regular mobile QA coverage.

### Long term — 3–6 months
1. Integrate automated checks into CI/CD.
2. Automate a meaningful share of repeatable regression scenarios.
3. Add runtime error monitoring.

---

**Summary:** the product showed several recurring quality risks — limited automation, weak integration-contract coverage, and late mobile validation — that require process improvements in addition to individual defect fixes.