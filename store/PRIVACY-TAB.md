# Pestaña "Privacy practices": respuestas para pegar

Los textos están en inglés porque los revisa el equipo de la tienda.

## Single purpose

```
No AIO has a single purpose: removing Google's AI-generated summaries (AI Overview and the AI Mode tab) from Google Search results pages. It does this either by hiding that block on the page, or, if the user enables "Web" mode, by opening searches in Google's own Web results filter (udm=14), where no AI summary is generated.
```

## Permission justification

**storage**
```
Stores the user's three settings (on/off, mode, hide AI Mode tab) with chrome.storage.sync. Nothing else is stored.
```

**declarativeNetRequest**
```
Used only when the user turns on "Web" mode in the popup. A static rule adds the udm=14 parameter to Google Search result URLs that have no results filter, so Google opens its Web results view. Searches that already use a filter (Images, News, etc.) are not modified. The ruleset is disabled by default. No requests are blocked, logged or sent anywhere.
```

**Host permissions (www.google.*/*)**
```
The content script must run on Google Search result pages (/search) to find and hide the AI Overview block, and declarativeNetRequest needs host access to these same Google domains to apply the optional Web-mode redirect. The list covers only Google's official country domains (google.com/supported_domains); the extension does not run on any other site.
```

## Remote code

- **Are you using remote code?** → **No, I am not using remote code**

## Data usage

Deja **todas** las casillas sin marcar (no recolecta ningún tipo de dato) y marca las tres certificaciones:

- [x] I do not sell or transfer user data to third parties, outside of the approved use cases
- [x] I do not use or transfer user data for purposes that are unrelated to my item's single purpose
- [x] I do not use or transfer user data to determine creditworthiness or for lending purposes

**Privacy policy URL:** `https://pablojarring.github.io/no-aio/privacy/`
