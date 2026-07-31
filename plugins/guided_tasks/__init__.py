"""Guided Tasks plugin — contractual foundation for the Harness guided task flow.

This plugin provides the *contract* (typed, serializable models) for guided tasks.
Operational surfaces (CLI, runtime, store, pipeline, gateway integration) will be
added in subsequent iterations.

No CLI commands, model tools, or runtime components are registered in this version.
"""

from __future__ import annotations


def register(ctx) -> None:
    """Register plugin surfaces with the host.

    In this foundation release, the plugin only exports its models via
    `from plugins.guided_tasks.models import ...`. No CLI commands, model tools,
    or runtime hooks are registered yet.

    Args:
        ctx: PluginContext provided by the plugin loader (unused in v0.1.0).
    """
    # Operational surfaces (CLI, runtime, store, pipeline) will be added later.
    # This no-op register ensures the plugin loads cleanly and declares intent.
    return None


__all__ = ["register"]