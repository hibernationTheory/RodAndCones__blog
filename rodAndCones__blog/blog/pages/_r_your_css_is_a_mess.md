# Your CSS is a Mess

### Review of the talk ["Your CSS is a Mess"](https://www.youtube.com/watch?v=C4z_9F6nfS8) by Jonathan Snook (Shopify)

#### tl;dr 

Writing self contained CSS and HTML is key to creating scalable CSS architectures. It also helps when using templating systems as well. Choose your CSS modules wisely to have them be able to exist in isolation (like a li element won't be able to exist in isolation, it relies on the surrounding ul). Keep the specificity of your selectors low and avoid using ID selectors. Choose a naming convention that allows you to identify the root element's, sub-modules and sub-components of your markup and stick with it.

#### Summary

Jonathan Snook is the author of the book 'Scalable and Modular Architecture for CSS and an engineer at Shopify. SMACSS defines a set of ideas and conventions for writing scalable CSS.

In this talk, he mentions how unwieldy CSS gets when multiple people start working on it together and presents set of solutions to tackle the issue under these three categories.

- Categorization
- Naming convention
- Decouple HTML / CSS

He believes that any CSS code that you write can be considered under one of these five main categories:

- **Base**  : Like CSS Reset. Defines what your elements look like at it's core.
- **Layout** : Main layout elements that makeup the page in very general terms. Like Header, Body, Footer.
- **Modules** : Content pieces that goes inside a layout. Like a search dialog box. Modules can contain other modules (Think of a modal dialog box)
- **State** : Variations of the modules due to mostly JS related state changes such as 'disabled state, active state' etc.
- **Theme** : User configuration on top of the base style.

The idea behind categorization is the separation and isolation of CSS and HTML elements. This is an attempt in adapting the 'Single Responsibility Principle' in CSS and to be able to separate concerns. It is a way of aiming to have your CSS and HTML "do one thing and one thing only" by modularizing it.

If you can have self-contained CSS and HTML it can be so much easier to test things in isolation and move them around freely - which makes them suitable for templating usages as well. One implication of this rule is that you need to have modules that can exist in isolation. For example a `<li>` element can't exist in isolation since it depends on the existence of a parent ul.

As a general rule one other thing to remember is to keep the specificity of your selector's low. Don't use an ID when a class would do. It is okay to have them for JS purposes but usually it is an overkill for constructing your CSS. This advice seems to be a recurring theme in the CSS related talks I have listened to so far.

Naming is important in your CSS architecture as well. The particular naming system you end up choosing (like BEM) doesn't matter too much as long as you go with something that has a way of identifying these following parts of your markup:

- Root Element
- Sub Modules
- Sub Components.

One practical advice he offers for picking up class names: Say you are creating classes for a large button. Having your css class names as 'btn large' can be problematic because when it is time for a change it would be really hard to find, select and change all those large buttons at once. Better name it as 'btn-large' This would allow you to propagate a change real easily since you can search and replace things pretty quickly.

He also advises against using inline classes that might come to your HTML through Javascript (such as usage of Jquery .css or slideDown, SlideUp animation methods) and instead adding or removing classes to manage state. This way you would have your css do what it does the best and html do what it is best at.

Finally in the Q&A section of his talk he offers a glimpse to the testing mechanisms that was employed in Yahoo during his employment over there. They would have 'handlebar' partials, and css files with the same name and automated scripts that run and compiles all the partials alongside with their corresponding css files in the same HTML file for testing purposes. One tidbit of wisdom that he offers in his answer is choosing 'convention over configuration'. (as in naming choosing same css file names as handlebar partials so that they can be assembled together automatically.) I found that philosophy to be highly interesting since I never heard mentioned before. I would highly recommend this talk if you are interested in trying to write scalable CSS.