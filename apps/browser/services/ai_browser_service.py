class AIBrowserService:
    """Advanced AI features for NovaOS browser."""
    
    def __init__(self, ai_assistant):
        self.ai = ai_assistant

    def _complete(self, prompt):
        if hasattr(self.ai, "ask"):
            return self.ai.ask(prompt)
        return self.ai.process(prompt)
    
    def smart_search(self, query):
        """AI-powered search with context understanding."""
        if not self.ai:
            return []
        
        try:
            prompt = f"Analyze this search query and provide 3 enhanced search suggestions: \"{query}\". Consider user intent and provide more specific, helpful alternatives. Return as a simple list, one per line."
            response = self._complete(prompt)
            return [line.strip() for line in response.split('\n') if line.strip()][:3]
        except Exception:
            return [f"Search for {query}", f"{query} tutorial", f"{query} examples"]
    
    def summarize_page(self, content):
        """Intelligent page summarization."""
        if not self.ai:
            return "AI not available"
        
        try:
            prompt = f"Analyze this webpage content and provide a concise 2-sentence summary: {content[:800]}. Focus on the main purpose and key information."
            return self._complete(prompt)
        except Exception:
            return "Unable to summarize page"

    def ask(self, question, page_content=""):
        """Answer a question using the current page as grounded context."""
        if not self.ai:
            return "AI is unavailable. Configure an AI provider in NovaOS settings."
        context = page_content[:12000]
        prompt = (
            "You are NovaOS Browser AI. Answer the user's question using the page context "
            "when present. Be concise and say when the context is insufficient.\n"
            f"Page context:\n{context}\n\nQuestion: {question}"
        )
        try:
            return self._complete(prompt)
        except Exception:
            return "Nova Browser AI could not complete that request."

    def extract(self, page_content, format_name="key points"):
        return self.ask(f"Extract the {format_name} from this page.", page_content)

    def research_prompt(self, topic):
        return (
            f"Research {topic} across several reliable sources. Compare the evidence, "
            "list useful links, and clearly separate facts from uncertainty."
        )