==============
pptx-templater
==============

When you need a template for your pptx-template.

If you are reading below and don't quite get it, you will need to familiarize with: https://github.com/m3dev/pptx-template

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

Instead of specifying the fixed greetings within the model.json, we want to have a file of greetings and create an output pptx for each one.  This is very useful when you have multiple reports to be created with the same pptx template, but populated with different data.

A pptx-templater model (model.json)::

    {
      "slides": {
        "1": {
          "greeting": {
            "en": "{{data.greeting_en}}",
            "ja": "{{data.greeitng_ja}}"
          },
        },

    }

Also needed is the data file (data.csv)::

    greeting_ja,greeting_en
    こんにちは！,Hello!
    ハウディ,Howdy

Please excuse my Japanese, ハウディ came from https://translate.google.com/#view=home&op=translate&sl=auto&tl=ja&text=Howdy

In the model.json, the {{data.greeting_en}} tells the jinja2 templating engine (https://jinja.palletsprojects.com/en/2.11.x/) to template the greeting_en column in the data.csv.

The 'data' in {{data.greeting_en}} is globally available to the templating engine, and should always be included prior to the column you wish to access => {{data.column}}.

::

    %pptx-templater --template template.pptx --out out.pptx --model-template model.json
