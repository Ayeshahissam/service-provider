import motor.motor_asyncio
import bcrypt
import random
from bson import ObjectId

mongoURI = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(mongoURI)

db = client["Website"]
freelancer_collection = db["Freelancers"]
booking_collection = db["Customers"]
admin_collection = db["Admins"]
query_collection = db["Queries"]
notification_collection = db["Notifications"]


async def create(data):
    data = dict(data)
    response = await freelancer_collection.insert_one(data)
    return str(response.inserted_id)

async def create_booking(data):
    data = dict(data)
    response = await booking_collection.insert_one(data)
    return str(response.inserted_id)

async def create_contact_query(data):
    data = dict(data)
    response = await query_collection.insert_one(data)
    return str(response.inserted_id)

async def create_notification(data):
    response = await notification_collection.insert_one(data)
    return str(response.inserted_id)

async def get_notifications(username):
    response = notification_collection.find({"providerUsername": username})
    data = []
    async for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return data


async def all_freelancers():
    response = freelancer_collection.find({})
    data = []
    async for i in response:
        i["_id"] = str(i["_id"])
        if 'password' in i:
            del i['password']
        data.append(i)
    return data

async def all_bookings():
    response = booking_collection.find({})
    data = []
    async for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return data

async def all_queries():
    response = query_collection.find({})
    data = []
    async for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return data

async def get_one(username):
    response = await freelancer_collection.find_one({"username": username})
    if response:
        response["_id"] = str(response["_id"])
        return response
    else:
        return None

async def update(username, data):
    data = dict(data)
    response = await freelancer_collection.update_one({"username": username}, {"$set": data})
    return response.modified_count

async def delete(username):
    response = await freelancer_collection.delete_one({"username": username})
    return response.deleted_count

async def delete_query(id):
    response = await query_collection.delete_one({"_id": ObjectId(id)})
    return response.deleted_count

async def validate_user(username, password):
    user = await freelancer_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return True
    return False

async def update_booking(id, data):
    data = dict(data)
    response = await booking_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return response.modified_count

async def delete_booking(id):
    response = await booking_collection.delete_one({"_id": ObjectId(id)})
    return response.deleted_count

# Admin functions
async def create_admin(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    admin = {"username": username, "password": hashed_password.decode('utf-8')}
    response = await admin_collection.insert_one(admin)
    return str(response.inserted_id)

async def get_admin(username):
    response = await admin_collection.find_one({"username": username})
    if response:
        response["_id"] = str(response["_id"])
        return response
    else:
        return None

async def validate_admin(username, password):
    admin = await get_admin(username)
    if admin and bcrypt.checkpw(password.encode('utf-8'), admin['password'].encode('utf-8')):
        return True
    return False

async def get_freelancers_by_service(service_type: str):
    response = freelancer_collection.find({"serviceType": service_type})
    data = []
    carWashHeadings = [
    "Car Wash Expert",
    "Car Wash Specialist",
    "Car Wash Professional",
    "Car Wash Technician",
    "Car Wash Master"
] 

    carWashDescriptions = [
    "I am an expert in car wash services, ensuring your vehicle looks spotless and shiny.",
    "As a specialist in car wash services, I provide exceptional care tailored to your needs.",
    "With my professional car wash services, I guarantee a thorough and efficient clean every time.",
    "As a dedicated technician, I ensure your car receives top-quality wash and care.",
    "I am a master in car wash services, committed to making your vehicle shine like new."
] 

    mechanicHeadings = [
    "Mechanic Expert",
    "Auto Repair Specialist",
    "Vehicle Repair Professional",
    "Car Maintenance Technician",
    "Automotive Repair Master"
] 

    mechanicDescriptions = [
    "I am an expert mechanic dedicated to keeping your vehicle running smoothly.",
    "As an auto repair specialist, I offer comprehensive services for all vehicle types.",
    "With my professional repair services, I ensure your vehicle gets reliable and efficient repairs.",
    "As a car maintenance technician, I provide top-quality service to keep your car in top condition.",
    "I am a master in automotive repair, committed to delivering the best care for your vehicle."
] 

    lawnCareHeadings = [
    "Lawn Care Expert",
    "Gardening Specialist",
    "Lawn Maintenance Professional",
    "Lawn Care Technician",
    "Lawn Care Master"
] 

    lawnCareDescriptions = [
    "I am an expert in lawn care, dedicated to transforming your lawn into a beautiful space.",
    "As a gardening specialist, I offer comprehensive lawn maintenance solutions.",
    "With my professional lawn care services, I ensure a healthy and lush lawn all year round.",
    "As a lawn care technician, I provide top-quality care to keep your lawn well-maintained.",
    "I am a master in lawn care, committed to creating stunning outdoor spaces for you to enjoy."
] 

    makeupHeadings = [
    "Makeup Artist Expert",
    "Beauty Specialist",
    "Professional Makeup Artist",
    "Makeup Technician",
    "Beauty Master"
] 

    makeupDescriptions = [
    "I am an expert makeup artist, here to enhance your beauty for any occasion.",
    "As a beauty specialist, I provide professional makeup services tailored to your style.",
    "With my expertise, I ensure you look stunning with flawless makeup applications.",
    "As a dedicated makeup technician, I offer top-quality makeup services to make you feel beautiful.",
    "I am a master in makeup artistry, committed to making you look and feel your best."
] 

    oilChangeHeadings = [
    "Oil Change Expert",
    "Lubrication Specialist",
    "Oil Change Professional",
    "Oil Change Technician",
    "Oil Change Master"
] 

    oilChangeDescriptions = [
    "I am an expert in oil changes, ensuring your engine runs smoothly and efficiently.",
    "As a lubrication specialist, I offer quick and reliable oil change services.",
    "With my professional oil change services, I keep your vehicle in top condition.",
    "As a dedicated oil change technician, I provide top-quality maintenance for your engine.",
    "I am a master in oil changes, committed to delivering the best service for your vehicle."
] 

    personalTrainingHeadings = [
    "Personal Trainer Expert",
    "Fitness Specialist",
    "Professional Personal Trainer",
    "Fitness Technician",
    "Personal Training Master"
] 

    personalTrainingDescriptions = [
    "I am an expert personal trainer, dedicated to helping you achieve your fitness goals.",
    "As a fitness specialist, I provide personalized training programs tailored to your needs.",
    "With my professional guidance, I ensure you stay motivated and reach your fitness milestones.",
    "As a fitness technician, I offer effective and safe workouts designed for optimal results.",
    "I am a master in personal training, committed to helping you achieve optimal health and wellness."
] 

    electricianHeadings = [
    "Electrician Expert",
    "Electrical Specialist",
    "Professional Electrician",
    "Electrical Technician",
    "Electrical Master"
] 

    electricianDescriptions = [
    "I am an expert electrician, ensuring your electrical systems are safe and efficient.",
    "As an electrical specialist, I provide comprehensive services for your home or business.",
    "With my professional electrical services, I guarantee reliable installations and repairs.",
    "As a dedicated electrical technician, I ensure your systems are up to code and functioning properly.",
    "I am a master electrician, committed to delivering top-notch electrical solutions for your needs."
] 

    plumbingHeadings = [
    "Plumber Expert",
    "Plumbing Specialist",
    "Professional Plumber",
    "Plumbing Technician",
    "Plumbing Master"
] 

    plumbingDescriptions = [
    "I am an expert plumber, here to solve all your plumbing issues efficiently.",
    "As a plumbing specialist, I provide reliable and comprehensive plumbing services.",
    "With my professional plumbing services, I ensure high-quality repairs and installations.",
    "As a dedicated plumbing technician, I keep your plumbing systems functioning smoothly.",
    "I am a master plumber, committed to delivering top-quality plumbing solutions for your needs."
] 

    tutorHeadings = [
    "Tutor Expert",
    "Education Specialist",
    "Professional Tutor",
    "Learning Technician",
    "Tutoring Master"
] 

    tutorDescriptions = [
    "I am an expert tutor, dedicated to enhancing your learning experience.",
    "As an education specialist, I provide personalized tutoring plans tailored to your needs.",
    "With my professional tutoring services, I ensure effective and reliable learning sessions.",
    "As a learning technician, I help you achieve your academic goals with customized lessons.",
    "I am a master tutor, committed to helping you succeed in your studies with top-quality tutoring."
] 

    
    rating = ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐" ,"⭐"]
    
    async for i in response:
        i["_id"] = str(i["_id"])
        if 'password' in i:
            del i['password']
        if 'email' in i:
            del i['email']
        if 'confirmPassword' in i:
            del i['confirmPassword'] 
        if '_id' in i:
            del i['_id']
        
        if service_type == "mechanic" :     
            i['mechanicDescriptions'] = random.choice(mechanicDescriptions)
            i['rating'] = random.choice(rating)
            i['mechanicHeadings'] = random.choice(mechanicHeadings)
            data.append(i)
        elif service_type == "carwash" :     
            i['carWashDescriptions'] = random.choice(carWashDescriptions)
            i['rating'] = random.choice(rating)
            i['carWashHeadings'] = random.choice(carWashHeadings)
            data.append(i)    
        elif service_type == "makeup" :     
            i['makeupDescriptions'] = random.choice(makeupDescriptions)
            i['rating'] = random.choice(rating)
            i['makeupHeadings'] = random.choice(makeupHeadings)
            data.append(i)
        elif service_type == "lawncare" :     
            i['lawnCareDescriptions'] = random.choice(lawnCareDescriptions)
            i['rating'] = random.choice(rating)
            i['lawnCareHeadings'] = random.choice(lawnCareHeadings)
            data.append(i)        
        elif service_type == "oilchange" :     
            i['oilChangeDescriptions'] = random.choice(oilChangeDescriptions)
            i['rating'] = random.choice(rating)
            i['oilChangeHeadings'] = random.choice(oilChangeHeadings)
            data.append(i)    
        elif service_type == "trainer" :     
            i['personalTrainingDescriptions'] = random.choice(personalTrainingDescriptions)
            i['rating'] = random.choice(rating)
            i['personalTrainingHeadings'] = random.choice(personalTrainingHeadings)
            data.append(i)
        elif service_type == "plumbing" :     
            i['plumbingDescriptions'] = random.choice(plumbingDescriptions)
            i['rating'] = random.choice(rating)
            i['plumbingHeadings'] = random.choice(plumbingHeadings)
            data.append(i)    
        elif service_type == "electrician" :     
            i['electricianDescriptions'] = random.choice(electricianDescriptions)
            i['rating'] = random.choice(rating)
            i['electricianHeadings'] = random.choice(electricianHeadings)
            data.append(i)    
        elif service_type == "tutor" :     
            i['tutorDescriptions'] = random.choice(tutorDescriptions)
            i['rating'] = random.choice(rating)
            i['tutorHeadings'] = random.choice(tutorHeadings)
            data.append(i)    
    print(data)  # Log the fetched data
    return data
