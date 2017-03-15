#!/bin/sh

# "piggyback" on the existing tox environment
DEVPI="$TRAVIS_BUILD_DIR/application/.tox/py35/bin/devpi"

if [ "$TRAVIS_BRANCH" = "master" ] && [ "$TRAVIS_PULL_REQUEST" = "false" ] ; then
    $DEVPI use "https://pypi.senic.com/${TRAVIS_REPO_SLUG%/*}/master"
    $DEVPI login $devpi_user --password="$devpi_password"
    $DEVPI upload --no-vcs --with-docs --formats bdist_wheel
else
    echo "Not building for branch '$TRAVIS_BRANCH'"
fi