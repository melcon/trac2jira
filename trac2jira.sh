#!/bin/sh

python ./comments.py

(echo 'ticket$type$component$version$created$_changetime$summary$description$priority$_reporter$resolution$status$keywords'; python ./export.py | iconv -f utf8 -t koi8-r) > /tmp/issues
