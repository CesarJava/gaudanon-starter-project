#! /bin/bash

sudo /greengrass/v2/bin/greengrass-cli deployment create \
--recipeDir ~/Documents/GreengrassCore/recipes \
--artifactDir ~/Documents/GreengrassCore/artifacts \
--merge "com.gaudanon.Blinky=1.0.0"
