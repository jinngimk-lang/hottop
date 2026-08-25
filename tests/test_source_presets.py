from hottop.source_presets import resolve_source_quality, source_preset


def test_direct_publishers_override_aggregator_defaults() -> None:
    assert resolve_source_quality("reuters.com", fallback=0.62) == 0.96
    assert resolve_source_quality("apnews.com", fallback=0.62) == 0.95
    assert resolve_source_quality("theguardian.com", fallback=0.62) == 0.90


def test_unknown_sources_keep_collector_fallback() -> None:
    assert resolve_source_quality("example.invalid", fallback=0.68) == 0.68


def test_domain_matching_handles_subdomains_and_urls() -> None:
    assert resolve_source_quality("https://www.reuters.com/world/story", fallback=0.5) == 0.96
    assert resolve_source_quality("https://m.ithome.com/html/123.htm", fallback=0.5) == 0.84


def test_presets_group_sources_by_editorial_domain() -> None:
    film = source_preset("film-entertainment")
    ai = source_preset("ai-tech")
    culture = source_preset("zh-internet-culture")

    assert "apnews.com" in film
    assert "reuters.com" in ai
    assert "ithome.com" in culture
