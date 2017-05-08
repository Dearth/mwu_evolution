#!/bin/bash

tar xvzf look-example.tar.gz

./n-prog -d $PWD/look-example -r $PWD/look-example/repair -n 2500 -k 2 -x 6000
