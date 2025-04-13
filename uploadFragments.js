const fs = require("fs");
const path = require("path");
const { S3Client, PutObjectCommand } = require("@aws-sdk/client-s3");
require("dotenv").config();

const s3 = new S3Client({
  region: "ap-south-1",
  credentials: {
    accessKeyId: process.env.ACCESS_ID,
    secretAccessKey: process.env.SECRET_ACCESS_KEY,
  },
});

const bucketName = process.env.BUCKET_NAME;

async function uploadEncodedFragments(buffersArray) {
  const timestamp = Date.now();
  const publicUrls = [];

  for (let i = 0; i < buffersArray.length; i++) {
    const buffer = buffersArray[i];

    // Convert Uint8Array to Buffer before uploading
    const binBuffer = Buffer.from(buffer);

    const key = `fragments/fragment_${i}_${timestamp}.bin`;

    const command = new PutObjectCommand({
      Bucket: bucketName,
      Key: key,
      Body: binBuffer,
      ContentType: "application/octet-stream", // better for binary files
    });

    await s3.send(command);
    const url = `https://${bucketName}.s3.ap-south-1.amazonaws.com/${key}`;
    publicUrls.push(url);
    console.log(`✅ Uploaded fragment ${i} to: ${url}`);
  }

  return publicUrls;
}

module.exports = {uploadEncodedFragments};
