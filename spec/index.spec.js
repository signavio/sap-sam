const translateGettext = require('../lib/translateGettext.js')

describe('translateGettext()', () => {
    let processedTranslations
    let emptyEntry
    let nonFuzzyEntry
    let fuzzyEntryComment
    let fuzzyEntry
    let entryFuzzyAfterOtherComment

    const setupTranslations = (input, fuzzy, overwrite, callback) => {
        translateGettext(input, fuzzy, overwrite, processedPoFile => {
            processedTranslations = processedPoFile.translations['']
            emptyEntry = processedTranslations['Configure']
            nonFuzzyEntry = processedTranslations['Control']
            fuzzyEntryComment = processedTranslations['fuzzy test comment']
            fuzzyEntry = processedTranslations['Copy all contents']
            entryFuzzyAfterOtherComment =
                processedTranslations['fuzzy suceeds other comment']
            callback()
        })
    }

    describe('`fuzzy` = true and `overwrite` = true', () => {
        beforeAll(done => {
            setupTranslations('./spec/messages.po', true, true, done)
        })

        it('should translate empty entry and mark it as fuzzy', () => {
            expect(emptyEntry.msgstr[0].length).not.toEqual(0)
            expect(emptyEntry.comments.flag).toEqual('fuzzy')
        })
        it('should translate and overwrite fuzzy entry but leave fuzzy flag', () => {
            expect(fuzzyEntry.msgstr[0]).not.toEqual('ONLY_IF_UNFUZZY')
            expect(fuzzyEntry.comments.flag).toEqual('fuzzy')
        })

        it('should translate and overwrite fuzzy, non-empty entry with a comment', () => {
            expect(fuzzyEntryComment.msgstr[0]).not.toEqual('ONLY_IF_UNFUZZY')
            expect(fuzzyEntryComment.comments.flag).toEqual('fuzzy, c-format')
        })
        it('should not newly translate non-empty entry', () => {
            expect(nonFuzzyEntry.msgstr[0]).toEqual('DONT_TRANSLATE_AGAIN')
        })
    })

    describe('`fuzzy` = true and `overwrite` = false', () => {
        beforeAll(done => {
            setupTranslations('./spec/messages.po', true, false, done)
        })

        it('should translate empty entry and mark it as fuzzy', () => {
            expect(emptyEntry.msgstr[0].length).not.toEqual(0)
            expect(emptyEntry.comments.flag).toEqual('fuzzy')
        })

        it('should not overwrite fuzzy entry', () => {
            expect(fuzzyEntry.msgstr[0]).toEqual('ONLY_IF_UNFUZZY')
            expect(fuzzyEntry.comments.flag).toEqual('fuzzy')
        })

        it('should not translate fuzzy, non-empty entry with a comment', () => {
            expect(fuzzyEntryComment.msgstr[0]).toEqual('ONLY_IF_UNFUZZY')
            expect(fuzzyEntryComment.comments.flag).toEqual('fuzzy, c-format')
        })

        it('should not newly translate non-empty entry', () => {
            expect(nonFuzzyEntry.msgstr[0]).toEqual('DONT_TRANSLATE_AGAIN')
        })
    })

    describe('`fuzzy` = false and `overwrite` = true', () => {
        beforeAll(done => {
            setupTranslations('./spec/messages.po', false, true, done)
        })

        it('should translate empty entry and not mark it as fuzzy', () => {
            expect(emptyEntry.msgstr[0].length).not.toEqual(0)
            expect(emptyEntry.comments).toBe(undefined)
        })

        it('should overwrite fuzzy entry and remove fuzzy flag', () => {
            expect(fuzzyEntry.msgstr[0]).not.toEqual('ONLY_IF_UNFUZZY')
            expect(fuzzyEntry.comments.flag).not.toEqual('fuzzy')
        })

        it('should overwrite fuzzy entry with a comment and remove fuzzy flag', () => {
            expect(fuzzyEntryComment.msgstr[0]).not.toEqual('ONLY_IF_UNFUZZY')
            expect(fuzzyEntryComment.comments.flag).toEqual('c-format')
        })

        it('should not newly translate non-empty entry', () => {
            expect(nonFuzzyEntry.msgstr[0]).toEqual('DONT_TRANSLATE_AGAIN')
        })

        it('should handle fuzzy entries with futher comments correctly', () => {
            expect(fuzzyEntryComment.comments.flag).not.toEqual('fuzzy')
            expect(entryFuzzyAfterOtherComment.comments.flag).not.toEqual(
                'fuzzy'
            )
        })
    })

    describe('`fuzzy` = false and `overwrite` = false', () => {
        beforeAll(done => {
            setupTranslations('./spec/messages.po', false, false, done)
        })

        it('should translate empty entry and not mark it as fuzzy', () => {
            expect(emptyEntry.msgstr[0].length).not.toEqual(0)
            expect(emptyEntry.comments).toBe(undefined)
        })

        it('should not overwrite fuzzy entry and leave fuzzy flag', () => {
            expect(fuzzyEntry.msgstr[0]).toEqual('ONLY_IF_UNFUZZY')
            expect(fuzzyEntry.comments.flag).toEqual('fuzzy')
        })

        it('should not overwrite fuzzy, non-empty entry with a comment', () => {
            expect(fuzzyEntryComment.msgstr[0]).toEqual('ONLY_IF_UNFUZZY')
            expect(fuzzyEntryComment.comments.flag).toEqual('fuzzy, c-format')
        })
        it('should not newly translate non-empty entry', () => {
            expect(nonFuzzyEntry.msgstr[0]).toEqual('DONT_TRANSLATE_AGAIN')
        })
    })

    describe('edge cases', () => {
        beforeAll(done => {
            setupTranslations(
                './spec/messages_translated.po',
                false,
                false,
                done
            )
        })
        it('should terminate given a .po file with only translated messages', () => {
            expect(emptyEntry).toEqual(undefined)
        })
    })
})
