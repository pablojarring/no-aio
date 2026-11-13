const DEFAULTS = { enabled: true, hideAiMode: true, mode: "hide" };
const $ = (id) => document.getElementById(id);
const t = (key) => chrome.i18n.getMessage(key) || key;

for (const el of document.querySelectorAll("[data-i18n]")) el.textContent = t(el.dataset.i18n);
document.documentElement.lang = chrome.i18n.getUILanguage();
$("version").textContent = "v" + chrome.runtime.getManifest().version;

function render(s) {
  $("enabled").checked = s.enabled;
  $("hideAiMode").checked = s.hideAiMode;
  $("modes").disabled = !s.enabled;
  $("hideAiMode").disabled = !s.enabled;
  $("aiModeRow").classList.toggle("disabled", !s.enabled);
  $("state").textContent = s.enabled ? `${t("on")} · ${t(s.mode === "web" ? "modeWeb" : "modeHide")}` : "Off";
  $("state").classList.toggle("off", !s.enabled);
  for (const r of document.querySelectorAll('input[name="mode"]')) r.checked = r.value === s.mode;
}

async function update(patch) {
  await chrome.storage.sync.set(patch);
  render(await chrome.storage.sync.get(DEFAULTS));
}

chrome.storage.sync.get(DEFAULTS, (s) => {
  render(s);
  requestAnimationFrame(() => document.body.classList.add("ready"));
});
$("enabled").addEventListener("change", (e) => update({ enabled: e.target.checked }));
$("hideAiMode").addEventListener("change", (e) => update({ hideAiMode: e.target.checked }));
for (const r of document.querySelectorAll('input[name="mode"]')) {
  r.addEventListener("change", () => update({ mode: r.value }));
}
