/**
 * Custom router - intelligent routing based on task type, content, and context
 * Routes: default, background, think, longContext, webSearch, image, planning, security, review, refactor
 * Policy: Maximize local usage, only escalate for specific reasons
 * 
 * Priority order (highest to lowest):
 * 1. Manual overrides
 * 2. Image content
 * 3. Context overflow
 * 4. Security audit
 * 5. Failure signals
 * 6. Web search
 * 7. Code review
 * 8. Multi-file refactor
 * 9. Planning/architecture
 * 10. Webdev planning
 * 11. Local (default)
 */
module.exports = async function router(req, config) {
  const messages = req.body.messages || [];
  const lastUserMsg = [...messages].reverse().find(m => m.role === "user");
  
  // Robust text extraction for various message formats
  const msgContent = lastUserMsg?.content;
  let rawContent = '';
  let hasImages = false;
  
  if (Array.isArray(msgContent)) {
    rawContent = msgContent
      .filter(p => p.type === 'text' && typeof p.text === 'string')
      .map(p => p.text)
      .join(' ');
    hasImages = msgContent.some(p => p.type === 'image_url' || p.type === 'image');
  } else if (typeof msgContent === 'string') {
    rawContent = msgContent;
  } else if (msgContent && typeof msgContent === 'object' && typeof msgContent.text === 'string') {
    rawContent = msgContent.text;
  } else if (msgContent != null) {
    rawContent = JSON.stringify(msgContent);
  }
  const content = rawContent.toLowerCase();

  // Get config values with defaults
  const routes = config.Router || {};
  const longContextThreshold = routes.longContextThreshold || 60000;

  // === MANUAL OVERRIDES (highest priority) ===
  // Use anchored regex to avoid false positives like "don't use claude"
  if (/\b(use|route to|switch to)\s+opus\b/.test(content)) {
    return "openrouter,anthropic/claude-opus-4.5";
  }
  if (/\b(use|route to|switch to)\s+(claude|sonnet)\b/.test(content)) {
    return "openrouter,anthropic/claude-sonnet-4.5";
  }
  if (/\b(use|route to|switch to)\s+(thinking|deepseek)\b/.test(content)) {
    return routes.think || "openrouter,deepseek/deepseek-v3.2";
  }

  // === IMAGE CONTENT (local can't handle) ===
  if (hasImages) {
    return routes.image || "openrouter,google/gemini-2.5-flash";
  }

  // === CONTEXT OVERFLOW (local can't handle) ===
  // Estimate total context size (rough: 4 chars ≈ 1 token, with 15% safety margin)
  const totalChars = messages.reduce((sum, m) => {
    const c = typeof m.content === 'string' ? m.content : JSON.stringify(m.content);
    return sum + c.length;
  }, 0);
  const estimatedTokens = Math.ceil((totalChars / 4) * 1.15);
  
  if (estimatedTokens > longContextThreshold) {
    return routes.longContext || "openrouter,google/gemini-3-flash-preview";
  }

  // === SECURITY AUDIT (high stakes, use stronger model) ===
  const securityPatterns = [
    /\b(security vulnerability|cve-\d+)\b/i,
    /\b(sql[_-]?injection|xss|csrf)\s+(attack|vulnerability|fix)/i,
    /\breview.*(auth|permission|crypto)/i,
    /\baudit.*(security|permission|access)/i,
    /\b(rls|row[_-]?level[_-]?security)\s+polic/i,
    /\bpenetration test/i,
  ];
  
  if (securityPatterns.some(r => r.test(content))) {
    return routes.security || "openrouter,anthropic/claude-sonnet-4.5";
  }

  // === FAILURE SIGNALS → THINKING MODEL ===
  const failureSignals = [
    /\b(build failed|compilation failed)\b/i,
    /\b(test(s)? failed|failing tests)\b/i,
    /\b(exit code [1-9]\d*)\b/i,
    /\b(unhandled|exception|traceback)\b/i,
    /\b(type error|ts(?!x)\d{3,})\b/i
  ];

  if (failureSignals.some(r => r.test(rawContent))) {
    return routes.think || "openrouter,deepseek/deepseek-v3.2";
  }

  // === WEB SEARCH (requires online capability) ===
  // Only explicit web search intent, URLs alone are not enough
  const explicitWebIntent = [
    /\b(search the web|web search|search online|look up online|google)\b/,
    /\baccording to (the )?(docs|documentation|official)\b/,
    /\bfrom (the )?internet\b/,
  ];
  const recencyWithWebContext = /\b(latest|newest|recent)\s+(version|release|changelog|announcement|pricing|news)\b/;
  // URL + fetch intent (not just any URL in code)
  const urlWithFetchIntent = /\bhttps?:\/\/\S+/.test(content) && 
    /\b(open|read|browse|summarize|extract|look at|check|fetch)\b/.test(content);
  
  if (explicitWebIntent.some(r => r.test(content)) || recencyWithWebContext.test(content) || urlWithFetchIntent) {
    return routes.webSearch || "openrouter,google/gemini-2.5-flash:online";
  }

  // === CODE REVIEW / BUG HUNTING ===
  const reviewRegexes = [
    /\b(code review|review (this|my|the) (code|pr|diff|changes))\b/,
    /\b(find bugs|bug hunt|edge cases|regression)\b/,
    /\b(check my work|verify my)\b/,
    /\bcritique (this|my|the)\b/,
  ];

  if (reviewRegexes.some(r => r.test(content))) {
    return routes.review || "openrouter,google/gemini-3-flash-preview";
  }

  // === MULTI-FILE REFACTOR ===
  const refactorRegexes = [
    /\b(refactor|restructure)\s+(across|the|multiple|all)\b/,
    /\bacross (the )?codebase\b/,
    /\bmultiple files\b/,
    /\blarge (change|refactor|migration)\b/,
    /\b(migration|migrate)\s+(from|to)\b/,
  ];

  if (refactorRegexes.some(r => r.test(content))) {
    return routes.refactor || "openrouter,anthropic/claude-sonnet-4.5";
  }

  // === PLANNING/ARCHITECTURE (benefits from stronger model) ===
  const planningRegexes = [
    /\b(architecture|architect)\s+(for|of|design|review)\b/,
    /\bdesign (pattern|system|the|a|this)\b/,
    /\b(roadmap|strategy)\s+(for|to)\b/,
    /\btrade-?offs?\s+(between|of|for)\b/,
    /\bpros and cons\b/,
    /\bplan (out|the architecture|the system)\b/,
  ];
  
  if (planningRegexes.some(r => r.test(content))) {
    return routes.planning || "openrouter,deepseek/deepseek-v3.2";
  }

  // === WEB/APP BUILD INTENT → PLANNING PASS ===
  const webdevRegexes = [
    /\b(website|web\s*app|landing\s*page|dashboard|admin\s*panel)\b/,
    /\b(next\.?js|react|remix|svelte|tailwind|shadcn)\b/,
    /\b(supabase|firebase|oauth|stripe|payments)\b/,
    /\b(api routes?|trpc|prisma|drizzle)\b/,
  ];

  if (webdevRegexes.some(r => r.test(content))) {
    return routes.webdevPlanning || routes.planning || "openrouter,moonshotai/kimi-k2.5";
  }

  // === EVERYTHING ELSE → LOCAL ===
  // Reasoning triggers, debugging, routine coding all stay local
  // User can explicitly request escalation with "use opus/claude/thinking"
  return routes.default || "local,qwen3-coder";
};
