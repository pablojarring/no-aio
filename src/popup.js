const DEFAULTS = { enabled: true, hideAiMode: true, mode: "hide" };
const $ = (id) => document.getElementById(id);

function render(s) {
  $("enabled").checked = s.enabled;
  $("hideAiMode").checked = s.hideAiMode;
  $("modes").disabled = !s.enabled;
  for (const r of document.querySelectorAll('input[name="mode"]')) r.checked = r.value === s.mode;
}

chrome.storage.sync.get(DEFAULTS, render);

$("enabled").addEventListener("change", (e) => {
  chrome.storage.sync.set({ enabled: e.target.checked });
  $("modes").disabled = !e.target.checked;
});
$("hideAiMode").addEventListener("change", (e) => chrome.storage.sync.set({ hideAiMode: e.target.checked }));
for (const r of document.querySelectorAll('input[name="mode"]')) {
  r.addEventListener("change", () => chrome.storage.sync.set({ mode: r.value }));
}
