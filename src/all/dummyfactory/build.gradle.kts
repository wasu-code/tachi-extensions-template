plugins {
    id("ext-android")
}

extension {
    name = "Dummy Factory"
    className = ".DummyFactory"
    versionCode = 1

    // One block per source returned by DummyFactory.createSources()
    source {
        lang = "en"
        baseUrl = "https://example.org"
    }
    source {
        lang = "fr"
        baseUrl = "https://example.org/fr"
    }
}
