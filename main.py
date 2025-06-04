from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from generator.builder import AndroidProjectBuilder
import json
import os
from starlette.background import BackgroundTask
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Android Project Generator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_android_project(file: UploadFile = File(...)):
    """
    Generate Android project ZIP from JSON configuration
    """
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="File must be a JSON file")
    
    try:
        # Read JSON configuration
        content = await file.read()
        config = json.loads(content.decode('utf-8'))
        
        # Validate required fields
        if not config.get('project', {}).get('name'):
            raise HTTPException(status_code=400, detail="Project name is required")
        if not config.get('project', {}).get('package'):
            raise HTTPException(status_code=400, detail="Project package is required")
        
        # Generate project
        builder = AndroidProjectBuilder(config)
        zip_path = builder.build()
        
        # Return ZIP file as streaming response
        def iter_file():
            with open(zip_path, mode="rb") as file_like:
                yield from file_like
        
        # Clean up temp file after response
        def cleanup():
            if os.path.exists(zip_path):
                os.remove(zip_path)
        
        project_name = config['project']['name']
        return StreamingResponse(
            iter_file(),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={project_name}.zip"},
            background=BackgroundTask(cleanup)
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating project: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Android Project Generator is running"}

@app.get("/")
async def health_check():
    return {"status": "healthy", "message": "Android Project Generator is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.0.90", port=8000, reload=True)