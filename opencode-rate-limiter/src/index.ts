import type { Plugin } from '@opencode-ai/plugin';

/**
 * Rate Limiter Plugin for OpenCode
 *
 * Prevents "rate limit reached" errors by enforcing a minimum interval
 * between consecutive API calls. Uses the `chat.params` hook which fires
 * right before each LLM request.
 *
 * Behavior:
 * - Tracks the timestamp of each API call per provider
 * - If a new call comes in before MIN_INTERVAL_MS has elapsed, it waits
 *   the remaining time before allowing the request to proceed
 * - First request after idle: no delay (smart throttling)
 * - Rapid-fire requests: automatically spaced out
 */

const MIN_INTERVAL_MS = 5000; // 5 seconds between requests

// Track last call time per provider to avoid cross-provider throttling
const lastCallTimeByProvider = new Map<string, number>();

// Global fallback for non-provider-specific throttling
let lastCallTimeGlobal = 0;

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const RateLimiterPlugin: Plugin = async (_ctx) => {
  return {
    name: 'opencode-rate-limiter',

    'chat.params': async (input, _output) => {
      const providerKey = input.provider?.info?.id ?? 'global';
      const now = Date.now();

      // Get last call time for this specific provider
      const lastProviderCall = lastCallTimeByProvider.get(providerKey) ?? 0;
      const lastCall = Math.max(lastProviderCall, lastCallTimeGlobal);
      const elapsed = now - lastCall;

      if (elapsed < MIN_INTERVAL_MS && lastCall > 0) {
        const waitTime = MIN_INTERVAL_MS - elapsed;
        const modelName = input.model?.id ?? 'unknown';
        console.log(
          `[rate-limiter] Throttling ${providerKey}/${modelName} - waiting ${waitTime}ms (interval: ${MIN_INTERVAL_MS}ms)`,
        );
        await delay(waitTime);
      }

      // Update timestamps after wait (so next call measures from actual send time)
      const sendTime = Date.now();
      lastCallTimeByProvider.set(providerKey, sendTime);
      lastCallTimeGlobal = sendTime;
    },
  };
};

export default RateLimiterPlugin;
