#! /usr/bin/env node

const translateGettext = require('./lib/translateGettext.js')
const argv = require('yargs')
    .usage('Usage: machine-gettext [options]')
    .example(
        'machine-gettext -in=messages_de_de.po -out=messages_de_de -f -o',
        'Writes all missing translations as fuzzy msgstrs into messages_de_de.' +
            ' Overwrites fuzzy messages.'
    )
    .boolean(['o', 'f'])
    .default('fuzzy', false)
    .default('overwrite', false)
    .alias('o', 'overwrite')
    .alias('f', 'fuzzy')
    .alias('in', 'input')
    .alias('out', 'output')
    .describe('in', 'Relative path to input file')
    .alias('out', 'Relative path to output file')
    .describe('f', 'Mark added translation as fuzzy')
    .describe('o', 'Overwrite existing translations which are marked as fuzzy')
    .demandOption(['input', 'output'])
    .help('h')
    .alias('h', 'help').argv

console.log(`translating .po file: ${argv.input}`)

const callback = () => {
    console.log(`writing to file: ${argv.output}`)
}

translateGettext(argv.input, argv.mode, callback, argv.output)
