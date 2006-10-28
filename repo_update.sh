#!/bin/sh

REPO_ROOT=$1
JIRA_KEY=$2
test -z "$REPO_ROOT" -o -z "$JIRA_KEY" && (echo "Usage: $0 repo_path jira_key\n$0 /home/svn/project PRJ"; exit)

HEAD_REV=`svn info file://$REPO_ROOT | grep 'Last Changed Rev' | cut -d':' -f2`

TMP_DIR=`mktemp`
mkdir $TMP_DIR
cd $TMP_DIR
for i in `seq 1 $HEAD_REV`; do svn propget svn:log --revprop -r$i file://$REPO_ROOT > $TMP_DIR/$i; done
for i in `ls`; do cat $i | sed "s/#/$JIRA_KEY-/g" > $i.new; mv $i.new $i; done
for i in `ls`; do test -z "`grep $JIRA_KEY- $i`" && (echo "$i"; rm $i); done
for i in `ls`; do sudo svnadmin setlog $REPO_ROOT --bypass-hooks -r$i $TMP_DIR/$i; done 
