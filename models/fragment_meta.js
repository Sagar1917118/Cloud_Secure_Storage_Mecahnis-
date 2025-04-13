// models/FragmentMeta.js
const mongoose = require("mongoose");

const FragmentMetaSchema = new mongoose.Schema({
  originalName: { type: String, required: true },
  uploadedAt: { type: Date, default: Date.now },
  fragmentsCount: { type: Number, required: true },
  fragmentKeys: [{ type: String }],
  userId: { type: String, required: true }
});

module.exports = mongoose.model("FragmentMeta", FragmentMetaSchema);
