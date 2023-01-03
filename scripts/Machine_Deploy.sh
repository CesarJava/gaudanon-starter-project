#! /bin/bash

aws s3 sync . s3://gaudanon-bucket

sudo /greengrass/v2/bin/greengrass-cli deployment create \
--recipeDir ~/Documents/gaudanon-starter-project/recipes \
--artifactDir ~/Documents/gaudanon-starter-project/artifacts \
--remove "com.gaudanon.Machine"

sudo /greengrass/v2/bin/greengrass-cli deployment create \
--recipeDir ~/Documents/gaudanon-starter-project/recipes \
--artifactDir ~/Documents/gaudanon-starter-project/artifacts \
--merge "com.gaudanon.Machine=1.0.1"
