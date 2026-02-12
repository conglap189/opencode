// @bun
// src/index.ts
var MIN_INTERVAL_MS = 5000;
var lastCallTimeByProvider = new Map;
var lastCallTimeGlobal = 0;
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
var RateLimiterPlugin = async (_ctx) => {
  return {
    name: "opencode-rate-limiter",
    "chat.params": async (input, _output) => {
      const providerKey = input.provider?.info?.id ?? "global";
      const now = Date.now();
      const lastProviderCall = lastCallTimeByProvider.get(providerKey) ?? 0;
      const lastCall = Math.max(lastProviderCall, lastCallTimeGlobal);
      const elapsed = now - lastCall;
      if (elapsed < MIN_INTERVAL_MS && lastCall > 0) {
        const waitTime = MIN_INTERVAL_MS - elapsed;
        const modelName = input.model?.id ?? "unknown";
        console.log(`[rate-limiter] Throttling ${providerKey}/${modelName} - waiting ${waitTime}ms (interval: ${MIN_INTERVAL_MS}ms)`);
        await delay(waitTime);
      }
      const sendTime = Date.now();
      lastCallTimeByProvider.set(providerKey, sendTime);
      lastCallTimeGlobal = sendTime;
    }
  };
};
var src_default = RateLimiterPlugin;
export {
  src_default as default
};
