===========================
pptx-template-jinja example
===========================

The goal of this example (and pptx-templater) is to create multiple pptx output files based on feeding dynamic data to the same model and ppt.

The model.json file templates three files used by the ppt.  We are going to jinja template them.  See model.json for details how.

In the terminal type::

    %pptx-templater --template in.pptx --model-template model.json --out out.pptx --data data.csv

Note you could have used pptx-template instead::

    %pptx-template --template in.pptx --model model.json --out out.pptx

This example does not use any of the jinja templating abilities and creates one output just as pptx-template does.  For a templated version of this example see pptx-template-jinja.
