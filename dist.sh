#!/bin/bash

SRCDIR=`pwd`
TMPDIR=`mktemp -d`

# Clean build of angular app
cd frontend
rm -rf dist
ng build --prod --aot
cd ..
cp -ax . $TMPDIR/commitstop

# Delete unnecessary files
mv $TMPDIR/commitstop/frontend/dist $TMPDIR/
rm -rf $TMPDIR/commitstop/.git $TMPDIR/commitstop/dist.sh $TMPDIR/commitstop/frontend
rm `find $TMPDIR -name *.pyc`
mv $TMPDIR/dist $TMPDIR/commitstop/frontend

# adjust relativ path because path is just "frontend" in distribution instead of "frontend/dist" 
export JS_FILE=`ls $TMPDIR/commitstop/frontend/main-es2015.*`
sed "s|\.\./\.\./api.py|../api.py|" < $JS_FILE > $TMPDIR/t.txt
mv $TMPDIR/t.txt $JS_FILE

export JS_FILE=`ls $TMPDIR/commitstop/frontend/main-es5.*`
sed "s|\.\./\.\./api.py|../api.py|" < $JS_FILE > $TMPDIR/t.txt
mv $TMPDIR/t.txt $JS_FILE

# Create .zip-file
cd $TMPDIR
mkdir $SRCDIR/dist
zip -r $SRCDIR/dist/commitstop-$1.zip *
cd $SRCDIR
rm -rf $TMPDIR
