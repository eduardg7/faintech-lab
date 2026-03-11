"""HTTP client for Agent Memory Cloud API."""

import os
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import httpx

from agentmemory.exceptions import (
    AgentMemoryError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from agentmemory.models import (
    Agent,
    Memory,
    MemoryType,
    PaginatedResponse,
    Project,
    SearchResult,
)


class MemoryClient:
    """
    Client for Agent Memory Cloud API.

    Usage:
        >>> client = MemoryClient(api_key="your-api-key")
        >>> memory = client.memories.create(
        ...     agent_id="agent-001",
        ...     memory_type="outcome",
        ...     content="Task completed successfully"
        ... )

    Or using environment variable:
        >>> import os
        >>> os.environ["AGENT_MEMORY_API_KEY"] = "your-api-key"
        >>> client = MemoryClient()
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.faintech.dev/v1",
        timeout: float = 30.0,
    ) -> None:
        """
        Initialize the MemoryClient.

        Args:
            api_key: API key for authentication. If not provided, reads from
                AGENT_MEMORY_API_KEY environment variable.
            base_url: Base URL for the API. Defaults to production.
            timeout: Request timeout in seconds.

        Raises:
            AuthenticationError: If API key is not provided and not in environment.
        """
        self.api_key = api_key or os.environ.get("AGENT_MEMORY_API_KEY")
        if not self.api_key:
            raise AuthenticationError(
                "API key required. Pass api_key parameter or set AGENT_MEMORY_API_KEY environment variable."
            )

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self._client = httpx.Client(timeout=timeout)
        self._memories: Optional[MemoriesResource] = None
        self._agents: Optional[AgentsResource] = None
        self._projects: Optional[ProjectsResource] = None
        self._search: Optional[SearchResource] = None

    @property
    def memories(self) -> "MemoriesResource":
        """Access memories resource."""
        if self._memories is None:
            self._memories = MemoriesResource(self)
        return self._memories

    @property
    def agents(self) -> "AgentsResource":
        """Access agents resource."""
        if self._agents is None:
            self._agents = AgentsResource(self)
        return self._agents

    @property
    def projects(self) -> "ProjectsResource":
        """Access projects resource."""
        if self._projects is None:
            self._projects = ProjectsResource(self)
        return self._projects

    @property
    def search(self) -> "SearchResource":
        """Access search resource."""
        if self._search is None:
            self._search = SearchResource(self)
        return self._search

    def _headers(self) -> Dict[str, str]:
        """Build request headers."""
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            path: API endpoint path.
            params: Query parameters.
            json: JSON body.

        Returns:
            Response JSON.

        Raises:
            AuthenticationError: 401 response.
            NotFoundError: 404 response.
            RateLimitError: 429 response.
            ValidationError: 422 response.
            AgentMemoryError: Other errors.
        """
        url = urljoin(self.base_url + "/", path.lstrip("/"))

        response = self._client.request(
            method=method,
            url=url,
            headers=self._headers(),
            params=params,
            json=json,
        )

        if response.status_code == 401:
            raise AuthenticationError("Invalid API key", status_code=401)
        elif response.status_code == 404:
            raise NotFoundError(f"Resource not found: {path}", status_code=404)
        elif response.status_code == 422:
            errors = response.json().get("detail", "Validation failed")
            raise ValidationError(str(errors), status_code=422)
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                "Rate limit exceeded",
                retry_after=int(retry_after) if retry_after else None,
                status_code=429,
            )
        elif response.status_code >= 400:
            raise AgentMemoryError(
                f"API error: {response.status_code} - {response.text}",
                status_code=response.status_code,
            )

        return response.json()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "MemoryClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()


class MemoriesResource:
    """Resource for memory operations."""

    def __init__(self, client: MemoryClient) -> None:
        self._client = client

    def create(
        self,
        agent_id: str,
        memory_type: Union[MemoryType, str],
        content: str,
        workspace_id: Optional[str] = None,
        project_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        confidence: Optional[float] = None,
    ) -> Memory:
        """
        Create a new memory.

        Args:
            agent_id: ID of the agent creating the memory.
            memory_type: Type of memory (outcome, learning, preference, decision).
            content: Memory content text.
            workspace_id: Optional workspace ID.
            project_id: Optional project ID.
            tags: Optional list of tags.
            metadata: Optional metadata dict.
            confidence: Optional confidence score (0.0-1.0).

        Returns:
            Created Memory object.

        Example:
            >>> memory = client.memories.create(
            ...     agent_id="agent-001",
            ...     memory_type="outcome",
            ...     content="Task completed successfully",
            ...     tags=["deployment", "success"],
            ... )
        """
        if isinstance(memory_type, MemoryType):
            memory_type = memory_type.value

        payload: Dict[str, Any] = {
            "agent_id": agent_id,
            "memory_type": memory_type,
            "content": content,
        }

        if workspace_id:
            payload["workspace_id"] = workspace_id
        if project_id:
            payload["project_id"] = project_id
        if tags:
            payload["tags"] = tags
        if metadata:
            payload["metadata"] = metadata
        if confidence is not None:
            payload["confidence"] = confidence

        data = self._client._request("POST", "/memories", json=payload)
        return Memory.from_dict(data)

    def get(self, memory_id: str) -> Memory:
        """
        Get a memory by ID.

        Args:
            memory_id: Memory UUID.

        Returns:
            Memory object.

        Raises:
            NotFoundError: If memory doesn't exist.
        """
        data = self._client._request("GET", f"/memories/{memory_id}")
        return Memory.from_dict(data)

    def list(
        self,
        agent_id: Optional[str] = None,
        project_id: Optional[str] = None,
        memory_type: Optional[Union[MemoryType, str]] = None,
        tags: Optional[List[str]] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> PaginatedResponse:
        """
        List memories with optional filters.

        Args:
            agent_id: Filter by agent ID.
            project_id: Filter by project ID.
            memory_type: Filter by memory type.
            tags: Filter by tags (AND logic).
            limit: Max results per page (1-100).
            offset: Pagination offset.

        Returns:
            PaginatedResponse with Memory items.
        """
        params: Dict[str, Any] = {"limit": limit, "offset": offset}

        if agent_id:
            params["agent_id"] = agent_id
        if project_id:
            params["project_id"] = project_id
        if memory_type:
            params["memory_type"] = (
                memory_type.value if isinstance(memory_type, MemoryType) else memory_type
            )
        if tags:
            params["tags"] = ",".join(tags)

        data = self._client._request("GET", "/memories", params=params)
        return PaginatedResponse.from_dict(data, Memory)

    def update(
        self,
        memory_id: str,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        confidence: Optional[float] = None,
    ) -> Memory:
        """
        Update a memory.

        Args:
            memory_id: Memory UUID.
            content: New content (optional).
            tags: New tags (optional).
            metadata: New metadata (optional).
            confidence: New confidence score (optional).

        Returns:
            Updated Memory object.
        """
        payload: Dict[str, Any] = {}

        if content is not None:
            payload["content"] = content
        if tags is not None:
            payload["tags"] = tags
        if metadata is not None:
            payload["metadata"] = metadata
        if confidence is not None:
            payload["confidence"] = confidence

        data = self._client._request("PUT", f"/memories/{memory_id}", json=payload)
        return Memory.from_dict(data)

    def delete(self, memory_id: str) -> None:
        """
        Delete a memory.

        Args:
            memory_id: Memory UUID.

        Raises:
            NotFoundError: If memory doesn't exist.
        """
        self._client._request("DELETE", f"/memories/{memory_id}")

    def compact(
        self,
        agent_id: str,
        project_id: Optional[str] = None,
        max_age_days: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Compact memories for an agent.

        Consolidates and summarizes old memories to reduce storage and improve
        retrieval performance.

        Args:
            agent_id: Agent ID to compact memories for.
            project_id: Optional project ID filter.
            max_age_days: Only compact memories older than this many days.

        Returns:
            Dict with compaction results (memories_processed, memories_created, etc.)

        Example:
            >>> result = client.memories.compact(
            ...     agent_id="agent-001",
            ...     max_age_days=30,
            ... )
            >>> print(f"Processed {result['memories_processed']} memories")
        """
        payload: Dict[str, Any] = {"agent_id": agent_id}

        if project_id:
            payload["project_id"] = project_id
        if max_age_days is not None:
            payload["max_age_days"] = max_age_days

        return self._client._request("POST", "/memories/compact", json=payload)


class AgentsResource:
    """Resource for agent operations."""

    def __init__(self, client: MemoryClient) -> None:
        self._client = client

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Agent:
        """
        Create a new agent.

        Args:
            name: Agent name.
            description: Optional description.
            metadata: Optional metadata.

        Returns:
            Created Agent object.
        """
        payload: Dict[str, Any] = {"name": name}

        if description:
            payload["description"] = description
        if metadata:
            payload["metadata"] = metadata

        data = self._client._request("POST", "/agents", json=payload)
        return Agent.from_dict(data)

    def get(self, agent_id: str) -> Agent:
        """
        Get an agent by ID.

        Args:
            agent_id: Agent ID.

        Returns:
            Agent object.
        """
        data = self._client._request("GET", f"/agents/{agent_id}")
        return Agent.from_dict(data)

    def list(self, limit: int = 20, offset: int = 0) -> PaginatedResponse:
        """
        List all agents.

        Args:
            limit: Max results per page.
            offset: Pagination offset.

        Returns:
            PaginatedResponse with Agent items.
        """
        params = {"limit": limit, "offset": offset}
        data = self._client._request("GET", "/agents", params=params)
        return PaginatedResponse.from_dict(data, Agent)


class ProjectsResource:
    """Resource for project operations."""

    def __init__(self, client: MemoryClient) -> None:
        self._client = client

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Project:
        """
        Create a new project.

        Args:
            name: Project name.
            description: Optional description.
            metadata: Optional metadata.

        Returns:
            Created Project object.
        """
        payload: Dict[str, Any] = {"name": name}

        if description:
            payload["description"] = description
        if metadata:
            payload["metadata"] = metadata

        data = self._client._request("POST", "/projects", json=payload)
        return Project.from_dict(data)

    def get(self, project_id: str) -> Project:
        """
        Get a project by ID.

        Args:
            project_id: Project ID.

        Returns:
            Project object.
        """
        data = self._client._request("GET", f"/projects/{project_id}")
        return Project.from_dict(data)

    def list(self, limit: int = 20, offset: int = 0) -> PaginatedResponse:
        """
        List all projects.

        Args:
            limit: Max results per page.
            offset: Pagination offset.

        Returns:
            PaginatedResponse with Project items.
        """
        params = {"limit": limit, "offset": offset}
        data = self._client._request("GET", "/projects", params=params)
        return PaginatedResponse.from_dict(data, Project)


class SearchResource:
    """Resource for search operations."""

    def __init__(self, client: MemoryClient) -> None:
        self._client = client

    def keyword(
        self,
        query: str,
        agent_id: Optional[str] = None,
        project_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10,
    ) -> List[SearchResult]:
        """
        Keyword search across memories.

        Args:
            query: Search query string.
            agent_id: Filter by agent ID.
            project_id: Filter by project ID.
            tags: Filter by tags.
            limit: Max results.

        Returns:
            List of SearchResult objects with relevance scores.

        Example:
            >>> results = client.search.keyword("redis caching", limit=5)
            >>> for result in results:
            ...     print(f"Score: {result.score}")
            ...     print(f"Content: {result.memory.content}")
        """
        params: Dict[str, Any] = {"query": query, "limit": limit}

        if agent_id:
            params["agent_id"] = agent_id
        if project_id:
            params["project_id"] = project_id
        if tags:
            params["tags"] = ",".join(tags)

        data = self._client._request("GET", "/search/keyword", params=params)
        return [SearchResult.from_dict(item) for item in data["results"]]

    def semantic(
        self,
        query: str,
        agent_id: Optional[str] = None,
        project_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 5,
    ) -> List[SearchResult]:
        """
        Semantic search using natural language queries.

        Uses vector embeddings to find conceptually similar memories,
        not just keyword matches.

        Args:
            query: Natural language query.
            agent_id: Filter by agent ID.
            project_id: Filter by project ID.
            tags: Filter by tags.
            limit: Max results.

        Returns:
            List of SearchResult objects with relevance scores.

        Example:
            >>> results = client.search.semantic(
            ...     "How did we improve performance?",
            ...     limit=5,
            ... )
        """
        params: Dict[str, Any] = {"query": query, "limit": limit}

        if agent_id:
            params["agent_id"] = agent_id
        if project_id:
            params["project_id"] = project_id
        if tags:
            params["tags"] = ",".join(tags)

        data = self._client._request("GET", "/search/semantic", params=params)
        return [SearchResult.from_dict(item) for item in data["results"]]
