const translateGettext = require('../lib/translateGettext.js')

describe('translateGettext()', () => {
    let processedTranslations
    let emptyEntry
    let nonFuzzyEntry
    let fuzzyEntryComment
    let fuzzyEntry
    let entryFuzzyAfterOtherComment

    const setupTranslations = (input, mode, callback) => {
        translateGettext(input, mode, processedPoFile => {
            processedTranslations = processedPoFile.translations['']
            emptyEntry = processedTranslations['Configure']
            nonFuzzyEntry = processedTranslations['Control']
            fuzzyEntryComment = processedTranslations['fuzzy test comment']
            fuzzyEntry = processedTranslations['Copy all contents']
            entryFuzzyAfterOtherComment = processedTranslations['fuzzy suceeds other comment']
            callback()
        })
    }

    describe('`fuzzy` mode', () => {
        beforeAll(done => {
            setupTranslations('./spec/messages.po', 'fuzzy', done)
        })

        it('should translate empty entry and mark it as fuzzy', () => {
            expect(emptyEntry.msgstr[0].length).not.toEqual(0)
            expect(emptyEntry.comments.flag).toEqual('fuzzy')
        })
        it('should not newly translate fuzzy, non-empty entry', () => {
            expect(fuzzyEntry.msgstr[0]).toEqual('ONLY_IF_UNFUZZY')
            expect(fuzzyEntry.comments.flag).toEqual('fuzzy')
        })
        it('should not newly translate fuzzy, non-empty entry with comment', () => {
            expect(fuzzyEntryComment.msgstr[0]).toEqual('ONLY_IF_UNFUZZY')
            expect(fuzzyEntryComment.comments.flag).toEqual('fuzzy, c-format')
        })
        it('should not newly translate non-empty entry', () => {
            expect(nonFuzzyEntry.msgstr[0]).toEqual('DONT_TRANSLATE_AGAIN')
        })
    })
    
    describe('`non-fuzzy` mode', () => {
        beforeAll(done => {
            setupTranslations('./spec/messages.po', 'non-fuzzy', done)
        })

        it('should translate empty entries (and not mark them as fuzzy)', () => {
            expect(emptyEntry.msgstr[0].length).not.toEqual(0)
            expect(emptyEntry.comments).toBe(undefined)
        })
        it('should not newly translate fuzzy, non-empty entry', () => {
            expect(fuzzyEntry.msgstr[0]).toEqual('ONLY_IF_UNFUZZY')
            expect(fuzzyEntry.comments.flag).toEqual('fuzzy')
        })
        it('should not newly translate fuzzy, non-empty entry with comment', () => {
            expect(fuzzyEntryComment.msgstr[0]).toEqual('ONLY_IF_UNFUZZY')
            expect(fuzzyEntryComment.comments.flag).toEqual('fuzzy, c-format')
        })
        it('should not newly translate non-empty entries', () => {
            expect(nonFuzzyEntry.msgstr[0]).toEqual('DONT_TRANSLATE_AGAIN')
        })
    })
    
    describe('`non-fuzzy-overwrite` mode', () => {
        beforeAll(done => {
            setupTranslations('./spec/messages.po', 'non-fuzzy-overwrite', done)
        })

        it('should translate empty entries (and not mark them as fuzzy)', () => {
            expect(emptyEntry.msgstr[0].length).not.toEqual(0)
            expect(emptyEntry.comments).toBe(undefined)
        })
        it('should translate fuzzy, non-empty entries and "unfzz" them', () => {
            expect(fuzzyEntry.msgstr[0]).not.toEqual('ONLY_IF_UNFUZZY')
            expect(fuzzyEntry.comments.flag).not.toEqual('fuzzy')
        })
        it('should not newly translate non-empty entries', () => {
            expect(nonFuzzyEntry.msgstr[0]).toEqual('DONT_TRANSLATE_AGAIN')
        })
        it('should handle fuzzy entries with futher comments correctly', () => {
            expect(fuzzyEntryComment.comments.flag).not.toEqual('fuzzy')
            expect(entryFuzzyAfterOtherComment.comments.flag).not.toEqual('fuzzy')
        })
    })

    describe('edge cases', () => {
        beforeAll(done => {
            setupTranslations('./spec/messages_translated.po', 'non-fuzzy', done)
        })
        it('should terminate given a .po file with only translated messages', () => {
            expect(emptyEntry).toEqual(undefined)
        })
    })
})
