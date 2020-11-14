=======================================
pptx-template-dynamic-file-data example
=======================================

If you haven't taken a look at the pptx-template example, please look there first.

The goal of this example (and pptx-templater) is to create multiple pptx output files based on feeding dynamic data to the same model and ppt.

The model.json file templates three files used by the ppt.  We are going to jinja template them.

We are going to include three of each of the .csv files (each file having different content, eg dynamic)::

    chart1.csv
    chart2.csv
    chart3.csv
    segment.csv
    segment2.csv
    segment3.csv
    xy.tsv
    xy2.tsv
    xy3.tsv

We need a way to pass the other files to the jinja template - our data.csv file::

    xy,segment,chart
    xy.tsv,segment.csv,chart1,csv
    xy2.tsv,segment2.csv,chart2.csv
    xy3.tsv,segment3.csv,chart3.csv

Here we configure the files appropriately in the csv file so that each row of data is passed to the jinja template.

In model.json, we make the appropriate changes::

    "2": {
      "bars": {
        "file_name": "{{data.chart}}",
        "value_axis_max": 150,
        "value_axis_min": 50
      }
    },
    "3": {
      "xy": {"file_name":  "{{data.xy}}"}
    },
    "pie": {
      "segment": {"file_name":  "{{data.segment}}"}
    },

The {{}} is standard jinja template stuff, and the variable within the brackets is our dynamic data.  The variable 'data' is global to the template.

What this means is that any data passed to the jinja template (aka the model.json file) will be accessible by {{data.something}}.  'something' in this case is our column name.

In the terminal, cd to this directory, then::

    %pptx-templater --template in.pptx --model-template model.json --out out.pptx --data data.csv

You will see three output pptx files.  They have been enumerated (instead of out.pptx, they are out0.pptx, out1.pptx, out2.pptx).
