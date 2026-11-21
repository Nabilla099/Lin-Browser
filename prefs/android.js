// Lin Browser - default preferences (GeckoView)

// Telemetry, studies, promotions
pref("toolkit.telemetry.enabled", false);
pref("toolkit.telemetry.unified", false);
pref("datareporting.healthreport.uploadEnabled", false);
pref("datareporting.policy.dataSubmissionEnabled", false);
pref("app.shield.optoutstudies.enabled", false);
pref("app.normandy.enabled", false);
pref("browser.discovery.enabled", false);

// No speculative network activity
pref("network.prefetch-next", false);
pref("network.dns.disablePrefetch", true);
pref("network.predictor.enabled", false);
pref("network.http.speculative-parallel-limit", 0);

// Lower memory use
pref("dom.ipc.processCount", 2);
pref("browser.sessionhistory.max_total_viewers", 1);
pref("browser.cache.memory.capacity", 32768);
