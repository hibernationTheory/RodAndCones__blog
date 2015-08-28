# PrimerCSS : The CSS toolkit and guidelines that power GitHub

In their own words PrimerCSS is the CSS Toolkit and Guidelines that power Github Front End. Simply put, it is their own version of Bootstrap. The web page not only documents the class names associated with the framework but also lays down some conventions to be followed when writing CSS using PrimerCSS. 

I have lately been on the hunt for best CSS practices so below are my notes from the website for actionable steps that can be implemented for any CSS you write.

- For a predictable behaviour while using padding and border, it is best to set the box-sizing to border box on every element.
- Use of normalize.css to get rid of small inconsistencies between browsers and devices.
- If you are to use a `<a>` element as a button by adding a pre-built class to it, you make sure to specify a ‘role=button’ attribute for it for accessibility purposes.
- One should be using ‘spaces’ while coding since it the “only way to guarantee code render the same in any person’s environment.”
- Always remember to place paragraphs of text in a `<p>` tag.
- Items in a list form should always be in `<ul>`, `<ol>` or `<dl>`. Never use a set of div or p’s for them.
- Every form input that has text attached should utilize a <label> tag. Especially radio or checkbox elements.
- When grouping selectors, keep individual selectors to a single line. This allows for more accurate error reporting.

Some of the formatting rules that are specified in the documentation have an arbitrary feeling to it. For example the following rule:

> Avoid trailing slashes in self-closing elements. For example, `<br>`, `<hr>`, `<img>`, and `<input>`.

Doesn’t really specify the reasoning behind the choice. Besides building an habit around the mentioned convention can get you into trouble in some other instances (for example when writing JSX for React  - which requires the trailing slash to be added). 

I think the key when looking at these documentations is to synthesize the most generalizable rules and takes the rest with a grain of salt.