from .docker import router as DockerRouter
from .system import router as SystemRouter
from .agent import router as AgentRouter

__all__ = ["DockerRouter","SystemRouter", "AgentRouter"]