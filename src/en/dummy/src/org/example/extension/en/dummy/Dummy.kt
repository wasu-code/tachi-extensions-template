package org.example.extension.en.dummy

import eu.kanade.tachiyomi.source.model.FilterList
import eu.kanade.tachiyomi.source.model.MangasPage
import eu.kanade.tachiyomi.source.model.Page
import eu.kanade.tachiyomi.source.model.SChapter
import eu.kanade.tachiyomi.source.model.SManga
import eu.kanade.tachiyomi.source.model.SMangaUpdate
import eu.kanade.tachiyomi.source.online.HttpSource

// Keep name/lang/baseUrl identical to the source { } block in build.gradle.kts
class Dummy : HttpSource() {
    override val name = "Dummy"
    override val lang = "en"
    override val baseUrl = "https://example.org"
    override val supportsLatest = true

    private fun dummyManga() = SManga.create().apply {
        url = "/manga/dummy"
        title = "Dummy manga"
    }

    override suspend fun getPopularManga(page: Int) = MangasPage(listOf(dummyManga()), hasNextPage = false)

    override suspend fun getLatestUpdates(page: Int) = MangasPage(listOf(dummyManga()), hasNextPage = false)

    override suspend fun getSearchManga(page: Int, query: String, filters: FilterList) =
        MangasPage(emptyList(), hasNextPage = false)

    override suspend fun getMangaUpdate(
        manga: SManga,
        chapters: List<SChapter>,
        fetchDetails: Boolean,
        fetchChapters: Boolean,
    ): SMangaUpdate {
        val chapter = SChapter.create().apply {
            url = "/manga/dummy/chapter-1"
            name = "Chapter 1"
        }
        return SMangaUpdate(manga, listOf(chapter))
    }

    override suspend fun getPageList(chapter: SChapter): List<Page> = emptyList()
}
