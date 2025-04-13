const { streamToBuffer } = require("./utils"); // helper function shown below
const bucketName = process.env.BUCKET_NAME;
const { S3Client, GetObjectCommand } = require("@aws-sdk/client-s3");
require("dotenv").config();

const s3 = new S3Client({
  region: "ap-south-1",
  credentials: {
    accessKeyId: process.env.ACCESS_ID,
    secretAccessKey: process.env.SECRET_ACCESS_KEY,
  },
});
async function downloadEncodedFragments(keys) {
    try{
    const reconstructedArrays = [];

    for (const key of keys) {
        try {
          const command = new GetObjectCommand({
            Bucket: bucketName,
            Key: key,
          });
      
          const response = await s3.send(command);
          const buffer = await streamToBuffer(response.Body); // stream -> Buffer
          const uint8Array = new Uint8Array(buffer); // convert to original format
          reconstructedArrays.push(Array.from(uint8Array));
      
        } catch (err) {
          // Silently skip this key if there's any error (like missing key)
          continue;
        }
      }
    return reconstructedArrays;
    }catch(err){
        return [];
    }
}
module.exports={downloadEncodedFragments}