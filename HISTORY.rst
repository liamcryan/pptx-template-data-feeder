HISTORY
-------

2/10/2021
+++++++++

* let user specify dynamic output file naming

Previously filenames were enumerated by index::

    outputfile1.pptx
    outputfile2.pptx
    ...

Now you can specify in the --out option::

    % pptx-templater --out outputfile-{{name}}.pptx

Where name is a column in your input data csv file::

    [{"name": "George"}, {"name": "Martha"}]

Files will look like::

    outputfile-George.pptx
    outputfile-Martha.pptx

