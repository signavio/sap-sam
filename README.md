# machine-gettext
``machine-gettext`` is a node module for adding machine translations to [GNU gettext .po files](https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html).
To translate content, it uses the [DeepL](https://www.deepl.com/translator) cloud service.

## Installation
Install ``machine-gettext`` by running ``npm install -g machine-gettext``.

## Usage
You can use ``machine-gettext`` via the command line or require it in a JavaScript file.

### Command line
On the command line you can run ``machine-gettext`` with the following arguments:

* ``-in, --input``: Relative path to input file

* ``-out, --output``: Relative path to output file

* ``-f, --fuzzy``: If specified, mark added translation as fuzzy

* ``-o, --overwrite``: If specified, overwrite existing fuzzy translations

The following example writes all missing translations as non-fuzzy msgstrs into ``messages`` and overwrites fuzzy messages:

```
machine-gettext -i=messages.po -o=messages.po -m=non-fuzzy-overwrite
```

### JavaScript
You can also require the module as ``translateGettext`` in a JavaScript file and execute ``translateGettext`` as a function with the following arguments:

* ``input`` (string): Relative path to input file

* ``markAsFuzzy`` (boolean): If ``true``, mark added translation as fuzzy

* ``overwrite`` (boolean): If ``true``, overwrite existing fuzzy translations

* ``callback`` (function): Executed after all messages have been processed. Takes a [gettext-parser](https://github.com/smhg/gettext-parser).po file object as its argument.

* ``output`` (string, optional): Relative path to output file 

The following example loads the content of ``./messages.po``, adds missing translations and logs the new content:

```JavaScript
const translateGettext = require('translateGettext')

poFile = parser.po.parse(fileSystem.readFileSync('./messages.po'))
translateGettext(poFile, true, false, processedPoFile => {
    console.log(processedPoFile)
})
```

**Note:** The example code marks the new translations as fuzzy and doesn't overwrite existing fuzzy translations.

## Contribution
Contributions are welcome.
Make sure you run the tests with ``npm run test`` before creating a pull request and add test cases that cover the contributed code.

Possible improvement are, for example:

* explicitely set the target language (currently determined via the .po file header),

* allow integration with alternative translation services,

* better support for interpolation and pluralization,

* support list of terms that shouldn't be translated (for example: product names),

* translation memory support.

## Authors

* Timotheus Kampik - [@TimKam](https://github.com/TimKam)
* Oleg Yarin - [@monapasan](https://github.com/monapasan)

