from typing import Dict, Optional
from sdk.language_service.providers.framework import HoverProvider, LanguageRequestContext

class MarkdownHoverProvider(HoverProvider):
    def provide(self, context: LanguageRequestContext) -> Optional[Dict]:
        # Pure function returning markdown hover using context
        return {
            "contents": {
                "kind": "markdown",
                "value": "### `lala.print`\n\nPrints a value to standard output."
            }
        }
