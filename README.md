# micronotes

### Installation

To add micronotes to any page on your website, simply add the following <script> tag to the HTML of the page at the bottom of the <body> section.

```html
<script type="text/javascript" src="https://cdn.jsdelivr.net/gh/generic-github-user/micronotes@v1.0/micronotes.js"></script>
```

If using plain HTML, you will need to add the script to any page that you want to add footnotes to. Alternatively, add it to a PHP functions file or similar file that loads content that must be added to every page on a website - this way, you only need to add the script once.

### Adding Footnotes

By default, footnotes can be added using the {note} and {/note} tags - just put whatever HTML you want in between those two tags, and it will automatically be made into a gorgeous, responsive footnote.

**Note:** the {note} syntax will be depreciated in version 1.5, which will introduce a custom HTML tag, <note>. From then on, the <note> tag should be used instead of {note}. However, {note} will continue to be supported for at least one year after the release of v1.5.

## Requirements

None! micronotes was designed to work without any dependencies or requirements of any kind - just drop it into your web page, and it'll work. One of the issues I had with some other JavaScript footnote plugins and libraries was that they needed [jQuery](https://jquery.com/) or other libraries to be loaded in order to work. Something as simple as adding footnotes to a web page should not require entire libraries - it should be simple, lightweight, and independent.

## Issues

Please submit any and all issues you have with micronotes to the [issues page](https://github.com/generic-github-user/micronotes/issues). I'll try to help you resolve it as soon as possible, or recommend an alternative solution if necessary.

If you want a feature added, submit that to the issues page too. I can't guarantee that everything people ask for will be added, but I'll read everything you submit.

## Alternatives

Some other great options for adding footnotes to a website include Lukas Mathis' [footnotes script](http://ignorethecode.net/blog/2010/04/20/footnotes/) from [ignore the code](http://ignorethecode.net/blog/) and [Matt Gemmell](https://github.com/mattgemmell/footnotes-popover)'s [Footnotes Popover](https://github.com/mattgemmell/footnotes-popover) script. Even just using a <title> tag with a superscript element can work, but it's not extremely elegant. [CSS Script](https://www.cssscript.com/) also has a [footnote generator](https://www.cssscript.com/sticky-footnote-generator/), in case you're looking for something that doesn't require adding any scripts to your code.

If you want to add footnotes to a [WordPress](https://wordpress.org/) website, I recommend the [Easy Footnotes](https://wordpress.org/plugins/easy-footnotes/) plugin, since JavaScript doesn't work too well with WordPress.

There really aren't that many options when it comes to adding clean, modern footnotes to a web page, though. The issue I had with most of the existing solutions was that they looked outdated, were missing important features, or relied on jQuery or other JavaScript libraries. Hopefully I was able to improve upon the existing options, and maybe someone will find this little project useful.
