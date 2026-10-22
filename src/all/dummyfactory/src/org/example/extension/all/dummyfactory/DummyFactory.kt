package org.example.extension.all.dummyfactory

import eu.kanade.tachiyomi.source.Source
import eu.kanade.tachiyomi.source.SourceFactory

class DummyFactory : SourceFactory {
    override fun createSources(): List<Source> = listOf(
        DummyFactorySource("en", "https://example.org"),
        DummyFactorySource("fr", "https://example.org/fr"),
    )
}
