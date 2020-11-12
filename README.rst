=========================
pptx-template-data-feeder
=========================

This library lets you feed data to pptx-template.

Examples
--------

These examples come from the Text Substitution & CSV Import examples here: https://github.com/m3dev/pptx-template/blob/master/README.md

1 output, static data in model
------------------------------
This example shows static data usage in the model.  The static data here that will be templated on pptx is "How are you?", "Hello!", and "XNDIEDNEF".  This example is just like that in pptx-template.

model.json::

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

::

    $ pptx-template --template template.pptx --model model.json --output output.json
    OR
    $ pptx-template-data-feeder --template template.pptx --model model.json --output output.json

data feeder! 1+ output, 1 dataset
---------------------------------
This example shows dynamic data usage in the model and extends from the first example in the pptx-template documentation.  The number of output in this case is the number of rows of data in data.csv.

data.csv::

    greeting1,greeting2,greeting3
    "How are you?","Hello","XNDIEDNEF"
    "Well, thanks", "Good Bye", "NVINOE"

model.json::

    {
        "slides": [
            {
                "hello": {
                    "en": [
                    "{{elem.greeting1}}",
                    "{{elem.greeting2}}"
                    ],
                    "ja": "{{elem.greeting3}}"
                }
            }
        ]
    }

::

    $ pptx-template-data-feeder --template template.pptx --model model.json --output "output{{:}}.pptx" --data data.csv

iterate through data & model.  csv data will always be converted to list of dicts.
so, here is the basic idea for the internals::

    from jinja2 import Template
    template = Template("model.json")
    for row in data:
        template.render(elem=row)

pptx-template-data-feeder will represent data.csv internally in Python as a list of dictionaries::

    data = [{'greeting1': 'How are you?", 'greeting2': 'Hello', 'greeting': 'XNDIEDNEF'}, ...]

By specifying the jinja template in the output, we are able to create separate output pptx files. If we had only wanted the first output, we could do --output "output{{0}}.pptx".


1 output, static data in model
------------------------------

This example replicates the second example from pptx-template.  Accomplishing static data is exactly like in pptx-template.

data.csv::

    Year,Sales,Cost,ROI
    1Q,90,45,0.5
    2Q,100,50,0.5
    3Q,60,20,0.33
    4Q,80,60,0.75

model.json (1)::

    {
        "slides": [
        {
            "data": {}
        }
        ]
    }

OR model.json (2)::

    {
        "slides": [
        {
            "data": {"file_name": "data.csv"}
        }
        ]
    }

OR model.json (3)::

    {
        "slides": [
        {
            "data": {"body": "Year,Sales,Cost,ROI\n1Q,90,45,0.5\n3Q,60,20,0.33\n4Q,80,60,0.75"}
        }
        ]
    }

::

    $ pptx-template --template template.pptx --model model.json --output output.pptx
    OR
    $ pptx-template-data-feeder --template template.pptx --model model.json --output output.pptx


data feeder! 1+ output, 1+ dataset
----------------------------------

This example accomplishes the same as above, in a slightly different way.  We cannot use model.json (1) above.  It cannot be templated.

data1.csv::

    Year,Sales,Cost,ROI
    1Q,90,45,0.5
    2Q,100,50,0.5
    3Q,60,20,0.33
    4Q,80,60,0.75

data2.csv::

    Year,Sales,Cost,ROI
    1Q,90,45,0.5
    2Q,100,50,0.5
    3Q,60,20,0.33
    4Q,80,60,0.75


In this example we will template from model.json (2).

model.json::

    {
        "slides": [
        {
            "data": {"file_name": "{{elem.dataset}}"}
        }
        ]
    }

datasets.csv::

    dataset
    data1.csv
    data2.csv

::

    $ pptx-template-data-feeder --template template.pptx --model model.json --output output{{:}}.pptx --data datasets.csv


Now, we will show how to use with with model.json (3).

model.json::

    {
        "slides": [
        {

            "data": {"body": "{{elem|join(',')}}\n{% for row in elem %}{{row|join(',')}}{% endfor %}"}
        }
        ]
    }

data.csv::

    i,Year,Sales,Cost,ROI
    0,1Q,90,45,0.5
    0,2Q,100,50,0.5
    0,3Q,60,20,0.33
    0,4Q,80,60,0.75
    1,1Q,90,45,0.5
    1,2Q,100,50,0.5
    1,3Q,60,20,0.33
    1,4Q,80,60,0.75

Internal representation of data.csv is::

    data = [
    [{'Year': 1Q, 'Sales': 90, 'Cost': 45, 'ROI': 0.5}, ...],
    [{'Year': 1Q, 'Sales': 90, 'Cost', 45, 'ROI': 0.5}, ...]
    ]

    from jinja2 import Template
    template = Template("model.json")
    for row in data:
        template.render(elem=row)

::

    $ pptx-template-data-feeder --template template.pptx --model model.json --output output{{:}}.pptx --data data.csv, --dataset-index i


