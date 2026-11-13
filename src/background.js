// Service worker: activa/desactiva la redirección a udm=14 (filtro "Web").
const DEFAULTS = { enabled: true, hideAiMode: true, mode: "hide" };
const RULESET = "udm14";

async function syncRuleset() {
  const s = await chrome.storage.sync.get(DEFAULTS);
  const on = s.enabled && s.mode === "web";
  await chrome.declarativeNetRequest.updateEnabledRulesets(
    on ? { enableRulesetIds: [RULESET] } : { disableRulesetIds: [RULESET] }
  );
}

chrome.runtime.onInstalled.addListener(async () => {
  const current = await chrome.storage.sync.get(null);
  await chrome.storage.sync.set({ ...DEFAULTS, ...current });
  await syncRuleset();
});

chrome.runtime.onStartup.addListener(syncRuleset);

chrome.storage.onChanged.addListener((_changes, area) => {
  if (area === "sync") syncRuleset();
});
