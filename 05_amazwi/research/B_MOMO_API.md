# MTN MoMo Developer API — Research for a Rewards Payout Mini App

Research date: 2026-08-31. Hackathon: 2-3 Sept 2026, South Africa.
Method: MTN's own pages fetched directly (via browser render, not just raw HTML, to get JS-rendered content) plus public community-forum threads and public GitHub gists. Every claim below is tagged with its source and type. Where MTN's own docs did not say something, this file says so explicitly instead of guessing.

Legend: **[MTN-PRIMARY]** = momodeveloper.mtn.com / momo.mtn.com / momodevelopercommunity.mtn.com. **[COMMUNITY]** = a forum thread on momodevelopercommunity.mtn.com (MTN-hosted but user-generated, not official spec). **[3P]** = third-party blog/GitHub/gist, unofficial.

---

## 1. DISBURSEMENTS ("Pay") — detail, and SOUTH AFRICA availability

### 1a. The exact URL requested: SA disbursement product page

**URL:** https://momodeveloper.mtn.com/SouthAfrica_Disbursement_productDetails
**Status:** Loads (HTTP 200), but is **NOT API documentation**. It renders as a full legal contract titled:

> "MTN MOBILE MONEY DISBURSEMENT SERVICE AGREEMENT"

Confirmed by direct browser render of the page (WebFetch's flattened HTML gave the same result independently). The document is a bulk-payment **service agreement**, not a REST API reference. Key verbatim clauses:

> "1.2.19. "Mobile Money Bulk Payment Service" or "the Services" means the online real-time payment platform that enables Customers, within the Republic of South Africa, to send Mobile Money to multiple Payees;"

> "2.1. MTN has developed a Mobile Money System and the Mobile Money Bulk Payment Service and is authorized to provide mobile money services in South Africa in conjunction with African Bank, to enable MTN Mobile Money Customers to carry out certain financial transactions using the Mobile Money App and USSD;"

> "1.2.4. "Bulk Remittance Sheet" means the sheet to be uploaded by the Customer on the Customer Portal on Microsoft Excel format which indicates the Payees and amount to be remitted to each Payee;"

The operating model described in Schedule 2 ("OPERATION OF THE SERVICES") is:

> "5. To effect Payment, the Customer shall upload its payroll file via a web link which MTN Mobile Money shall provide."
> "8. The Customer will schedule the date and time of payment and at the appointed time MTN through the MTN MOBILE MONEY System will cause the transaction to be effected in one bulk movement of Mobile Money."
> "10. The Payee account numbers listed by The Customer shall be credited with E-Money value and a report generated within two (2) hours on the status of the accounts."

**There is no mention anywhere on this page of:** REST endpoints, JSON request/response bodies, HTTP headers, OAuth/Bearer tokens, X-Reference-Id, X-Target-Environment, sandbox, error codes, or rate limits. The entire document is a B2B legal agreement for a **web-portal Excel-upload bulk payment product**, run through a commercial contract with African Bank as the banking partner, with a **3-year initial term**, formal onboarding, and a physical/legal domicilium in Randburg.

**CONCLUSION — this is the single most important finding for the team:** *The product MTN's own portal links as "South Africa Disbursement" is not a self-serve developer REST API.* It is a bulk-payroll batch product requiring a signed commercial agreement, a Customer Portal login provisioned by MTN, and processing measured in hours (2-hour status report, "by the action date"), not the instant sandbox-signup REST flow used in other MTN markets. **A hackathon team cannot self-provision this in 48 hours.**

### 1b. The REST Disbursement API that DOES exist on the generic sandbox (momodeveloper.mtn.com)

This is a separate thing from 1a — it's the standard multi-country MTN Open API product, self-serve via sandbox signup. Its existence and shape are confirmed by MTN's own products list plus multiple community/third-party sources, but **country-availability for South Africa specifically in this REST/sandbox form is NOT confirmed by any MTN page found.**

Sandbox base URL: `https://sandbox.momodeveloper.mtn.com` **[COMMUNITY / 3P — the api-documentation pages themselves render as JS shells that would not yield body text via automated fetch; endpoint paths below are corroborated across multiple independent community/gist sources rather than a single official page, so treat exact field names as "very likely correct, verify against the live Swagger/API-collections in-portal try-it-out before the pitch."]**

Confirmed product description from the sandbox portal's own Products list **[MTN-PRIMARY]** (`https://momodeveloper.mtn.com/products`):

> "Disbursements | Automatically deposit funds to multiple users
> The MoMo Disbursement API product subscription offers a range of features for businesses. Key features include bulk payouts, business-to-business payments, and customer payouts, such as salaries. This streamlined payment process enables businesses to..." (description truncated by the page's own UI)

Endpoints (as corroborated by community threads **[COMMUNITY]** and public gists **[3P]** — not independently confirmed on a single official swagger page in this session):
- `POST /disbursement/v1_0/transfer` — initiate a payout (transfer)
- `GET /disbursement/v1_0/transfer/{referenceId}` — get transfer status
- `GET /disbursement/v1_0/account/balance` — account balance (pattern mirrors Collections' `/collection/v1_0/account/balance`; not independently verified for the disbursement path in this session)
- `POST /disbursement/token/` — OAuth2 token endpoint for the Disbursement product (mirrors confirmed Collections token endpoint `POST /collection/token/`)

Request body shape for `transfer` (reconstructed from the confirmed Collections `requesttopay` shape **[3P gist, directly fetched]**, which MTN's API-description community article confirms uses the identical envelope style across products):
```json
{
  "amount": "100",
  "currency": "EUR",
  "externalId": "123456",
  "payee": {
    "partyIdType": "MSISDN",
    "partyId": "46733123453"
  },
  "payerMessage": "payout",
  "payeeNote": "reward"
}
```
Response/status-check body shape — this exact shape **was directly fetched and quoted** from an MTN community product-update page **[MTN-PRIMARY]**, `https://momodevelopercommunity.mtn.com/product-updates/momo-api-error-response-enrichment-186` (example shown for Collections but documented as the same envelope used across products):
```json
{
    "externalId": "04822b2a-0896-4612-9e9e-15ce749b7883",
    "amount": "500000000",
    "currency": "UGX",
    "payer": { "partyIdType": "MSISDN", "partyId": "25677000000" },
    "payerMessage": "test",
    "payeeNote": "test",
    "status": "FAILED",
    "reason": "INTERNAL_PROCESSING_ERROR"
}
```
That same page states verbatim: *"HTTP Codes remain unchanged"* while a `reason` field was added to give failure detail beyond the bare `status`. Confirmed `status` enum values seen across sources: `SUCCESSFUL`, `PENDING`, `FAILED`. **`REJECTED` was NOT independently confirmed in any fetched MTN page in this session — do not assume it exists as a literal status string without checking the live Swagger.**

**Async model:** `POST .../transfer` returns **202 Accepted** with no body (confirmed pattern from Collections' `requesttopay`, which the sandbox testing thread **[COMMUNITY]** shows returning 202 on success after fixing a payerMessage special-character bug). The caller must then either (a) poll `GET .../transfer/{referenceId}` or (b) receive a callback at the `providerCallbackHost` registered at API-user creation. **NOT PUBLICLY DOCUMENTED — confirm with mentors:** the exact callback payload JSON shape was not found on any fetched MTN page in this session.

**Production base URL and per-country target environment**, confirmed from a community article fetched directly **[MTN-PRIMARY-hosted, community-authored]**, `https://momodevelopercommunity.mtn.com/how-to-59/target-environment-for-production-100`:

> Production `X-Target-Environment` values by country include: mtnuganda, mtnghana, mtnivorycoast, mtnzambia, mtncameroon, mtnbenin, mtncongo, mtnswaziland, mtnguineaconakry, **mtnsouthafrica**, mtnliberia.

This confirms MTN's platform *has a slot* for `mtnsouthafrica` as a production target-environment string — i.e., South Africa exists as a country code in the multi-country Open API platform's config. It does **not** confirm that the Disbursement product is actually turned on / subscribable for that environment — the SA-specific product page (1a) suggests the actual productized SA disbursement offering is the bulk-agreement product, not this REST platform. A production disbursement transaction-status query against `https://proxy.momoapi.mtn.com/disbursement/v1_0/transfer/{id}` with `X-Target-Environment: mtnzambia` was seen failing with 400 in a live community bug report **[COMMUNITY]** (`momo-zambia-developers-27/issue-fetching-disbursement-transaction-status-425`), left unanswered — illustrating this endpoint is not rock-solid even for markets where it clearly exists.

**VERDICT for item 1:** SA disbursement via the standard sandbox-signup REST API is **NOT CONFIRMED AVAILABLE**. The one page MTN's portal itself links for "South Africa Disbursement" is a commercial bulk-payment legal agreement, not a developer API. **Ask the mentors on day one whether the SA sandbox actually exposes `disbursement/v1_0/transfer` with `X-Target-Environment: sandbox`, or whether SA disbursement is genuinely restricted to the bulk/portal product.**

---

## 2. AUTH AND CALL MECHANICS

Confirmed sandbox provisioning + auth flow, corroborated across a directly-fetched public gist **[3P]** (`gist.github.com/chaiwa-berian/...`) and a WebSearch-summarized community how-to article **[COMMUNITY]** (`creating-sandbox-momo-api-user-and-key-with-python-274`), consistent with each other:

1. **Subscribe to a product** on momodeveloper.mtn.com (e.g. Collections, Disbursements) to get a **Subscription Key** (`Ocp-Apim-Subscription-Key`) — this is a per-product, per-account API-gateway key, separate from the API user/key below. Confirmed gotcha **[COMMUNITY]**: using the *wrong product's* subscription key (e.g. Collection Widget's key) against another product's provisioning endpoint returns `401`/access denied even though the call otherwise looks correct.
2. **Create an API user**: `POST https://sandbox.momodeveloper.mtn.com/v1_0/apiuser`
   Headers: `X-Reference-Id: <UUIDv4 you generate>`, `Ocp-Apim-Subscription-Key: <key>`, `Content-Type: application/json`
   Body: `{ "providerCallbackHost": "<your callback base URL>" }`
   Response: `201 Created`, empty body. The UUID you supplied becomes the API User ID.
3. **Create an API key** for that user: `POST https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/{API_USER_ID}/apikey`
   Headers: `Ocp-Apim-Subscription-Key: <key>`. Empty body.
   Response: `201 Created`, body `{ "apiKey": "<generated key>" }`.
4. **Get an access token**: `POST https://sandbox.momodeveloper.mtn.com/collection/token/` (or the equivalent `disbursement/token/` for that product)
   Auth: `Authorization: Basic base64(API_USER_ID:API_KEY)`
   Headers: `Ocp-Apim-Subscription-Key`, `X-Target-Environment: sandbox`
   Response: `{ "access_token": "...", "token_type": "access_token", "expires_in": 3600 }` — **token lifetime is 3600 seconds (1 hour)**, per this directly-quoted example body seen twice independently.
5. **Call the product endpoint** with `Authorization: Bearer <access_token>`, `Ocp-Apim-Subscription-Key`, `X-Reference-Id: <new UUIDv4 per transaction>`, `X-Target-Environment: sandbox`, `Content-Type: application/json`.

**Required headers, consolidated:**
| Header | Used for | Notes |
|---|---|---|
| `Ocp-Apim-Subscription-Key` | every call | product-specific; missing it → `401 Access Denied` (confirmed community thread) |
| `Authorization` | provisioning (`Basic base64(user:key)`) and product calls (`Bearer <token>`) | confirmed community gotcha: forgetting the literal word `Basic` or `Bearer` prefix causes 400/401 |
| `X-Reference-Id` | idempotency / transaction identity | **must be UUID v4** — confirmed community gotcha: non-UUIDv4 values cause `400 Bad Request` |
| `X-Target-Environment` | routes to sandbox vs a specific production country | `sandbox` in sandbox; `mtnsouthafrica` is the documented production value for South Africa (see §1b) |
| `X-Callback-Url` | optional per-call override of callback destination | seen in a community bad-request thread alongside the other standard headers |
| `Content-Type` | `application/json` | — |

**X-Reference-Id idempotency semantics: NOT PUBLICLY DOCUMENTED beyond "must be a UUIDv4 you generate per transaction" — confirm with mentors** whether re-sending the same X-Reference-Id is treated as a duplicate-suppression key (idempotent retry) or as a hard collision error. No fetched MTN page stated this explicitly.

**Callback URL / webhook payload shape: NOT PUBLICLY DOCUMENTED — confirm with mentors.** MTN's own community "Understanding MoMo Open API Keys" article **[MTN-PRIMARY, directly fetched]** only says to register `providerCallbackHost` at API-user creation and to *"verify the source"* of anything hitting that endpoint rather than trust it blindly — no example callback JSON body was found on any fetched page. **Design the app to poll `GET .../transfer/{referenceId}` as the reliable path, and treat the callback as a nice-to-have** you have not seen a documented shape for.

**Polling vs callback:** both exist. Given the callback shape is undocumented in every source checked, **polling the GET status endpoint is the safer demo-day mechanism.**

---

## 3. SANDBOX — provisioning, limitations, and reserved test MSISDNs

Provisioning sequence: see §2, steps 2-4. This is genuinely self-service — a community "Understanding..." article states verbatim:

> "You are in control" and can "provision" your own user and key via API calls without MTN approval — contrasted explicitly against Production, where: "You cannot auto-generate users in Production via the API. This ensures security and KYC (Know Your Customer) compliance." **[MTN-PRIMARY community article, directly fetched]**

**Sandbox does not move real money.** Confirmed verbatim from a community answer:

> "Sandbox is a testing environment and therefore will not process real money. Therefore expect no USSD prompts when you make any API calls during your development process." — Harold Rwothomio, MoMo Dev Community **[COMMUNITY]**

**Reserved/test MSISDNs that force specific outcomes: NOT PUBLICLY DOCUMENTED IN ANY PAGE THIS SESSION COULD ACTUALLY RETRIEVE.** Multiple third-party sources (blogs, SDK READMEs) assert that MTN publishes such a list on `https://momodeveloper.mtn.com/api-documentation/testing/`, and one community answer paraphrases it as *"if you use a phone number other than test numbers from MTN's documentation, the response will always return SUCCESSFUL; to see PENDING or FAILED you need to use a test number from MTN's MoMo Documentation Website."* However, **directly fetching `https://momodeveloper.mtn.com/api-documentation/testing/` in this session returned only page chrome/navigation, no actual number list** — the content is very likely rendered client-side behind the in-portal "try it out" UI and/or requires a logged-in session. **Do not invent numbers. On day one, log into the sandbox portal yourselves and open the "Testing" tab under API documentation to get the current reserved MSISDN list before you build your demo script around forced outcomes.**

Known-good general shape of failure signals that IS confirmed (from the error-response-enrichment example, §1b): `status: "FAILED"` with `reason` values including `INTERNAL_PROCESSING_ERROR`; community threads separately reference `INSUFFICIENT_BALANCE` and a `CUSTOMER_INPUT_REJECTION/CANCEL_REQUEST`-type reason, but the exact literal reason strings were not seen verbatim in a directly-fetched page for those two — **treat as "very likely real, verify against the live docs".**

**Known sandbox limitations, confirmed:**
- Sandbox enforces a **call volume quota** and returns `403` when exceeded. Verbatim error body captured from a community thread **[COMMUNITY]**: `{ "statusCode": 403, "message": "Out of call volume quota. Quota will be replenished in 2.13:47:06." }`. **No published numeric rate limit (calls/minute or /day) was found anywhere** — only that a quota exists and replenishes after a multi-day cooldown once exhausted. This is a real demo-day risk: **do not hammer the sandbox with test loops close to the event.**
- Currency in sandbox requests must be `EUR` regardless of target market — confirmed twice independently across community threads (a `GH` currency value caused a 400).
- `payerMessage`/`payeeNote` fields reject at least the `#` special character, causing 400s (confirmed community root-cause thread) — keep these fields to plain alphanumeric text.
- Sandbox `bc-authorize` / `oauth2/token` flows exist alongside the plain `token/` flow but are poorly documented; one community thread found the `MerchantTransferWithConsent` endpoint referenced in docs but never actually reachable in sandbox, with a community member guessing *"it is live server only"* (unconfirmed by MTN staff).

---

## 4. ERROR CODES and error response format; RATE LIMITS

**Error envelope**, confirmed directly from an MTN community product-update page (quoted in full in §1b): the standard success/status-check body gets a `status` field (`SUCCESSFUL` / `PENDING` / `FAILED`) plus, since the "error response enrichment" change, a `reason` field carrying the specific failure cause, while **"HTTP Codes remain unchanged."**

**Confirmed HTTP-level error causes, each seen directly in a fetched community thread:**
- `400 Bad Request` — non-UUIDv4 `X-Reference-Id`; non-`EUR` currency in sandbox; special characters (e.g. `#`) in `payerMessage`; malformed `bc-authorize` payload.
- `401 Access Denied` — missing/incorrect `Ocp-Apim-Subscription-Key`; using the wrong product's subscription key against a different product's endpoint; expired bearer token.
- `403` — sandbox call-volume quota exhausted (`"Out of call volume quota"`, resets after a multi-day cooldown shown in the response message itself).
- Missing `Basic`/`Bearer` literal prefix on `Authorization` — causes request rejection at the gateway.

**A full canonical list of MoMo error codes (e.g. PAYER_NOT_FOUND, PAYEE_NOT_FOUND, NOT_ENOUGH_FUNDS, etc. as literal enum strings): NOT PUBLICLY DOCUMENTED IN ANY PAGE THIS SESSION COULD RETRIEVE — confirm with mentors** or pull the live Swagger `definitions` block from inside the portal's interactive docs.

**Rate limits:** no numeric published rate limit (req/sec, req/day) was found on any MTN page. Only the existence of a sandbox call-volume quota is confirmed (see §3), with no stated number.

---

## 5. THE OTHER PRODUCTS

Sources: MTN's own sandbox Products list at `https://momodeveloper.mtn.com/products` **[MTN-PRIMARY, directly fetched]** (only 4 items actually listed there as subscribable sandbox products), and MTN's marketing/business-solutions page `https://momodevelopercommunity.mtn.com/p/business_solutions` **[MTN-PRIMARY, fetched]** (9 named business-solution concepts, described at a marketing level, not necessarily self-serve sandbox products).

- **Collections / "Get Paid"** — Publicly documented: **YES** (it is one of the 4 items on the live sandbox Products page, with full request/response shapes independently corroborated across multiple sources including a directly-fetched community error-format example). South Africa availability: **UNKNOWN** — not tested in this session, and the same caution as Disbursement applies: check whether SA has a REST-sandbox Collections product or only a bank-agreement style product.

- **Invoice** — Publicly documented: **YES**, but only as a marketing-page description ("Allows businesses to create invoices that payers can settle through any channel later," from Business Solutions page) plus one incidental code snippet (`POST /collection/v2_0/invoice`) seen in a third-party adaptor doc. Not seen as a top-level item on the sandbox Products list itself. South Africa availability: **UNKNOWN**.

- **Manage** — Publicly documented: **YES** at a marketing level ("Get Balance and Check Transaction Status APIs"). Not a distinct sandbox-subscribable product in its own right — appears to describe capabilities folded into Collections/Disbursements (balance, status). South Africa availability: **UNKNOWN**.

- **Distribute** — Publicly documented: **YES** at a marketing level only ("distribute MTN and MoMo services including cash-in, cash-out, and airtime sales with commission returns"). No endpoint-level documentation found anywhere in this session. South Africa availability: **UNKNOWN**.

- **Interact (Channel as a Service)** — Publicly documented: **YES**, and in real technical detail — a full community how-to article was directly fetched (`momo-open-api-channel-as-a-service-dynamic-journey-services-djs-223`). It lets a partner "showcase and control a secondary menu on the MoMo USSD and App platforms," communicating via a REST API implemented on the partner's own side, gated by an approval workflow: partner designs an XML "Journey," submits it via the MTN Partner Portal, MTN reviews/approves or sends back for revision, then the partner publishes. This is **not a self-serve sandbox product** — it requires MTN's manual review, so it is not viable for a 48-hour hackathon build. South Africa availability: **UNKNOWN**.

- **Identify (KYC)** — Publicly documented: **YES** at a marketing level only ("obtaining Know Your Customer (KYC) information about MoMo Consumers"). No endpoint documentation found. South Africa availability: **UNKNOWN**.

- **Get Consent** — Publicly documented: **YES** at a marketing level only ("use MoMo USSD to engage clients and collect terms acceptance via MoMo PIN"). No endpoint documentation found. South Africa availability: **UNKNOWN**.

- **Notify** — Publicly documented: **YES** at a marketing level ("send personalized SMS to both MoMo consumers and businesses following successful Pay or Get Paid transactions"). No endpoint documentation found as a standalone product; the underlying SMS-on-completion behaviour is also described directly inside the SA Disbursement legal agreement (§1a) as something MTN does automatically, not something a developer calls. South Africa availability: **UNKNOWN** as a standalone API; the SMS-notify behaviour clearly exists for the SA bulk product.

- **Remittance** — Publicly documented: **YES** — it is one of the 4 items on the live sandbox Products page: *"Remittances | Remit funds to local recipients from the diaspora with ease... KYC like first name and last name with clear identifications of the sender..."* South Africa availability: **UNKNOWN**, not tested.

- **Collection Widget** — Publicly documented: **YES** — one of the 4 sandbox Products, described as: *"Collection Widget | Receive mobile money payments on your website through a USSD or QR code... enables a developer or partner to integrate a MoMoPay checkout button to accept Mobile Money payments on your e-commerce site."* Also independently confirmed via momo.mtn.com marketing copy: *"Receive and approve Mobile Money payments on your website by scanning a QR code."* South Africa availability: **UNKNOWN**.

**Summary table:**

| Product | Publicly documented | Self-serve sandbox product? | SA availability |
|---|---|---|---|
| Collections / Get Paid | Yes | Yes (on live Products list) | Unknown |
| Disbursements / Pay | Yes | Yes (on live Products list) as generic REST product; SA's own linked product page is a different bulk-agreement product | SA REST sandbox: **not confirmed**. SA bulk product: yes, but not a dev-self-serve API |
| Collection Widget | Yes | Yes (on live Products list) | Unknown |
| Remittances | Yes | Yes (on live Products list) | Unknown |
| Invoice | Yes (marketing-level) | Not confirmed as standalone sandbox item | Unknown |
| Manage | Yes (marketing-level) | No — folded into other products | Unknown |
| Distribute | Yes (marketing-level) | Not confirmed | Unknown |
| Interact / Channel-as-a-Service | Yes (detailed how-to exists) | No — requires manual Partner Portal approval workflow | Unknown |
| Identify (KYC) | Yes (marketing-level) | Not confirmed | Unknown |
| Get Consent | Yes (marketing-level) | Not confirmed | Unknown |
| Notify | Yes (marketing-level) | Not confirmed as standalone | Confirmed as automatic behaviour inside SA bulk product |

---

## 6. THE MINI APP SPEC

**Is it public or gated?** The top-level program page `https://momodevelopercommunity.mtn.com/momo-mini-app-program-64` **[MTN-PRIMARY]** shows a "LOGIN" button in its header, but **the actual technical article underneath rendered fully without needing to log in** when navigated to directly with a real browser (this contradicts a naive non-JS-rendering fetch of the same page, which reported everything as gated — the lesson: MTN's site is a JS app, so a plain HTML fetch under-reports what's actually public).

The category lists exactly two articles:
- "MoMo PWA Mini App Integration" (index/overview, at `momo-pwa-mini-app-integration-66`) — its own summary blurb, quoted verbatim:
  > "Comprehensive guidelines outlining the end-to-end integration of MoMo PWA Mini Apps, including detailed technical integration requirements, user experience and design standards, mandatory security and compliance controls, and the applicable Terms and Conditions governing participation in the MoMo ecosystem"
  This index page itself contains only that description and a link onward — the promised "design standards" and "security and compliance controls" detail was **not found rendered as visible body text** on this index page in this session (it may be a further-nested article not discovered, or gated deeper than we went — **NOT PUBLICLY DOCUMENTED IN WHAT WE COULD RETRIEVE; confirm with mentors / dig further inside the portal**).
- "MoMo PWA Integration" by community author Ddamula (`momo-pwa-mini-app-integration-66/momo-pwa-integration-465`) — **this one is a full, fully public, technical integration guide**, fetched and quoted in full below.

### Container / shell and how a mini app is loaded
The mini app runs as a **web page loaded inside a React Native WebView inside the MTN MoMo mobile app** (not literally an Ant/Alipay-branded mini-program runtime — MTN's own community docs call it a "MicroSite"). Verbatim:

> "Guidelines to Installing and testing partners PWA with the MoMo MicroSite"
> "Journey Initialization — Receiving: START_JOURNEY — Automatically sent when your microsite loads in the mobile app"

### Does the user arrive already authenticated?
**Yes.** The `START_JOURNEY` event delivers a security token and the user's phone number directly to your page:
```javascript
window.addEventListener('MoMoWebViewEvent', (payload) => {
  const { event, msisdn } = payload.detail;
  if (event === 'START_JOURNEY') {
    const token = window.micrositeToken;
    startYourApplication(token, msisdn);
  }
});
```
So your mini app receives `msisdn` (the logged-in user's phone number) and a `micrositeToken` for free at launch — no separate OAuth/login screen needed inside the mini app itself.

### Session lifetime and keep-alive (JS bridge)
Directly quoted, verbatim:
> "The micrositeToken is valid for 10 minutes."
> "If no activity (no heartbeats) occurs within 10 minutes, the session ends and the user must restart."
> "If heartbeats are continuously sent, the session continues beyond 10 minutes."
> "At 9 minutes, restart the journey to obtain a new valid token." (i.e. your app must implement its own refresh logic)
> Heartbeat event: `IS_STILL_ACTIVE`, "Keep the session alive... every 50 seconds", "Actual timeout is 60 seconds, providing a 10-second buffer," "Recommended sending interval: every 45-50 seconds." Only `IS_STILL_ACTIVE` resets the timer — other events (`AWAITING_FOR_APPROVAL`, `APPROVED`, `REJECTED`) do not.

Heartbeat code:
```javascript
function sendHeartbeat() {
  const message = { event: 'IS_STILL_ACTIVE', micrositeToken: window.micrositeToken };
  window.ReactNativeWebView.postMessage(JSON.stringify(message));
}
const heartbeatInterval = setInterval(sendHeartbeat, 50000);
```

### The JS bridge / "SDK"
There is no separate SDK package — the entire bridge is: (1) listen for the browser CustomEvent `MoMoWebViewEvent`, and (2) call `window.ReactNativeWebView.postMessage(JSON.stringify({...}))` to send events back to the host app. Documented event vocabulary, each with an exact code sample directly quoted from the page: `START_JOURNEY` (received), `IS_STILL_ACTIVE` (sent, heartbeat), `AWAITING_FOR_APPROVAL` (sent, with a `transactionId`), `APPROVED` / `REJECTED` (sent, user's approve/deny action on a transaction), `DONE` (sent, journey complete — also stops the heartbeat interval), `ERROR` (sent, with a `message` string).

### Design standards / CSP / viewport
**NOT PUBLICLY DOCUMENTED IN WHAT WE COULD RETRIEVE.** The overview page promises "user experience and design standards" and "mandatory security and compliance controls" exist somewhere in the program's material, but no page reachable in this session rendered actual CSP rules, viewport requirements, or visual design-standard specifics. **Ask the mentors directly for the design-standards document and any CSP allowlist on day one** — building against an unknown CSP is a real risk if your app tries to load external fonts/scripts/images.

### Review / approval process for a mini app
**NOT PUBLICLY DOCUMENTED for the Mini App program specifically in what we could retrieve.** By analogy, the sibling "Interact / Channel as a Service" product (§5) uses a manual Partner Portal review-and-approve workflow with revision cycles — if the Mini App program works the same way, a hackathon prototype likely will **not** go through real MTN review in 48 hours, and the demo will need to run in a simulator instead (see next point).

### Testing without a real device
The article explicitly supports this and provides a downloadable **`momo-micro-site-integration-Simulator.zip`** attachment on the page, plus a guard pattern for local browser testing:
```javascript
function sendMessage(message) {
  if (window.ReactNativeWebView) {
    window.ReactNativeWebView.postMessage(JSON.stringify(message));
  } else {
    console.log('Would send to mobile app:', message);
  }
}
```
Also confirmed verbatim restriction: "Can the microsite use device microphone APIs? No — must be implemented natively in the app" — i.e. the mini app WebView cannot access native device hardware APIs like the mic directly; anything like that has to be done by the native host app, not your page.

### Ant International / Alipay mini-program angle
This is **not** the same platform as the WebView "MicroSite" bridge documented above — it is a **separate, much bigger, still-rolling-out initiative**, confirmed only via third-party tech press, not MTN developer docs:
- MTN Group Fintech signed a partnership with **Ant International** (global arm of Ant Group / Alipay) to rebuild MoMo into a super-app using Ant's mini-program platform technology. **[3P — Ecofin Agency, TechCentral, Innovation Village, Techmoonshot, all June 2026 coverage]**
- Initial rollout is reported as **Nigeria, Q3 2026** — South Africa is not reported as part of the initial rollout in any article found.
- No MTN developer-portal page describing an Ant-style mini-program SDK/manifest/API surface was found. The "MoMo MicroSite" WebView bridge documented above (§6, PWA/React-Native-WebView) appears to be MTN's **existing, already-shipping** mechanism, separate from and likely predating the Ant International initiative. **Do not assume the Ant/Alipay mini-program tooling is what the hackathon's "Mini App" track actually runs on — confirm with mentors which of the two (existing MoMo MicroSite bridge vs. new Ant-powered mini-program platform) the hackathon environment targets.**

---

## 7. HACKATHON T&Cs — verbatim

**URL:** https://momodevelopercommunity.mtn.com/p/momo_hackathon_2026_terms_and_conditions
**Status:** Loads fully, public, no login required. Page title: "MoMo_Hackathon_2026_TnCs". Full document heading: **"MTN Group Fintech Hackathon – Terms & Conditions."**

### (a) Judging criteria — verbatim, section 5:
> "5. Judging Criteria
> Solutions will be evaluated based on:
> Innovation & Creativity
> Relevance to Fintech Challenges
> Feasibility & Scalability
> Technical Execution
> Presentation & Pitch
> The judges' decision is final and binding. See decision clause a the end of the documents." [sic — typo in the original]

### (b) Rule on pre-existing code / work created before the event — verbatim, section 3:
> "3. Hackathon Rules
> Participants will have 48 hours to ideate, build, and present a prototype/solution.
> All submissions must be original and created during the hackathon. Pre-existing projects are not allowed unless approved by organizers.
> Use of open-source libraries and APIs is permitted, provided licenses are respected.
> Teams must present their solutions within the allocated time."

**This is a hard constraint for this team:** any pre-hackathon build work you do now (research is fine — code is not, unless organizer-approved) risks disqualification unless explicitly cleared with organizers beforehand. **Get this clearance in writing on day one if any scaffolding was done before 2 Sept.**

### (c) IP / ownership clause — verbatim, section 4:
> "4. Intellectual Property (IP)
> Participants retain ownership of their ideas, code, and prototypes.
> By participating in the Hackathon, teams and individuals hereby grant MTN Group Fintech and sponsors the right to use project descriptions, demos, and media for marketing and promotional purposes.
> The participants hereby grant a royalty free, sub-licensable and exclusive license to use the project descriptions, demos and products for marketing and promotional purposes to MTN Group Fintech and the sponsors
> If participants use third-party materials, they must ensure compliance with copyright, licensing, and usage rights."

Note the internal tension worth flagging to teammates: the clause says participants "retain ownership," but the license granted over "demos and products" (not just descriptions/media) is described as **"exclusive"** for marketing/promotional purposes — an exclusive license over your own product output, even if scoped to marketing use, is unusual and worth a direct question to organizers about scope (see §9 questions).

### (d) Team size — verbatim, section 1:
> "1. Eligibility
> Open to individuals aged 18 years and above.
> Participants may enter individually or as part of a team (up to four (4) members).
> Directors, agents, employees or consultants of MTN Group, its affiliates, sponsors, and immediate family members may not be eligible.
> Proof of identity and eligibility may be required."

### Other sections captured verbatim for completeness:
> "6. Prizes — Cash prize of USD 10,000 to be distributed among 1st, 2nd and 3rd prize winners. Payable in local currency at prevailing exchange rates. 1st, 2nd and 3rd prize amounts to be determined by the organizers. Prizes are non-transferable and subject to applicable taxes. The organizers reserve the right to substitute prizes with similar value items."

> "7. Code of Conduct — ... Alcohol, drugs, and unlawful behavior are strictly prohibited. Participants may not consume, possess, distribute, or be under the influence of illegal substances at any time during the Hackathon or any official Hackathon activity."

> "8. Liability & Disclaimers — The hackathon is provided on an "as-is" basis. Organizers are not liable for: Technical failures, interruptions, or errors. Loss of data or intellectual property. Personal injury, theft, or damage to property during the event. Participants are responsible for their own equipment, expenses, and travel arrangements."

---

## 8. COMMUNITY GOTCHAS — most common integration failures

All directly sourced from momodevelopercommunity.mtn.com forum threads **[COMMUNITY]**:

1. **Non-UUIDv4 `X-Reference-Id`** → `400 Bad Request`. Fix: always generate a real UUIDv4 per transaction.
2. **Missing the literal `Basic` or `Bearer` keyword** in the `Authorization` header (e.g. sending just the base64 string, or just the token, without the scheme word) → request rejected. Two independent threads hit this exact bug.
3. **Special characters in `payerMessage`/`payeeNote`** (a `#` was the confirmed culprit) → `400 Bad Request`. Fix: keep these fields to plain text.
4. **Wrong currency in sandbox** — must be `EUR` even if your real market currency is ZAR/GHS/UGX/etc. A user sending `"GH"` as currency got 400s until switching to `EUR`.
5. **Using the wrong product's subscription key** — e.g. calling a Collections/Disbursement provisioning endpoint with the Collection Widget's subscription key → access denied, even though everything else about the request was correct. Fix: subscribe to the specific product you're calling and use *that* product's primary key.
6. **Sandbox call-volume quota exhaustion** → `403`, with a multi-day cooldown before it resets (`"Out of call volume quota. Quota will be replenished in 2.13:47:06."`). This is a real risk if the team runs automated test loops in the days right before the event and burns the quota before demo day.
7. **Expired bearer token** silently causing `401` on `bc-authorize`/product calls — tokens last only 3600 seconds; a long build/demo session needs its own refresh logic, not just a token grabbed once at the start of the day.
8. **Endpoints referenced in docs but not actually reachable in sandbox** (e.g. `MerchantTransferWithConsent`) — at least one confirmed community report of a documented endpoint simply not existing in the sandbox, guessed to be production-only, never confirmed by MTN staff. Lesson: **verify every endpoint you plan to use actually 202/200s in your own sandbox account before building a demo flow around it — don't trust the written docs alone.**

---

## MINIMUM VIABLE INTEGRATION FOR A REWARDS APP

Given everything above — especially that the SA-specific Disbursement product on MTN's own portal is a commercial bulk-agreement product, not a self-serve API, and that the exact SA sandbox REST availability for Disbursements is unconfirmed — here is the safest build path for a 48-hour demo:

1. **Day one, first hour:** Log into momodeveloper.mtn.com yourselves and check, inside the portal (not from outside docs): (a) does `Disbursements` appear as a subscribable product when your account/country context is South Africa; (b) does the in-portal "try it out" for `disbursement/v1_0/transfer` actually return 202 against `X-Target-Environment: sandbox`; (c) open `/api-documentation/testing/` while logged in to get the real reserved-MSISDN list for forced PENDING/FAILED outcomes. **This single check determines which of the two paths below you're on.**

2. **Path A — if sandbox Disbursements works for your account:**
   a. Subscribe to the **Disbursements** product → get its `Ocp-Apim-Subscription-Key`.
   b. `POST /v1_0/apiuser` with a fresh UUIDv4 and a `providerCallbackHost` (a webhook.site URL is fine for a demo) → 201.
   c. `POST /v1_0/apiuser/{id}/apikey` → get `apiKey`.
   d. `POST /disbursement/token/` with `Authorization: Basic base64(id:apiKey)` → get `access_token` (expires in 3600s; refresh before it lapses during a long demo).
   e. For each reward payout: `POST /disbursement/v1_0/transfer` with a fresh UUIDv4 `X-Reference-Id`, `Bearer` token, `X-Target-Environment: sandbox`, amount in `EUR` (sandbox quirk), plain-text `payerMessage`/`payeeNote`, payee `partyIdType: MSISDN` using one of the reserved test MSISDNs you found in step 1c to force a chosen demo outcome.
   f. Poll `GET /disbursement/v1_0/transfer/{referenceId}` every few seconds and render `status` (+ `reason` on `FAILED`) in your app UI. Do not depend on the callback — its payload shape is undocumented.
   g. **Pre-record a fallback demo video** of a successful run, in case sandbox quota/availability fails live on stage (real risk given the undocumented rate limit and the unconfirmed SA availability).

3. **Path B — if SA sandbox Disbursements does NOT work (the more likely outcome given the product-page evidence):**
   a. Reframe the demo around **Collections** ("Get Paid") instead, which is unambiguously a live sandbox product, to demonstrate the payment-rail mechanics end to end (request-to-pay from a "sponsor" wallet into your app's own float), and mock the actual "pay the user" leg with a clearly-labeled simulated payout inside your own backend/UI, explicitly disclosed to judges as "disbursement API pending MTN production approval — sandboxed via Collections + a simulated payout ledger for the demo."
   b. Ask the mentors on day one (see below) whether they can grant temporary access to a working disbursement sandbox for the hackathon specifically — this is exactly the kind of thing hackathon mentor support exists for.

4. Regardless of path, wire the **MoMo PWA MicroSite bridge** (§6) if the hackathon's mini-app track requires running inside the MoMo app shell: listen for `MoMoWebViewEvent`/`START_JOURNEY` to get `msisdn` + `micrositeToken` for free, start a 45-50s heartbeat immediately, and post `AWAITING_FOR_APPROVAL` → `APPROVED`/`REJECTED` → `DONE` around your payout action so the host app's own UX chrome reflects transaction state correctly. Use the provided simulator zip to test this without a physical enrolled device.

---

## QUESTIONS TO ASK THE MOMO MENTORS ON DAY ONE

1. Does the South Africa sandbox account actually expose `disbursement/v1_0/transfer` as a callable REST endpoint under `X-Target-Environment: sandbox`, or is South Africa's disbursement offering genuinely restricted to the bulk/Excel-upload Customer Portal product described at `SouthAfrica_Disbursement_productDetails`?
2. If SA disbursement REST is not available, can you grant our team temporary access to a working disbursement sandbox (any country) for the purposes of this hackathon demo?
3. What is the current list of reserved/test MSISDNs in the sandbox, and which ones force `PENDING`, `FAILED`, and (if it exists) `REJECTED` outcomes for both Collections and Disbursements?
4. What is the actual documented payload shape MTN posts to our `providerCallbackHost` webhook on transaction completion? Is it worth building against, or should we rely on polling only?
5. What is the numeric sandbox rate limit (calls per minute/hour), so we don't get locked out with a multi-day cooldown right before our demo slot?
6. Is the "MoMo Mini App Program" review/approval process (analogous to the Interact/Channel-as-a-Service manual Partner Portal review) something a hackathon prototype can bypass for a live demo, or must we simulate the container entirely?
7. Where can we find the actual CSP restrictions, viewport requirements, and visual design-standard document promised on the Mini App Program overview page — it wasn't rendered content we could reach publicly.
8. Is the hackathon's "Mini App" concept built on the existing MoMo PWA/React-Native-WebView MicroSite bridge we found documented, or on the newer Ant International/Alipay mini-program platform reported in the press (initial rollout reportedly Nigeria-only, Q3 2026) — these appear to be two different things and we want to build against the right one.
9. Section 3 of the hackathon T&Cs says pre-existing projects are disqualifying "unless approved by organizers" — can we get written confirmation of exactly what pre-event research/scaffolding is acceptable?
10. Section 4's IP clause grants an "exclusive license" over our "demos and products" for marketing purposes, alongside a statement that we "retain ownership" — can you clarify the practical scope of that exclusivity (does it limit our ability to demo or license the same product elsewhere afterward)?
