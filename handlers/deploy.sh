#!/bin/bash

# usage: ./deploy.sh <FILE_NAME> <FUNCTION_NAME>
# example: ./deploy.sh scraper.py dbmScraper

paplay /usr/share/sounds/freedesktop/stereo/complete.oga

# 1. Setup variables
FILE_NAME=$1
FUNCTION_NAME=$2

ZIP_FILE="$FUNCTION_NAME.zip"
BUILD_DIR="build_temp"
BUCKET_NAME="dbm-nca-ph-lambda-deployments"

echo "=========================================="
echo "  Deploying $FOLDER_NAME to $FUNCTION_NAME"
echo "=========================================="

# 2. Prepare a clean build directory
rm -rf $BUILD_DIR $ZIP_FILE
mkdir $BUILD_DIR

# 3. Copy ONLY necessary source code (Prevents copying venv/.git)
echo "Copying source code..."
cp -r "../src" $BUILD_DIR/
cp $FILE_NAME $BUILD_DIR/lambda_function.py
cp "${FUNCTION_NAME}_requirements.txt" $BUILD_DIR/

# 4. Install dependencies
echo "Installing dependencies..."
pip install \
    --target $BUILD_DIR \
    -r ${FUNCTION_NAME}_requirements.txt  \
    --upgrade \
    --quiet

# 5. Clean up garbage files (Crucial for size)
echo "Cleaning up garbage..."
find $BUILD_DIR -type d -name "__pycache__" -exec rm -rf {} +
find $BUILD_DIR -type d -name "*.dist-info" -exec rm -rf {} +
find $BUILD_DIR -type d -name "tests" -exec rm -rf {} +
rm -rf $BUILD_DIR/boto3 $BUILD_DIR/botocore

# 6. Zip the package
echo "Zipping package..."
cd $BUILD_DIR
zip -r -q ../$ZIP_FILE .
cd ..

# 7. Upload to S3
echo "Uploading to ${ZIP_FILE} AWS S3..."
aws s3 cp $ZIP_FILE s3://$BUCKET_NAME \
    --profile dbm-dev \
    --region ap-southeast-1 \
    --cli-connect-timeout 900 \

# 8. Upload to AWS
echo "Updating AWS Lambda function..."
aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --s3-bucket $BUCKET_NAME \
    --s3-key $ZIP_FILE \
    --profile dbm-dev \

# 8. Clean up
rm -rf $BUILD_DIR $ZIP_FILE
echo "✅ Deployment Complete: $FUNCTION_NAME"

paplay /usr/share/sounds/freedesktop/stereo/complete.oga
