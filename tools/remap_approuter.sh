#!/bin/bash
echo XSA Remap AppRouter Starting

js_url="$(xs app python-js --urls)"
python_url="$(xs app python-python --urls)"

cmd="xs set-env python-web destinations '[{\"forwardAuthToken\":true,\"name\":\"js_be\",\"url\":\"$js_url\"},{\"forwardAuthToken\":true,\"name\":\"python_be\",\"url\":\"$python_url\"}]'"
echo $cmd
eval $cmd
echo ""

cmd="xs restage python-web"
echo $cmd
eval $cmd
echo ""

cmd="xs restart python-web"
echo $cmd
eval $cmd
echo ""

echo XSA Remap AppRouter Finished

exit 0
