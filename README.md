# machine-gettext
``machine-gettext`` is a node module for adding machine translations to [GNU gettext .po files](https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html).
To translate content, it uses the [DeepL](https://www.deepl.com/translator) cloud service.

## Installation
Install ``machine-gettext`` by running ``npm install -g machine-gettext``.

## Usage
You can use ``machine-gettext`` via the command line or require it in a JavaScript file.

### Command line
On the command line you can run ``machine-gettext`` with the following arguments:

* ``-i, --input``: Relative path to input file

* ``-o, --output``: Relative path to output file

* ``-m, --mode``: one of the following:

    *  ``fuzzy`` (default): Marks all added translations as fuzzy; ignores existing translations, even if they are marked as ``fuzzy``

    *  ``non-fuzzy``: Doesn't mark added translations as fuzzy; ignores existing translations, even if they are marked as ``fuzzy``

    * ``non-fuzzy-overwrite``:  Doesn't mark added translations as fuzzy; overwrites existing translations if they are marked as ``fuzzy``

The following example writes all missing translations as non-fuzzy msgstrs into ``messages`` and overwrites fuzzy messages:

```
machine-gettext -i=messages.po -o=messages.po -m=non-fuzzy-overwrite
```

### JavaScript
You can also require the module as ``translateGettext`` in a JavaScript file and execute ``translateGettext`` as a function with the following arguments:

* ``input`` (string): Relative path to input file

* ``mode`` (string): See above (command line arguments)

* ``callback`` (function): Executed after all messages have been processed. Takes a [gettext-parser](https://github.com/smhg/gettext-parser).po file object as its argument.

* ``output`` (string, optional): Relative path to output file 

The following example loads the content of ``./messages.po``, adds missing translations and logs the new content:

```JavaScript
const translateGettext = require('translateGettext')

poFile = parser.po.parse(fileSystem.readFileSync('./messages.po'))
translateGettext(poFile, 'fuzzy', processedPoFile => {
    console.log(processedPoFile)
})
```

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

