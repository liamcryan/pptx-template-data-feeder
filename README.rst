=========================
pptx-template-data-feeder
=========================

This library lets you feed data to pptx-template.

These next two sections come directly from pptx-template, showing how one would 'feed data'.

Text substitution
-----------------

The first example in the pptx-template project page is::

    $ pptx-template --template template.pptx --model model.json --out out.pptx

The model.json file that looks like this::

    {
        "slides": [
            {
                "hello": {
                    "en": [
                    "How are you?",
                    "Hello!"
                    ],
                    "ja": "XNDIEDNEF"
                }
            }
        ]
    }

As you can see, this data is fixed.  But...what if we want the data in model.json to be dynamic?  If it were dynamic, then we could create multiple out.pptx files rather than one, all displaying different data.  We can change our model.json file to this::

    {
        "slides": [
            {
                "hello": {
                    "en": [
                    "{{greeting_1}}",
                    "{{greeting_2}}"
                    ],
                    "ja": "{{greeting_3}}"
                }
            }
        ]
    }

So now we need a way to pick up greeting_1, greeting_2 and greeting_3.  Suppose we have a greetings.csv file that looks like this::

    greeting1,greeting2,greeting3
    "How are you?","Hello","XNDIEDNEF"
    "Well, thanks", "Good Bye", "NVINOE"

Now we can use pptx-template-data-feeder to create the two output.pptx files::

    $ pptx-template-data-feeder --template template.pptx --model model.json --data greetings.csv --out out.pptx

output.pptx will be enumerated this time simply by each row in the greetings.csv file: output-0.pptx, output-1.pptx.

CSV Import
----------

Second example::

    $ pptx-template --template template.pptx --model model.json --out out.pptx

The model.json file in the second example of the pptx-template project page looks like this::

    {
        "slides": [
        {
            "data": {}
        }
        ]
    }

pptx-template internally expects to find a data.csv file that looks like this::

    Year,Sales,Cost,ROI
    1Q,90,45,0.5
    2Q,100,50,0.5
    3Q,60,20,0.33
    4Q,80,60,0.75

The way to make a workflow out of this (because your data is dynamic of course), is to change you model.json to this::

        {
        "slides": [
        {
            "{{data}}": {}
        }
        ]

    }

We need a way to set up {{data}} properly.  Let's create {{data}}.csv (yes include the double brackets)::

    Year,Sales,Cost,ROI
    {% for row in rows %}
        {{row.Year}},{{row.Sales}},{{row.Cost}},{{row.ROI}}
    {% endfor %}

Finally, we need the actual csv data files, call them sales-data1.csv & sales-data2.csv::

    Year,Sales,Cost,ROI
    1Q,90,45,0.5
    2Q,100,50,0.5
    3Q,60,20,0.33
    4Q,80,60,0.75

And::

    Year,Sales,Cost,ROI
    10Q,900,450,0.05
    20Q,1000,500,0.05
    30Q,600,200,0.033
    40Q,800,600,0.075

Our pptx-template-data-feeder call will look like this::

    $ pptx-template-data-feeder --template template.pptx --model model.json --data-template {{data}}.csv --data sales-data1.csv --data sales-data2.csv --out out.pptx

Or we can provide a data directory (containing the csv files)::

    $ pptx-template-data-feeder --template template.pptx --model model.json --data-template {{data}}.csv --data-directory /path/to/sales/data --out out.pptx


out.pptx this time will be: out-sales-data1.pptx & out-sales-data2.pptx
