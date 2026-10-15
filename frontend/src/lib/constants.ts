// ─── History Seed Data ────────────────────────────────────────────────────────
export const HISTORY_TITLES = [
  "Best POS Systems for Small Restaurants in 2026 (Complete Comparison Guide)",
  "How to Choose the Right Restaurant Management Software for Your Business",
  "10 Common Mistakes Restaurants Make While Choosing a POS System",
  "FoodChow vs POSApt POS: Which Restaurant POS Is Better in 2026?",
  "Top 7 Benefits of Using Cloud-Based POS Systems for Restaurants",
  "Restaurant Billing Software: Features Every Restaurant Owner Should Know",
  "How Digital Billing Is Transforming the Restaurant Industry",
  "Restaurant Management Software for Cafés & Cloud Kitchens – Complete Guide",
  "Step-by-Step Guide to Setting Up a POS System for a New Restaurant",
  "Future Trends in Restaurant Technology: POS, AI, and Automation",
];

// ─── Claude System Prompt ─────────────────────────────────────────────────────
export const BLOG_SYSTEM_PROMPT = `You are a world-class SEO content strategist and blog writer. Given a blog topic, return ONLY valid JSON (no markdown fences, no backticks, no preamble) with this exact structure:
{
  "title": "Compelling, SEO-optimized blog title",
  "meta_title": "SEO meta title (max 60 chars)",
  "meta_description": "Compelling meta description (max 155 chars)",
  "keywords": ["primary keyword", "secondary keyword", "keyword 3", "keyword 4", "keyword 5"],
  "table_of_contents": ["Introduction", "Section 2 title", "Section 3 title", "Section 4 title", "Section 5 title", "Conclusion"],
  "content": "Full blog in markdown. Use ## for H2 sections, ### for H3. Write at least 900 words. Include an intro paragraph, 4-5 detailed sections with subheadings, bullet points, and a conclusion. Make it engaging, informative, and SEO-friendly."
}`;

// ─── API Config ───────────────────────────────────────────────────────────────
export const ANTHROPIC_MODEL = "claude-sonnet-4-20250514";
export const ANTHROPIC_MAX_TOKENS = 4000;

// ─── App Meta ─────────────────────────────────────────────────────────────────
export const APP_NAME = "AI Blog Writing Agent";
export const APP_DESCRIPTION = "Generate SEO-optimized blog posts in minutes with Claude AI.";
