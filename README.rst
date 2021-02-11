==============
pptx-templater
==============

When you need a template for your pptx-template.

I wrote a blog post to help explain use cases: https://hellofrom.liamcryan.com/2020/12/pptx-templates-with-python.html

A typical pptx-template model might look like this (model.json)::

    {
      "slides": {
        "1": {
          "greeting": {
            "en": "Hello!",
            "ja": "こんにちは！"
          },
        },

    }

::

    %pptx-template --template template.pptx --out out.pptx --model model.json

Instead of specifying the fixed greetings within the model.json, we want to have a file of greetings and create an output pptx for each one.  This is very useful when you have multiple reports to be created with the same pptx template, but populated with different 

A pptx-templater model (model.json)::

    {
      "slides": {
        "1": {
          "greeting": {
            "en": "{{greeting_en}}",
            "ja": "{{greeitng_ja}}"
          },
        },

    }

Also needed is the data file (csv)::

    greeting_ja,greeting_en
    こんにちは！,Hello!
    ハウディ,Howdy

Please excuse my Japanese, ハウディ came from https://translate.google.com/#view=home&op=translate&sl=auto&tl=ja&text=Howdy

In the model.json, the {{greeting_en}} tells the jinja2 templating engine (https://jinja.palletsprojects.com/en/2.11.x/) to template the greeting_en column in the csv.

::

    %pptx-templater --template template.pptx --out out-{{greeting_en}}.pptx --model-template model.json --data csv

Notice you can specify the format of the output file using jinja style bracketing.  In this example, the output files would be called::

    out-Hello!.pptx
    out-Howdy.pptx

Getting started -> Python installation::

    %pip install git+https://github.com/liamcryan/pptx-templater.git

Now you are able to use the command line tool::

    %pptx-templater

