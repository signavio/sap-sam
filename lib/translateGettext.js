#! /usr/bin/env node

const fileSystem = require('fs')
const parser = require('gettext-parser')
const google_translate = require('@k3rn31p4nic/google-translate-api')

module.exports = (input, markAsFuzzy, overwrite, callback, output) => {
    const poFile = parser.po.parse(fileSystem.readFileSync(input))
    let language
    try {
        language = poFile.headers.language.toUpperCase()
    } catch (e) {
        console.log(
            `${input} does not contain any language definition in its header. To perform the translation, you need to specify a language.`,
        )
        return
    }
    if (language.split('_').length) {
        language = language.split('_')[0]
    }

    const contextKeys = Object.keys(poFile.translations)
    const mapToTranslationObjects = createTranslationObjectsMapper(
        poFile,
        markAsFuzzy,
        overwrite,
    )
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
            google_translate(translationKey, { from: 'EN', to: language }).then((res) => {
                if (!res.text) {
                    if (translationKey)
                        console.log(
                            `Google can not translate: ${translationKey}. We'll put an empty string at it's place.`,
                        )
                    resolve({
                        translatedKey: '',
                        translationKey,
                        context,
                    })
                    return
                }
                resolve({
                    translatedKey: res.text,
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

function createTranslationObjectsMapper(poFile, markAsFuzzy, overwrite) {
    return context =>
        Object.keys(
            poFile.translations[context],
        ).reduce((acc, translationKey) => {
            const translation = poFile.translations[context][translationKey]
            const isEmpty = !translation.msgstr[0]
            const isFuzzy = hasFuzzyFlag(translation)

            // replace empty translations
            // or marked as fuzzy in case overwrite is true
            const replaceTranslation = isEmpty || (isFuzzy && overwrite)
            if (!replaceTranslation) return acc
            if (isFuzzy && !markAsFuzzy) {
                translation.comments.flag = removeFuzzyFlag(
                    translation.comments.flag,
                )
            } else if (!isFuzzy && markAsFuzzy) {
                addFuzzyFlag(translation)
            }
            return [
                ...acc,
                {
                    translationKey,
                    context,
                },
            ]
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

function removeFuzzyFlag(flag) {
    return flag
        .replace('fuzzy, ', '') // if 'fuzzy' preceeds other comment
        .replace(', fuzzy', '') // if 'fuzzy' succeeds other comment
        .replace('fuzzy', '') // if 'fuzzy' is only comment
}
