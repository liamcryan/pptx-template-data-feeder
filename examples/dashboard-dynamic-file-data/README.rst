===================================
dashboard-dynamic-file-data example
===================================

If you haven't looked at the dashboard example, please take a look there first.

This example shows how to various types of chart data, but this time with the goal of producing more than one pptx file (dynamic data).

This time we will focus on how to properly template model.json (using jinja templating style).  First let's define a csv file with all of the csv files that we expect to be templated.  This will look like::

    donut,clustered,bar,line,area
    donut-data.csv,clustered-bar-data.csv,100-bar-data.csv,line-data.csv,area-data.csv
    donut-data2.csv,clustered-bar-data2.csv,100-bar-data2.csv,line-data2.csv,area-data2.csv

Notice the headers of the csv file.  The 'donut' header specifies the associated donut-data files (donut-data.csv & donut-data2.csv).

We need to jinja template model.json so that the chart data will not be fixed (previously in last example was 'donut-data.csv', 'clustered-bar-data.csv', '100-bar-data.csv')::

    {"slides": {
        "0": {
                "donut": {
                    "file_type": "{{data.donut}}"
                },
                "clustered_bar": {
                    "file_type": "{{data.clustered}}"
                },
                "100_bar": {
                    "file_type": "{{data.bar}}"
                }
        },
        "1": {},
        "2": {}
      }
    }

The double brackets are standard jinja templating: https://jinja.palletsprojects.com/en/2.11.x/

Let's look at the first one:  {{data.donut}}.  'data' is a special variable available to the entire model.json.  It represents a row of data in the data.csv file.  The 'donut' is referring to the column name.  So, when we say '{{data.donut}}' what is really happening is in the first ppt output this will be replaced with donut-data.csv, and the second ppt output this will be replaced with donut-data2.csv.  This is how we are able to produce multiple pptx reports from dynamic data.

Other ways of assigning the data to the chart can be seen in the pptx-template documentation: https://github.com/m3dev/pptx-template. NOTE: the file (donut-data.csv, etc) are relative to where the script was called from (ie current working directory) - if you find the data isn't getting replaced it is probably because the data is not located in the same directory where the script was called.

In the terminal, cd to this directory, then::

    %pptx-templater --template in.pptx --model-template model.json --out out.pptx --data data.csv

Notice this time we needed to specify a --data data.csv.  There will be two output pptx files.  Instead of them both being named out.pptx, the index of enumeration will be appended (out0.pptx & out1.pptx).
