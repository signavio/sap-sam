#! /usr/bin/env node

const translateGettext = require('./lib/translateGettext.js')
const argv = require('yargs' )
    .usage('Usage: machine-gettext [options]')
    .example(
        'machine-gettext -i=messages_de_de.po -o=messages_de_de -m=non-fuzzy-overwrite',
        'Writes all missing translations as non-fuzzy msgstrs into messages_de_de.' +
        ' Overwrites fuzzy messages.'
    )
    .default('mode', 'fuzzy')
    .alias('i', 'input')
    .alias('o', 'output')
    .alias('m', 'mode')
    .describe('i', 'Relative path to input file')
    .alias('o', 'Relative path to output file')
    .alias('m',
        'Mode: either `fuzzy`, `non-fuzzy` or `non-fuzzy-overwrite`')
    .demandOption(['input','output'])
    .help('h')
    .alias('h', 'help')
    .argv

console.log(`translating .po file: ${argv.input}`)

const callback = () => {
    console.log(`writing to file: ${argv.output}`)
}

translateGettext(argv.input, argv.mode, callback, argv.output)
