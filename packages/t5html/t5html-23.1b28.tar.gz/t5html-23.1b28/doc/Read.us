T5HTML
======

Converts a text file into HTML. 

The text must be formatted according to the rules of a Trivial Text Tree To
Trivial HTML (T5HTML) file.


## Disclaimers

This **Read.Me** is a link to doc/Read.us!
For **licensing** look at meta/license.


## Example

```t5html
## t5html

## definitions / macros
##
DCT := <!DOCTYPE html>
CHARSET := meta charset=utf-8
VIEWPORT := meta name=viewport
DESC := meta name=description content="A simple HTML5 Template"
AUTHOR := meta name=author content=splendor
OG_PROPERTY := meta property=og:title content=HTML5-Template |
            .. meta property=og:type content=website |
            .. meta property=og.url content=www.example.org |
            .. meta property=og.description content=Example for t5html |
            .. meta property=og.image content=noneatm
FAVICON := link rel=icon href=/favicon.ico |
        .. link rel=icon href=/favicon.svg type=image/svg+xml |
        .. link rel=apple-touch-icon href=/apple-touch-icon.png
CSS_ := link rel=stylesheet 
JS_  := script src=

## DOCUMENT-TREE
#
!DCT
html > head
      # not more then one multiline macro per line
      CHARSET | DESC | AUTHOR | FAVICON
      OG_PROPERTY
      CSS_ href=css/styles.css?v=23.1
      JS_ js/script.js
   body
      main
         article#example
            h1 > "This is an t5html-example
            p class=p-normal
               " A human readable, strucured file
               .. written in a specific format called the
               .. Trivial Text-Tree To Trivial HTML (ttttthtml or t5html)
               .. format, allows for easy prototyping of web-pages.

```

translates into:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8"/>
    <meta name="description" content="A simple HTML5 Template"/>
    <meta name="author" content="splendor"/>
    <link rel="icon" href="/favicon.ico"/>
    <link rel="icon" href="/favicon.svg" type="image/svg+xml"/>
    <link rel="apple-touch-icon" href="/apple-touch-icon.png"/>
    <meta property="og:title" content="HTML5-Template"/>
    <meta property="og:type" content="website"/>
    <meta property="og.url" content="www.example.org"/>
    <meta property="og.description" content="Example" for t5html/>
    <meta property="og.image" content="noneatm"/>
    <link rel="stylesheet" href="css/styles.css?v=23.1"/>
    <script src="js/script.js">
  </head>
  <body>
    <main>
      <article id="example">
        <h1>
          This is an t5html-example
        </h1>
        <p class="p-normal">
           A human readable, strucured file written in a specific format called the Trivial Text-Tree To Trivial HTML (ttttthtml or t5html) format, allows for easy prototyping of web-pages.
        </p>
      </article>
    </main>
  </body>
</html>
```


## t5html-Syntax

1. Every line is processed separatly

2. except a line is the continuation of the previous one, signified by a
   leading `..`

3. Whitespaces are important! Don't ignore them, they seperate syntactic
   elements.

4. Indentation matters! Every indentation marks a hierarchical step down!

5. There are 6 type of lines: blanks, verbatim, elements, comments, text-nodes,
   macros.

6. Every line-type starts with a special symbol, except: blanks, elements and
   macros.

7. Macros have a macroname followed by an assignment operator `:=` and after a
   white-space the macro-value.

8. The first word of an element-line is the element's name.

9. Indentation are **3 whitespaces**! Do **not** use **tabs**!

10. There is a special syntax for `id` and `class` attributes: `div#id.class` !

11. `>` means an hierarchical step down, `<` up and `|` same hierarchical level
    if uses in the same line. They substitute indentation if used in the same
    line, e.g.: `div > p > "Paragraph text`.

12. A leading `"` double-quote marks a text-node.




## For Developers

Start with `Read.4dev` in the `doc` directory.


[//]: # vi: set et ts=4 sw=4 ai ft=markdown tw=80 cc=+0 spl=en:
