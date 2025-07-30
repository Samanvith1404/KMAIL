from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
# DB team to dumb the json in the same vairable and update the json to atleast 15 members
bd_data = {
    "24BD1A054B": {
        "Password": "ram118",
        "frpw": {
            "Ans": "Hare krishna",
            "phoneno": 6281198159
        },
        "inbox": {
            "XYZ@gmail.com": "mail content",
            "ABC@gmail.com": "mail content",
            "ijk@gmail.in": "mail content"
        },
        "sent": {
            "sam@gmail.com": "mail content",
            "shiva@gmail.com": "mail content",
            "rohan@gmail.com": "mail content"
        }
    },
    "24BD1A0555": {
        "Password": "nrkr2504",
        "frpw": {
            "Ans": "Rohan kumar reddy",
            "phoneno": 9381418665
        },
        "inbox": {
            "XYZ@gmail.com": "mail content",
            "ABC@gmail.com": "mail content",
            "ijk@gmail.in": "mail content"
        },
        "sent": {
            "sam@gmail.com": "mail content",
            "shiva@gmail.com": "mail content",
            "ram@gmail.com": "mail content"
        }
    }
}

class otp(BaseModel):
    otp: str

class Username(BaseModel):
    username: str

class Password(BaseModel):
    password: str
    username: str

class OtpType(BaseModel):
    otptype: str

class data(BaseModel):
    sender: str
    content: str
    date: str
    starred: False
    subject: str
    
user_name=""

#sign_in content

@app.get("/", response_class=HTMLResponse)
async def serve_login():
    with open("USERNAME.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.post("/")
async def login(data: Username):
    user_name = data.username.strip()
    if user_name in bd_data:
        return JSONResponse({
            "message": "Username correct.",
            "redirect": f"/Password?username={user_name}"
        })
    else:
        return JSONResponse({
            "message": "Invalid username. Please try again."
        }, status_code=400)


@app.get("/Password", response_class=HTMLResponse)
async def serve_password_page(username: str):
    with open("Password.html") as f:
        html_content = f.read().replace("{{username}}", username)
        return HTMLResponse(content=html_content, status_code=200)

@app.post("/Password")
async def check_password(data: Password):
    username = data.username.strip()
    password = data.password.strip()

    if username not in bd_data:
        return JSONResponse({"message": "Invalid username."}, status_code=400)

    if password == bd_data[username]["Password"]:
        return JSONResponse({
            "message": "Password correct.",
            "redirect": f"/inbox?username={username}"
        })
    else:
        return JSONResponse({
            "message": "Invalid password. Please try again."
        
        }, status_code=400)

#sign_in content ends





#Forgot password content starts from here
@app.get("/forgotpassword",response_class=HTMLResponse)
async def forgot_password():
    with open("forgot_password.html") as f:
        return HTMLResponse(content=f.read(),status_code=200)

@app.get("/whatsapp",response_class=HTMLResponse)
async def forgot_pass_whatsapp():
    with open("forgot_password_whatsapp.html") as f:
        return HTMLResponse(content=f.read(),status_code=200)
    
@app.get("/email",response_class=HTMLResponse)
async def forgot_pass_email():
    with open("forgot_password_email.html") as f:
        return HTMLResponse(content=f.read(),status_code=200)

@app.post("/whatsapp")
async def whatsapp_otp(data: OtpType, username: str):
    if data.otptype == "whatsapp":
        otp = "123456"  # Generate actual OTP here
        return {"otp": otp, "phone": bd_data[username]["frpw"]["phoneno"]}
    else:
        return JSONResponse({"message": "Invalid OTP type"}, status_code=400)


@app.post("/email")
async def email_otp(data: OtpType, username: str):
    if data.otptype == "email":
        otp = "123456"  # Generate actual OTP here
        # Note: email field doesn't exist in database, you may need to add it
        return {"otp": otp, "message": "OTP sent to registered email"}
    else:
        return JSONResponse({"message": "Invalid OTP type"}, status_code=400)

@app.get("/verify_otp",response_class=HTMLResponse)
async def verify_otp():
    with open("verify_otp.html") as f:
        return HTMLResponse(content=f.read(),status_code=200)

@app.get("/updatephone",response_class=HTMLResponse)
async def update_phone():
    #code for updating the phone number
    return JSONResponse({"message": "Phone update page"})

@app.get("/updatemail",response_class=HTMLResponse)
async def update_mail():
    #code for updating the mail
    return JSONResponse({"message": "Email update page"})


@app.post("/verify_otp")
async def verify_otp_post(data: otp):
    #code for checking and returning a dict if true like {"otp":"True"}
    return JSONResponse({"otp": "True", "message": "OTP verified successfully"})
#Forgot password ends here










#Mail data starts from here
@app.get("/inbox",response_class=HTMLResponse)
async def inbox(username: str):
    with open('index.html') as f:
        return HTMLResponse(content=f.read,status_code=404)

@app.post("/compose")
async def sending_mails(data):
    #data is given in the form of a list
    #add in backend data for sender as well as receiver
    # sending mails code here
    bd_data[user_name]["mails"]["inbox"][mail.sender]={
        "subject":data.subject,
        "date": data.date,
        "content":data.content,
        "starred": data.starred
    }
    bd[mail.sender]["mails"]["sent"][user_name]={
        "subject":data.subject,
        "date": data.date,
        "content":data.content,
        "starred": data.starred
    }
    return JSONResponce({"satus":"updated Succesfully","status_code":"400"})


@app.get("/sent",response_class=HTMLResponse)
async def sent():
    # taking all sent content and returning the DS containg the data
    #inbox code here
    return

@app.get("/trash",response_class=HTMLResponse)
async def trash():
    # taking all trash content and returning the DS containg the data
    #trash code here
    return

@app.get("/allmails",response_class=HTMLResponse)
async def all_mails():
    # taking all mail (sent,inbox) content and returning the DS containg the data
    return JSONResponse({"message": "All mails functionality"})

#mail data ends here
