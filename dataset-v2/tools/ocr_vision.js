// OCR an image with the built-in macOS Vision framework (verification only; nothing to install).
// Usage: osascript -l JavaScript ocr_vision.js <image.png>
ObjC.import('Vision');
function run(argv) {
  const req = $.VNRecognizeTextRequest.alloc.init;
  req.recognitionLevel = 0;            // accurate
  req.usesLanguageCorrection = false;
  const h = $.VNImageRequestHandler.alloc.initWithURLOptions($.NSURL.fileURLWithPath(argv[0]), $.NSDictionary.dictionary);
  h.performRequestsError($.NSArray.arrayWithObject(req), null);
  const out = [], res = req.results;
  for (let i = 0; i < res.count; i++) out.push(res.objectAtIndex(i).topCandidates(1).objectAtIndex(0).string.js);
  return out.join('\n');
}
