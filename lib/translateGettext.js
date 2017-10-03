#! /usr/bin/env node

const fileSystem = require('fs')
const parser = require('gettext-parser')
const translate = require('node-deepl')

module.exports = (input, mode, callback, output) => {
    const poFile = parser.po.parse(fileSystem.readFileSync(input))
    let language
    try {
        language = poFile.headers.language.toUpperCase()
    } catch (e) {
        console.log(
            `${input} does not contain language definition in the header. In order to perform the translation language should be specifed.`
        )
        return
    }

    const contextKeys = Object.keys(poFile.translations)

    let contextIndex = 0 // asynchronous code; can't use forEach index

    contextKeys.forEach(context => {
        contextIndex++
        const translationKeys = []
        Object.keys(poFile.translations[context]).forEach(translationKey => {
            const translation = poFile.translations[context][translationKey]
            const isEmpty = !translation.msgstr[0]
            const isFuzzy = hasFuzzyFlag(translation)
            if (mode === 'non-fuzzy-overwrite') {
                // consider fuzzy & empty
                if (isFuzzy) {
                    translation.comments.flag = translation.comments.flag.replace(
                        'fuzzy, ',
                        ''
                    )
                    translationKeys.push(translationKey)
                }
                if (isEmpty) translationKeys.push(translationKey)
            } else if (isEmpty) {
                // consider empty only
                if (mode === 'fuzzy') {
                    addFuzzyFlag(translation)
                }
                translationKeys.push(translationKey)
            }
        })
        let translationIndex = 0 // asynchronous code; can't use forEach index
        // edge case handling: no translation needed
        if (translationKeys.length === 0) callback(poFile)
        // translate
        translationKeys.forEach(translation => {
            translate(translation, 'EN', language, (err, res) => {
                translationIndex++
                if (err) {
                    if (translation)
                        console.log(`couldn't translate: ${translation}`)
                    return
                }
                poFile.translations[context][translation].msgstr[0] = res
                if (
                    contextIndex === contextKeys.length &&
                    translationIndex === translationKeys.length
                ) {
                    if (output)
                        fileSystem.writeFileSync(
                            output,
                            parser.po.compile(poFile)
                        )
                    callback(poFile)
                }
            })
        })
    })
}

function hasFuzzyFlag(translation) {
    return (
        translation.comments &&
        translation.comments.flag &&
        translation.comments.flag.includes('fuzzy')
    )
}

function addFuzzyFlag(translation) {
    if (!translation.comments) {
        translation.comments = {
            flag: 'fuzzy',
        }
    } else {
        const oldFlag = translation.comments.flag
        const newFlag = oldFlag ? oldFlag + ', fuzzy' : 'fuzzy'
        translation.comments.flag = newFlag
    }
}
