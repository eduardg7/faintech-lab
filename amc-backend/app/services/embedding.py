"""OpenAI embedding service for text vector embeddings."""
from typing import List, Dict, Any, Optional
from datetime import datetime
from openai import AsyncOpenAI
from openai.types import CreateEmbeddingResponse
import os

from config import settings


class EmbeddingService:
    """Service for generating text embeddings using OpenAI API."""
    
    # OpenAI embedding models
    MODEL_SMALL = "text-embedding-3-small"  # Cheapest, 1536 dimensions
    MODEL_LARGE = "text-embedding-3-large"  # Better quality, 3072 dimensions
    
    # Pricing per 1M tokens (as of 2024)
    PRICING = {
        MODEL_SMALL: 0.020,  # $0.02 per 1M tokens
        MODEL_LARGE: 0.130,  # $0.13 per 1M tokens
    }
    
    def __init__(self):
        """Initialize OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = self.MODEL_SMALL  # Default to small model
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        response: CreateEmbeddingResponse = await self.client.embeddings.create(
            model=self.model,
            input=text
        )
        
        # Track token usage
        token_count = response.usage.total_tokens
        cost = self._calculate_cost(token_count)
        
        return {
            'embedding': response.data[0].embedding,
            'token_count': token_count,
            'cost': cost,
            'model': self.model
        }
    
    async def embed_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Generate embeddings for multiple texts (batched)."""
        results = []
        
        # Process in batches of up to 100 texts
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response: CreateEmbeddingResponse = await self.client.embeddings.create(
                model=self.model,
                input=batch
            )
            
            total_tokens = response.usage.total_tokens
            cost = self._calculate_cost(total_tokens)
            
            for j, embedding in enumerate(response.data):
                results.append({
                    'embedding': embedding.embedding,
                    'token_count': response.usage.prompt_tokens,
                    'cost': cost / len(batch),  # Distribute cost evenly
                    'model': self.model
                })
        
        return results
    
    def _calculate_cost(self, token_count: int) -> float:
        """Calculate cost in USD for token usage."""
        price_per_million = self.PRICING.get(self.model, 0.020)
        return (token_count / 1_000_000) * price_per_million
    
    async def track_usage(
        self,
        token_count: int,
        cost: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Track embedding usage for cost monitoring."""
        usage_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'token_count': token_count,
            'cost': cost,
            'model': self.model,
            'metadata': metadata or {}
        }
        
        # In production, this would be stored in a database table
        # For now, we log it
        print(f"[EmbeddingService] Usage tracked: {token_count} tokens, ${cost:.6f}")
        
        return usage_record


# Global embedding service instance
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """Get the global embedding service instance."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
