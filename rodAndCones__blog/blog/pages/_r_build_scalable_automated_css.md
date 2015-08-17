# Build Scalable, Automated CSS

### Review of the talk "Build Scalable, Automated CSS"

#### tl;dr 

You spend most of your time reading code, so optimize your CSS for readability. Use descriptive class names and don't restrict yourself in terms of the character length. Don't use element selectors except for reset or sitewide base styling purposes, as you would be trying yourself to a specific element and markup. Semantic markup using elements might be unnecessary given the rise of semantic attributes.

#### Summary

Below are my impressions and notes from the talk ["Build Scalable, Automated CSS"](https://www.youtube.com/watch?v=Tk_0qYEFtAY) at CSSConf Asia from speaker Christian Lilley. 

(`$speaker: "Christian Lilley"`)

In his talk `$speaker` argues that just like your Javascript, your CSS should adhere to some basic programming principles such as the following:

- Be dry (Don't Repeat Yourself)
- Be maintainable (Write for updates and debugging )
- Don't optimize prematurely.

There are some general rules that you can follow to write more maintainable CSS. According to the `$speaker`; one thing that can be done is to stop yourself from using hacks such as 'float'. Float was pretty much only invented to have text flowing around an image. Using it beyond it's intended purpose ends up creating ugly - incomprehensible code.

I found myself semi-agreeing with this point. I too think that a layout that is based on some convoluted usage of float's can make be pretty incomprehensible but having a float based layout that is abstracted from you through convenient class names (like what Bootstrap would provide) should not be an issue. Given that it's an abstraction, it should also mean that the underlying implementation could be changed by whatever that is most convenient when necessary.

The reason I am not quite on board with inline block is I couldn't find a reliable way of solving the white space bug yet. And the word is that flexbox might not be the best choice in terms of compatibility but is definitely getting there. But it is worth mentioning that flexbox seems to be the most convenient alternative to build layouts easily and efficiently.

During a development process you use most of your time trying to understand your own code, so optimizing for readability is a huge gain in terms of efficiency and your own performance. `$speaker` claims the usage of element names as selectors is the worst idea ever, since you would be tying yourself to a specific component in your HTML architecture but also be writing a pretty generic looking CSS. You should instead be using descriptive, intelligible class names. Don't worry about having too many classes around or having long names for them. They don't bite and there is no issue whatsoever in leveraging classes as extensively as you can. They are as efficient as it gets in terms of performance. The `$speaker` goes on to say that even 'the cool selectors' such as n-th-child should generally be avoided if possible due to sub-optimal perfomance and ambiguity problems. 

Namespacing is a good start but is not a substitute for a more comprehensive naming strategy. It is like saying 'Statistically speaking I am somewhat sure that a collision won't happen'. Well it just might.

The only good usage of element names are for 'normalize' or 'reset' files -  which you should be using by the way even though they are not enforced -, or a style change that you need everywhere now and moving forward (like removing underlines from anchor elements)

At this point in time it goes without saying that CSS preprocessors are good. in fact they might be the best thing since sliced bread for a bread loving CSS user. Make use of those variables (like I am doing in this review) and also the mixins, import statements, etc... Though one thing to beware of could be the use of descendent selectors. The problem with them can be that you would be tying yourself to a specific markup increasing coupling in between your HTML and CSS but also in case you were also using element selectors you would find that you can't put new, external, components in your markup in a sane manner. Your selectors would have unintended consequences.

Some preprocessors can give you a nesting syntax for you to create name prefixes when flattened such as:
```
	.main-content : {
		&__left-nav {}
```
	compiling to:
```
	.main-content__left-nav {}
```

His last point was the most interesting for me, the `$speaker` makes a compelling argument about not sweating it too much about using some of the new semantic html elements such as `<section>` or `<article>`. To quote him directly:

**"Don't feel guilty (if you can't use semantic elements). The era of semantic elements for machine readability is over in favor of semantic 'attributes' (see: wai-aria , microformats)"**

Overall it was a enjoyable talk, the `$speaker` was comfortable and confident in his delivery but given the amount of actual information I found the talk to be a bit too long. Also the titles that the `$speaker` choose for his talking points were a bit too cryptic (be a lover not fighter?). I had a hard time guessing what the upcoming point would be by just looking at the slide deck. Maybe his rules around naming could be extended to presentations as well.

