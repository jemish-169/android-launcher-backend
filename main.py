from fastapi import BackgroundTasks, FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from generator.builder import AndroidProjectBuilder
import json, os
from fastapi.middleware.cors import CORSMiddleware
from models.config_model import ProjectConfig
from pydantic import ValidationError

app = FastAPI(title="Android Project Generator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_android_project(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """
    Generate Android project ZIP from JSON configuration
    """
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="File must be a JSON file")
    
    try:
        # Read JSON configuration
        content = await file.read()
        config_dict = json.loads(content.decode('utf-8'))
        
        config = ProjectConfig(**config_dict)
        
        # Generate project
        builder = AndroidProjectBuilder(config)
        zip_path = builder.build()
        
        # Return ZIP file as streaming response
        def iter_file():
            with open(zip_path, mode="rb") as file_like:
                yield from file_like
        
        # Clean up temp file after response
        background_tasks.add_task(os.remove, zip_path)

        return StreamingResponse(
            iter_file(),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={config.project.name}.zip"},
            background=background_tasks
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error generating project: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Android Project Generator is running"}

@app.get("/")
async def health_check():
    return {"status": "healthy", "message": "Android Project Generator is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.51.207", port=8000, reload=True)