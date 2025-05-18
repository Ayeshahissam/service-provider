from fastapi import FastAPI, HTTPException, Body, Form, Request, Depends, Cookie, Response, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import bcrypt
import uvicorn
import logging
import db
from typing import Optional
import shutil


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    username: str
    password: str

class SignUpFreelancers(BaseModel):
    serviceType: str
    fullname: str
    username: str
    email: str
    hourlyrate: int
    password: str
    confirmPassword: str

class Booking(BaseModel):
    providerName: str
    providerUsername : str
    customerName: str
    customerEmail: str
    customerPhone: str
    serviceDate: str
    serviceTime: str
    additionalNotes: str = None

class ContactQuery(BaseModel):
    name: str
    email: str
    contact_no: str
    message: str

class Admin(BaseModel):
    username: str
    password: str

def get_current_user(admin_token: Optional[str] = Cookie(None)):
    if not admin_token or admin_token != "admin-token":
        raise HTTPException(status_code=403, detail="Not authenticated")
    return "admin"

def get_authenticated_user(user_token: Optional[str] = Cookie(None)):
    if not user_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_token

@app.get('/homepage', response_class= HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("homepage.html", {"request" : request})

@app.get('/homeservices', response_class= HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("homeservices.html", {"request" : request})

@app.get('/automotiveservices', response_class= HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("automotiveservices.html", {"request" : request})

@app.get('/personalservices', response_class= HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("personalservices.html", {"request" : request})

@app.get('/aboutus', response_class= HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("aboutus.html", {"request" : request})

@app.get('/contactus', response_class= HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("contactus.html", {"request" : request})


@app.get('/carwash', response_class=HTMLResponse)
async def carwash(request: Request):
    freelancers = await db.get_freelancers_by_service("carwash")
    print(freelancers)  # Log the freelancers data
    return templates.TemplateResponse("car_wash.html", {"request": request, "freelancers": freelancers})

@app.get('/test_get_freelancers')
async def test_get_freelancers():
    freelancers = await db.get_freelancers_by_service("carwash")
    return {"freelancers": freelancers}


@app.get('/carrepair', response_class= HTMLResponse)
async def carrepair(request: Request):
    freelancers = await db.get_freelancers_by_service("mechanic")
    print(freelancers)  # Log the freelancers data
    return templates.TemplateResponse("mechanic.html", {"request": request, "freelancers": freelancers})

@app.get('/makeup', response_class= HTMLResponse)
async def makeup(request: Request):
    freelancers = await db.get_freelancers_by_service("makeup")
    print(freelancers)  # Log the freelancers data
    return templates.TemplateResponse("makeup.html", {"request": request, "freelancers": freelancers})

@app.get('/oilchange', response_class= HTMLResponse)
async def oilchange(request: Request):
    freelancers = await db.get_freelancers_by_service("oilchange")
    print(freelancers)  # Log the freelancers data
    return templates.TemplateResponse("oil_change.html", {"request": request, "freelancers": freelancers})

@app.get('/personaltraining', response_class= HTMLResponse)
async def carrepair(request: Request):
    freelancers = await db.get_freelancers_by_service("trainer")
    print(freelancers)  # Log the freelancers data
    return templates.TemplateResponse("personal_training.html", {"request": request, "freelancers": freelancers})

@app.get('/plumbing', response_class= HTMLResponse)
async def plumbing(request: Request):
    freelancers = await db.get_freelancers_by_service("plumbing")
    print(freelancers)  # Log the freelancers data
    return templates.TemplateResponse("plumbing.html", {"request": request, "freelancers": freelancers})

@app.get('/tutor', response_class= HTMLResponse)
async def carrepair(request: Request):
    freelancers = await db.get_freelancers_by_service("tutor")
    print(freelancers)  # Log the freelancers data
    return templates.TemplateResponse("tutor.html", {"request": request, "freelancers": freelancers})

@app.get('/lawncare', response_class= HTMLResponse)
async def carrepair(request: Request):
    freelancers = await db.get_freelancers_by_service("lawncare")
    print(freelancers)  # Log the freelancers data
    return templates.TemplateResponse("lawn_care.html", {"request": request, "freelancers": freelancers})

@app.get('/electrician', response_class= HTMLResponse)
async def electrician(request: Request):
    freelancers = await db.get_freelancers_by_service("electrician")
    print(freelancers)  # Log the freelancers data
    return templates.TemplateResponse("electrician.html", {"request": request, "freelancers": freelancers})

@app.get('/freelancerDashboard', response_class= HTMLResponse)
async def index(request: Request, user_token: str = Depends(get_authenticated_user)):
    user = await db.get_one(user_token)  # Assuming the token is the username
    return templates.TemplateResponse("freelancer.html", {"request" : request, "user": user})

@app.post("/contactus")
async def submit_contact_query(data: ContactQuery):
    id = await db.create_contact_query(data)
    return {"success": True, "inserted_id": id}

@app.get("/admin/login", response_class=HTMLResponse)
async def get_admin_login(request: Request):
    logger.info("Admin login page accessed")
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/logout")
async def admin_logout(response: Response):
    response.delete_cookie("admin_token")
    return {"status": "success"}

@app.post("/admin/login", response_class=HTMLResponse)
async def admin_login(username: str = Form(...), password: str = Form(...)):
    logger.info(f"Admin login attempt for user: {username}")
    if await db.validate_admin(username, password):
        logger.info("Admin login successful")
        response = HTMLResponse(content="""
        <html>
            <body>
                <script>
                    alert('Admin login successful');
                    window.location.href = '/admin/dashboard';
                </script>
            </body>
        </html>
        """)
        response.set_cookie(key="admin_token", value="admin-token", httponly=True)
        return response
    else:
        logger.warning("Invalid admin credentials")
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie("user_token")
    return {"status": "success"}

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, current_user: str = Depends(get_current_user)):
    try:
        freelancers = await db.all_freelancers()
        bookings = await db.all_bookings()
        queries = await db.all_queries()
        logger.info(f"Freelancers: {freelancers}")
        logger.info(f"Bookings: {bookings}")
        return templates.TemplateResponse("admin_dashboard.html", {"request": request, "freelancers": freelancers, "bookings": bookings, "queries": queries})
    except Exception as e:
        logger.error(f"Error loading admin dashboard: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/freelancersignup", response_class=HTMLResponse)
async def get_signup_page(request: Request):
    logger.info("Signup page accessed")
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup(
    serviceType: str = Form(...),
    fullname: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    hourlyrate: int = Form(...),
    password: str = Form(...),
    confirmPassword: str = Form(...),
    profileImage: UploadFile = File(...)
):
    if password != confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing_user = await db.get_one(username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Save the image to the static/images directory
    image_path = f"images/{profileImage.filename}"
    with open(f"static/{image_path}", "wb") as image_file:
        shutil.copyfileobj(profileImage.file, image_file)

    # Save the relative image path in the database
    id = await db.create({
        "serviceType": serviceType,
        "fullname": fullname,
        "username": username,
        "email": email,
        "hourlyrate": hourlyrate,
        "password": hashed_password.decode('utf-8'),
        "profileImage": image_path
    })
    return {"inserted": True, "inserted_id": id}

@app.post("/login")
async def login(data: User, response: Response):
    user = await db.get_one(data.username)
    if user and bcrypt.checkpw(data.password.encode('utf-8'), user['password'].encode('utf-8')):
        response.set_cookie(
            key="user_token",
            value=data.username,
            httponly=True,
            max_age=30*24*60*60  # 30 days in seconds
        )
        return {"status": "success", "user": user}
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")

@app.post("/book")
async def book_service(data: Booking):
    id = await db.create_booking(data)
    await db.create_notification({
        "providerUsername": data.providerUsername,
        "details": {
            "providerName": data.providerName,
            "customerName": data.customerName,
            "customerEmail": data.customerEmail,
            "customerPhone": data.customerPhone,
            "serviceDate": data.serviceDate,
            "serviceTime": data.serviceTime,
            "additionalNotes": data.additionalNotes
        }
    })
    return {"success": True, "inserted_id": id}

@app.get("/notifications")
async def get_notifications(username: str):
    notifications = await db.get_notifications(username)
    return notifications


@app.delete("/delete")
async def delete_user(user: User = Body(...)):
    valid_user = await db.validate_user(user.username, user.password)
    if not valid_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    deleted_count = await db.delete(user.username)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"delete": True}

@app.post("/admin/delete_freelancer/{username}")
async def admin_delete_freelancer(username: str, method_override: str = Form(...), current_user: str = Depends(get_current_user)):
    if method_override != "DELETE":
        raise HTTPException(status_code=405, detail="Method Not Allowed")
    deleted_count = await db.delete(username)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Freelancer not found")
    return {"delete": True}

@app.post("/admin/delete_booking/{id}")
async def admin_delete_booking(id: str, method_override: str = Form(...), current_user: str = Depends(get_current_user)):
    if method_override != "DELETE":
        raise HTTPException(status_code=405, detail="Method Not Allowed")
    deleted_count = await db.delete_booking(id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"delete": True}

@app.post("/admin/delete_query/{id}")
async def admin_delete_query(id: str, method_override: str = Form(...), current_user: str = Depends(get_current_user)):
    if method_override != "DELETE":
        raise HTTPException(status_code=405, detail="Method Not Allowed")
    deleted_count = await db.delete_query(id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Query not found")
    return {"delete": True}


@app.post("/admin.update_freelancer/{username}")
async def admin_update_freelancer(username: str, fullname: Optional[str] = Form(None), serviceType: Optional[str] = Form(None), email: Optional[str] = Form(None), hourlyrate: Optional[int] = Form(None), method_override: str = Form(...), current_user: str = Depends(get_current_user)):
    if method_override != "PUT":
        raise HTTPException(status_code=405, detail="Method Not Allowed")
    
    update_data = {}
    if fullname is not None:
        update_data['fullname'] = fullname
    if serviceType is not None:
        update_data['serviceType'] = serviceType
    if email is not None:
        update_data['email'] = email
    if hourlyrate is not None:
        update_data['hourlyrate'] = hourlyrate
    
    updated_count = await db.update(username, update_data)
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Freelancer not found")
    return update_data

@app.post("/admin.update_booking/{id}")
async def admin_update_booking(id: str, providerName: Optional[str] = Form(None), customerName: Optional[str] = Form(None), customerEmail: Optional[str] = Form(None), customerPhone: Optional[str] = Form(None), serviceDate: Optional[str] = Form(None), serviceTime: Optional[str] = Form(None), additionalNotes: Optional[str] = Form(None), method_override: str = Form(...), current_user: str = Depends(get_current_user)):
    if method_override != "PUT":
        raise HTTPException(status_code=405, detail="Method Not Allowed")
    
    update_data = {}
    if providerName is not None:
        update_data['providerName'] = providerName
    if customerName is not None:
        update_data['customerName'] = customerName
    if customerEmail is not None:
        update_data['customerEmail'] = customerEmail
    if customerPhone is not None:
        update_data['customerPhone'] = customerPhone
    if serviceDate is not None:
        update_data['serviceDate'] = serviceDate
    if serviceTime is not None:
        update_data['serviceTime'] = serviceTime
    if additionalNotes is not None:
        update_data['additionalNotes'] = additionalNotes
    
    updated_count = await db.update_booking(id, update_data)
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
    return update_data
