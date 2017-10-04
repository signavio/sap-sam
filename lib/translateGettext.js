#! /usr/bin/env node

const fileSystem = require('fs')
const parser = require('gettext-parser')
const deepl_translate = require('node-deepl')

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
    const mapToTranslationObjects = createTranslationObjectsMapper(poFile, mode)
    const translationObjects = contextKeys
        .map(mapToTranslationObjects)
        // flatten array
        .reduce((acc, cur) => acc.concat(cur), [])

    // edge case handling: no translation needed
    if (translationObjects.length === 0) return callback(poFile)

    const translationsPromises = translationObjects.map(translate)
    Promise.all(translationsPromises).then(translatedObjects => {
        translatedObjects.forEach(replaceInPOFile)
        if (output) fileSystem.writeFileSync(output, parser.po.compile(poFile))
        callback(poFile)
    })

    function translate(translationObjects) {
        const { translationKey, context } = translationObjects
        return new Promise((resolve, reject) => {
            deepl_translate(translationKey, 'EN', language, (err, res) => {
                if (err) {
                    if (translationKey)
                        console.log(
                            `Deepl can not translate: ${translationKey}`
                        )
                    resolve({
                        translatedKey: '',
                        translationKey,
                        context,
                    })
                    return
                }
                resolve({
                    translatedKey: res,
                    translationKey,
                    context,
                })
            })
        })
    }

    function replaceInPOFile(translatedObject) {
        const { translatedKey, translationKey, context } = translatedObject
        poFile.translations[context][translationKey].msgstr[0] = translatedKey
        return poFile
    }
}

function createTranslationObjectsMapper(poFile, mode) {
    return context =>
        Object.keys(
            poFile.translations[context]
        ).reduce((acc, translationKey) => {
            const translation = poFile.translations[context][translationKey]
            const isEmpty = !translation.msgstr[0]
            const isFuzzy = hasFuzzyFlag(translation)
            // maybe we should consider always replace empty string does not matter
            // which flag they have
            const replaceTranslation =
                isEmpty && !(isFuzzy && mode === 'non-fuzzy-overwrite')

            // add appropriate flat to the po translations
            // if overwrite remove fuzzy flag
            // if fuzzy add fuzzy flag
            if (mode === 'non-fuzzy-overwrite') {
                if (isFuzzy) {
                    translation.comments.flag = translation.comments.flag.replace(
                        'fuzzy, ',
                        ''
                    )
                }
            } else if (mode === 'fuzzy' && isEmpty) {
                addFuzzyFlag(translation)
            }
            return replaceTranslation
                ? [
                      ...acc,
                      {
                          translationKey,
                          context,
                      },
                  ]
                : acc
        }, [])
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
