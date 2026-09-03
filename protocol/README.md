# Protocol

The protocol is the source of truth for agent behavior.

`manifest.json` declares the protocol version and the canonical schemas, policies, and
modes that adapters consume.

Adapters may translate these contracts into skills, plugins, prompts, hooks, CLI output, editor rules, or CI checks. They must not redefine the contract locally.
