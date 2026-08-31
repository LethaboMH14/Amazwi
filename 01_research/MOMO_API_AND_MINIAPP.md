# MoMo API & Mini App — Technical Reference
**Compiled:** 2026-08-15 · For build planning. Verify against live docs before the event.

---

## 1. WHAT A MOMO MINI APP ACTUALLY IS

MTN's Mini App programme is documented as **"MoMo PWA Mini App Integration."**

**It is a Progressive Web App.** Not native, not a proprietary DSL like WeChat's WXML. That means:

- Standard web stack — React / Vue / Svelte / plain JS, a service worker, a manifest.
- No app store, no native build, no install friction.
- Loaded inside the MoMo super app shell (the Ant International platform provides the container).
- **You can build and demo one in 24 hours.** That is the good news.
- **So can everyone else in the room.** Your differentiation cannot be the stack — it must be the idea, the polish, and the pitch.

MTN's published scope for the programme covers four things:
1. End-to-end **technical integration requirements**
2. **UX and design standards**
3. Mandatory **security and compliance controls**
4. **Terms & Conditions** for participating in the MoMo ecosystem

> ⚠️ **ACTION BEFORE 2 SEPT:** the detailed spec is gated behind a developer account and the public pages are navigation stubs. Register at `momodeveloper.mtn.com`, join `momodevelopercommunity.mtn.com`, and pull the **full PWA Mini App integration guide + design standards**. Judges from MTN will instantly recognise an entry that follows their own design system. Almost nobody else will have read it.

### Design implications to assume until proven otherwise
- Assume a **constrained viewport** inside a host shell — design mobile-first, single column.
- Assume the host owns navigation, identity and the payment sheet. Don't rebuild them.
- Assume **strict CSP / sandboxing.** Avoid exotic browser APIs; prefer graceful degradation.
- Assume the user arrives **already authenticated as a MoMo user.** Do not build a login screen — that's the whole point of a mini app.
- Optimise ruthlessly for **payload size**. Data cost is a real barrier in this market.

---

## 2. THE NINE API PRODUCT FAMILIES

MTN publishes far more than "collections and disbursements." The full set:

### 2.1 Get Paid (Collections)
Collect payments from consumers and businesses.
`Request Payment` · `Refund` · `Notify` · `Payment Status` · `Account Balance`
→ The default. Every hackathon team will use this.

### 2.2 Pay (Disbursements)
Send money out to wallets — salaries, benefits, supplier payments, payouts.
`Transfer` · `Transfer Status` · `Account Balance`
→ Rewards, refunds, revenue-share, escrow release.
⚠️ **Production disbursement requires IP whitelisting** by your MoMo provider.

### 2.3 Invoice ⭐
Bill a customer for **deferred payment**, across channels.
→ Credit-like UX **without becoming a lender**. Instalments, pay-later, staged payments. Almost nobody uses this.

### 2.4 Manage
Transaction visibility and financial oversight — balance enquiry, transaction status, reconciliation.
→ The backbone of any merchant bookkeeping product.

### 2.5 Distribute ⭐
Resell MTN/MoMo services — cash-in, cash-out, airtime — on commission.
→ Turn any user or shop into a **mini-agent**. Powerful for agent-network or township-commerce plays.

### 2.6 Interact — "Channel as a Service" ⭐⭐
**Insert your service as a secondary menu item inside the MoMo USSD menu and app.**
→ The most powerful and least understood API MTN has. You are not building an app users must discover — you are appearing inside the thing they already open. Reaches **feature phones**. Rova Pay (Nigeria winner) used this.

### 2.7 Identify (KYC) ⭐
Retrieve verified customer identity **without collecting or storing it yourself**.
→ Zero-friction onboarding, no KYC burden, no data liability. "Sign in with MoMo."

### 2.8 Get Consent ⭐⭐
USSD-based terms acceptance, authenticated with the user's **MoMo PIN**.
→ A **PIN-signed mandate primitive**. Combine with Invoice + Pay and you have standing authority over a wallet — effectively **direct debit for the unbanked**, which Africa does not have. This is the most under-exploited thing in the entire catalogue. See Wild Concept 1 in the research brief.

### 2.9 Notify
Transactional SMS to the customer after payment.
→ Reaches users with no data. Essential for offline-first designs.

### Also available
- **Remittances** — cross-border transfers.
- **Collection Widget** — accept MoMo payment on any website via QR code.

---

## 3. AUTHENTICATION & CALL MECHANICS

Three credential layers:

| Credential | Where from | Purpose |
|---|---|---|
| `Ocp-Apim-Subscription-Key` | Developer portal, per product | Identifies your subscription |
| **API User ID + API Key** | Provisioned per environment | Identifies your app |
| **Access Token** (Bearer) | `POST /{product}/token/` with Basic auth = `apiUserId:apiKey` | Per-call auth. **Expires in 3600s.** |

### Required headers on transactional calls
```
Authorization: Bearer <access_token>
Ocp-Apim-Subscription-Key: <subscription_key>
X-Reference-Id: <UUID v4 — unique per request, this IS your idempotency key>
X-Target-Environment: sandbox | mtnsouthafrica | mtnnigeria | ...
X-Callback-Url: https://your.host/callback     (optional but use it)
Content-Type: application/json
```

### Core endpoints
```
POST  /collection/token/
POST  /collection/v1_0/requesttopay
GET   /collection/v1_0/requesttopay/{X-Reference-Id}
GET   /collection/v1_0/account/balance
POST  /disbursement/token/
POST  /disbursement/v1_0/transfer
GET   /disbursement/v1_0/transfer/{X-Reference-Id}
```
(v2_0 variants exist for several operations; check the portal.)

- Base (production): `https://proxy.momoapi.mtn.com`
- Sandbox: provisioned via `sandbox.momodeveloper.mtn.com`
- Party identification: `partyIdType: "MSISDN"`, party ID in full international format (e.g. `27XXXXXXXXX`).

### Async model — build for it from minute one
`requesttopay` is **asynchronous**. You submit, you get a 202, and the outcome arrives either at your `X-Callback-Url` webhook or by polling the status endpoint on the same `X-Reference-Id`.

**Demo-day survival tips:**
- Implement **both** webhook and polling. Conference wifi will break your webhook.
- Use **ngrok** (or Cloudflare Tunnel) for callbacks during the event.
- Store every `X-Reference-Id` you generate. It's your only handle on a transaction.
- Build a **"simulate success" toggle** in the demo UI. Sandbox flakiness has killed better demos than ours.

---

## 4. PRE-EVENT CHECKLIST

- [ ] Register on `momodeveloper.mtn.com` — get subscription keys for **Collections, Disbursements, and Remittances**
- [ ] Provision sandbox API User + API Key; complete one successful `requesttopay` end-to-end
- [ ] Join `momodevelopercommunity.mtn.com` and **download the full Mini App PWA integration spec + design standards**
- [ ] Read the community's **Sandbox Q&A (105 topics)** and **Production Q&A (55 topics)** — that's where the real gotchas live
- [ ] Import the official MoMo Postman collection; save a working environment
- [ ] Stand up a deployment target (Vercel / Netlify / Cloudflare Pages) so demo deploys are instant
- [ ] Prepare a callback receiver + tunnel, tested
- [ ] Decide the stack and scaffold the *knowledge*, not the code — **all code must be written during the event**

---

## 5. KNOWN CONSTRAINTS & GOTCHAS

- Access tokens live **1 hour** — refresh logic is not optional.
- `X-Reference-Id` must be a **fresh UUID per request**; reuse causes conflicts.
- Sandbox and production behave differently. Do not assume parity.
- Disbursements in production need **IP whitelisting** — irrelevant for the hackathon, critical for the "how do we ship this" slide.
- Sandbox availability is variable. **Always have a recorded demo video as backup.**
- Country coverage: 16 markets. For SA use the South Africa target environment.
