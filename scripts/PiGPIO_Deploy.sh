#! /bin/bash

sudo /greengrass/v2/bin/greengrass-cli deployment create \
--recipeDir ~/Documents/gaudanon-starter-project/recipes \
--artifactDir ~/Documents/gaudanon-starter-project/artifacts \
--merge "com.gaudanon.PiGPIO=1.0.1"
