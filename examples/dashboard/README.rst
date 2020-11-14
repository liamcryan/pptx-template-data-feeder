=================
dashboard example
=================

This example shows how to various types of chart data (static data - no extra templating).

Notice the {id:0}, {id:0}, {id:2} on each slide in template.pptx.  This tells pptx-template that there is some templating to be done and model.json will specify what to do::

    {
      "slides": {
        "0": {},
        "1": {},
        "2": {}
      }
    }

Notice the titles of the charts.  There is a {donut}, {clustered_bar}, and {100_bar}.  We put this here because it tells pptx-template that we are going to replace some chart data here.  In model.json, here is how we do this::

    {"slides": {
        "0": {
                "donut": {},
                "clustered_bar": {},
                "100_bar": {}
        },
        "1": {},
        "2": {}
      }
    }

There are a few ways to define the data appropriately in model.json.  This example shows how to do so with csv files::

    {"slides": {
        "0": {
                "donut": {
                    "file_type": "donut-data.csv"
                },
                "clustered_bar": {
                    "file_type": "clustered-bar-data.csv"
                },
                "100_bar": {
                    "file_type": "100-bar-data.csv"
                }
        },
        "1": {},
        "2": {}
      }
    }

Other ways of assigning the data to the chart can be seen in the pptx-template documentation: https://github.com/m3dev/pptx-template. NOTE: the file (donut-data.csv, etc) are relative to where the script was called from (ie current working directory) - if you find the data isn't getting replaced it is probably because the data is not located in the same directory where the script was called.

In the terminal, cd to this directory, then::

    %pptx-templater --template in.pptx --model-template model.json --out out.pptx

Note you could have used pptx-template instead::

    %pptx-template --template in.pptx --model model.json --out out.pptx

This example does not use any of the jinja templating abilities and creates one output just as pptx-template does.  For a templated version of this example see pptx-template-jinja.
