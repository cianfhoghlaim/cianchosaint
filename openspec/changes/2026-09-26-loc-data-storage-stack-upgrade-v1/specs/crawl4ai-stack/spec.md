# cianchosaint-crawl4ai-stack — Capability Spec

> **Spec ID:** `crawl4ai-stack`
> **Capability umbrella:** `cianchosaint-pipeline`
> **Status:** PROPOSED (post-`2026-09-26-loc-data-storage-stack-upgrade-v1` archive)
> **Last updated:** 2026-09-26

## Purpose

Canonical surface for the Crawl4AI web scraper stack — the OpenAI-friendly LLM web crawler + scraper. Covers version pinning.

## ADDED Requirements

### Requirement: Crawl4AI pinned to v0.9.4

The system SHALL pin the Crawl4AI container in `bonnegar/stacks/crawl4ai/compose.yaml` to `unclecode/crawl4ai:${TAG:-v0.9.4}` (with the v0.9.4 default tag).

#### Scenario: Crawl4AI uses pinned v0.9.4 image

- **WHEN** the Crawl4AI container starts
- **THEN** the container SHALL be running `unclecode/crawl4ai:v0.9.4` (the latest security release)
- **AND** the `:v0.9.2` placeholder SHALL NOT appear as the default

## MODIFIED Requirements

None.

## REMOVED Requirements

None.

## Cross-references

- `infrastructure-stacks` (the umbrella spec)
- `package-version-drift` (the Stage 1 spec) — this spec implements Stage 2c
- [Crawl4AI v0.9.4 release](https://github.com/unclecode/crawl4AI/releases/tag/v0.9.4)
