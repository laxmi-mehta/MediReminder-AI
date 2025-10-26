function OCRUpload() {
    return (
      <div>
        <h2 className="text-xl font-semibold mb-4">OCR Upload</h2>
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-600">Upload prescription images to extract medication information</p>
          <div className="mt-4 border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
            <p className="text-gray-500">Drop files here or click to upload</p>
          </div>
        </div>
      </div>
    );
  }
  
  export default OCRUpload;