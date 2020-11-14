=====================
pptx-template example
=====================

This example shows how to replicate (with pptx-templater), the output from the pptx-template test here: https://github.com/m3dev/pptx-template/tree/master/test/data

In the terminal, cd to this directory, then::

    %pptx-templater --template in.pptx --model-template model.json --out out.pptx

Note you could have used pptx-template instead::

    %pptx-template --template in.pptx --model model.json --out out.pptx


This example does not use any of the jinja templating abilities and creates one output just as pptx-template does.  For a templated version of this example see pptx-template-jinja.
