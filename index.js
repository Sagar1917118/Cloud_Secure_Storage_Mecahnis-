const express = require("express");
const multer = require("multer");
const fs = require("fs");
const path = require("path");
const axios = require("axios");

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
const upload = multer({ dest: "uploads/" });
const {uploadEncodedFragments}=require("./uploadFragments");
const {downloadEncodedFragments}=require("./downloadFragments");
const {connectDB}=require("./database_config");

// controller function to stroed file metadata in database
const FragmentMeta = require("./models/fragment_meta");
const saveToDB = async (originalName, urls, userId) => {
    try {
      console.log("Saving to DB with:", { originalName, urls, userId });
  
      const fragmentData = new FragmentMeta({
        originalName,
        uploadedAt: new Date(),
        fragmentsCount: urls.length,
        fragmentKeys: urls,
        userId
      });
  
      const dbResponse = await fragmentData.save();
      console.log("Metadata saved to DB:", dbResponse);
      return dbResponse;
  
    } catch (err) {
      console.error("Error in saving file metadata to database:", err.message);
      return null;
    }
  };
// ---------------------------------------------------------
app.post("/upload-file", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ message: "No file uploaded" });
    }

    const filePath = req.file.path;
    const originalName = req.file.originalname;
    // Read and convert buffer to string
    const buffer = fs.readFileSync(filePath);
    const textContent = buffer.toString("base64"); // Or 'ascii' if needed
    // Send to Flask server
    const response = await axios.post("http://127.0.0.1:5000/encode", {
      text: textContent,
    });
    const encoded_fragments=response?.data?.encoded_fragments
    console.log(encoded_fragments);
    const uploadingResponse = await uploadEncodedFragments(encoded_fragments); 
    // console.log("Uploaded URLs/keys:", uploadingResponse);

    // Extract keys if you received full URLs
    const keys = uploadingResponse.map(url => url.split(".com/")[1]);
    // store the keys in the database
    const dbResponse=await saveToDB(originalName,keys,"sagar123");
    console.log("Retured Object Id",dbResponse?._id);
    fs.unlinkSync(filePath);
    return res.json({dbResponse});
  } catch (err) {
    console.error(" Upload failed:", err.message);
    res.status(500).json({ message: "Internal server error" });
  }
});
// code to fetch donloaded documents
app.post("/download-file",async (req,res)=>{
    try{
        const {file_id}=req.body;
        const fileObj=await FragmentMeta.findById(file_id);
        console.log(fileObj);
        if(!fileObj)
            return res.status(400).json({message:"file is not available"});
        const keys=fileObj?.fragmentKeys;
        const downloadedResponse = await downloadEncodedFragments(keys);
        console.log(downloadedResponse)
        if(!downloadedResponse||downloadedResponse.length<3)
                return res.status(400).json({
                message:"Meta Data of file is not avialable"
        })
        const response=await getDecodedmaterial(downloadedResponse);
        if(!response){
                return res.status(400).json({
             message:"Error in downloading file"});
                }
        return res.status(200).json({message:response?.message})
    }
    catch(err){
        console.log("Error in downloading data",err.message)
        return res.status(500).json({
            success:false,
            message:err.message,
        })
    }
})
// code to decode the binary encoding
// app.post("/decode-file",async (req,res)=>
async function getDecodedmaterial(encoded_fragments)  {
    try{
    const decodedResponse=await axios.post("http://127.0.0.1:5000/decode",{
        fragments:encoded_fragments
    });
   const decodedData = (decodedResponse?.data?.recovered).toString();
   const cleaned = decodedData.replace(/[\x00-\x1F\x7F]/g, ''); 

        fs.writeFile('output.txt', cleaned, 'utf8', (err) => {
            if(err){
                console.log(err.message);
                return NULL;
            }
            else
                console.log("File downloaded successfully");
        })
        return {message:"File saved as output.txt and should be readable!"};
    }catch(err){
       console.log("Error in geeting data for donwloading file",err.message);
       return NULL;
    }   
}
// )
connectDB();
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Node.js server running at http://localhost:${PORT}`);
});
