from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import pywhatkit as kit
import datetime
import time
import pyautogui as pi


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
  "24BD1A054B":{
    "Password":"ram118",
    "frpw":{
      "Ans":"Hare krishna",
      "phoneno":6281198159,
      "user_email":"ramakrishna118g@gmail.com"
    },
   "Emails": {
    "inbox": {
      "XYZ@gmail.com": {
        "subject":"",
        "date":"",
        "content":"",
        "imp":False,
      },
      "ABC@gmail.com": {
        "subject":"",
        "date":"",
        "content":"",
        "imp":False,
      },
      "ijk@gmail.in": {
        "subject":"",
        "date":"",
        "content":"",
        "imp":False,
      }
    },
    "sent": {
      "sam@gmail.com": {
        "subject":"",
        "date":"",
        "content":"",
        "imp":False,
      },
      "shiva@gmail.com": {
        "subject":"",
        "date":"",
        "content":"",
        "imp":False,
      },
      "rohan@gmail.com": {
        "subject":"",
        "date":"",
        "content":"",
        "imp":False,
      }
    }
  }
  },
  "24BD1A0555": {
    "Password":"nrkr2504",
    "frpw":{
      "Ans": "Rohan kumar reddy",
      "phoneno": 9381418665
    },
    "inbox": {
            "XYZ@gmail.com": {
        "subject":"",
        "date":"",
        "content":"",
        "imp":False,
      },
      "ABC@gmail.com": {
        "subject":"",
        "date":"",
        "content":"",
        "imp":False,
      },
      "ijk@gmail.in": {
        "subject":"",
        "date":"",
        "content":"",
        "imp":False,
      }
    },
    "sent": {
      "sam@gmail.com": {
        "subject":"",
        "date":"",
        "content":"",
        "imp":False,
      },
      "shiva@gmail.com": {
        "subject":"",
        "date":"",
        "content":"",
        "imp":False,
      },
      "rohan@gmail.com": {
        "subject":"",
        "date":"",
        "content":"",
        "imp":False,
      }
    }
  }
}


class Otp(BaseModel):
    otp: str

class MailAction(BaseModel):
    username: str
    folder: str  # "inbox", "sent", or "trash"
    mail_id: str

class Password(BaseModel):
    password: str
    username: str

class OtpType(BaseModel):
    otptype: str
    username: str

class data(BaseModel):
    sender: str
    content: str
    date: str
    starred: bool=False
    subject: str
    
user_name=""

#sign_in content

@app.get("/" , response_class=HTMLResponse)
async def serve_login():
    with open("USERNAME.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.post("/")
async def check_password(data: Password):
    username = data.username.strip()
    password = data.password.strip()

    if username in bd_data:
        if password == bd_data[username]["Password"]:
            return JSONResponse({
            "message": "Password correct.",
            "redirect": f"/Home",
        })
        else:
            return JSONResponse({
                "message":"Invalid password."
            })
    else:
        return JSONResponse({
            "message": "Invalid username. Please try again."
        
        }, status_code=400)

#sign_in content ends





#Forgot password content starts from here
@app.get("/forgotpassword",response_class=HTMLResponse)
async def forgot_password():
    with open("forgotpass.html") as f:
        return HTMLResponse(content=f.read(),status_code=200)
    
otp=""
@app.post("/forgotpassword")
async def func(data: OtpType):
    if(data.username not in bd_data.keys()):
        return JSONResponse({"msg":"Username Not Found","status_code":202})
    if(data.otptype=="whatsapp"):
        phone=bd_data[data.username]["frpw"]["phoneno"]
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        msg_otp = f"Your OTP for login is: {otp}"

        # Phone number (in E.164 format)
        ph = f"+91{str(phone)}"  # replace with actual number

        # Calculate safe send time
        now = datetime.datetime.now()
        send_time = now + datetime.timedelta(minutes=1)
        hour = send_time.hour
        minute = send_time.minute

        # Schedule message
        kit.sendwhatmsg(ph, msg_otp, hour, minute, wait_time=8, tab_close=True)
        time.sleep(10)
        return JSONResponse({"msg":"Success","status_code":300})
    if(data.otptype=="email"):
        email=bd_data[data.username]["frpw"]["user_email"]


@app.get("/verify_otp",response_class=HTMLResponse)
async def verify_otp():
    with open("OTP.html") as f:
        return HTMLResponse(content=f.read(),status_code=200)

@app.post("/verify_otp")
async def verify_otp_post(data: Otp):
    #code for checking and returning a dict if true like {"otp":"True"}
    if(Otp.otp == otp):
        return JSONResponse({"otp": "True", "message": "OTP verified successfully"})
    else:
        return JSONResponse({"otp": "False", "message": "OTP not verified successfully"})
#Forgot password ends here








#Mail data starts from here
@app.get("/Home",response_class=HTMLResponse)
async def inbox():
    with open('Home.html') as f:
        return HTMLResponse(content=f.read(),status_code=404)

@app.get("/compose",response_class=HTMLResponse)
async def inbox():
    with open('Home.html') as f:
        return HTMLResponse(content=f.read(),status_code=404)
    
@app.get("/sent",response_class=HTMLResponse)
async def inbox():
    with open('Home.html') as f:
        return HTMLResponse(content=f.read(),status_code=404)

@app.get("/inbox",response_class=HTMLResponse)
async def inbox():
    with open('Home.html') as f:
        return HTMLResponse(content=f.read(),status_code=404)

@app.get("/allmails",response_class=HTMLResponse)
async def inbox():
    with open('Home.html') as f:
        return HTMLResponse(content=f.read(),status_code=404)
    
@app.post("/compose")
async def sending_mails(mail: data):
    #data is given in the form of a list
    #add in backend data for sender as well as receiver
    # sending mails code here
    bd_data[user_name]["mails"]["inbox"][mail.sender]={
        "subject":data.subject,
        "date": data.date,
        "content":data.content,
        "starred": data.starred
    }
    bd_data[mail.sender]["mails"]["sent"][user_name]={
        "subject":data.subject,
        "date": data.date,
        "content":data.content,
        "starred": data.starred
    }
    return JSONResponse({"satus":"updated Succesfully","status_code":"400"})


@app.get("/sent")
async def sent(username: str):
    # taking all sent content and returning the DS containing the data
    if username not in bd_data:
        return JSONResponse({"message": "Invalid username."}, status_code=400)
    
    sent_mails = bd_data[username]["mails"]["sent"]
    
    # Format the sent mails data for better readability
    formatted_sent_mails = []
    for recipient, mail_content in sent_mails.items():
        if isinstance(mail_content, dict):
            # If mail_content is a dictionary (new format with subject, date, etc.)
            formatted_sent_mails.append({
                "recipient": recipient,
                "subject": mail_content.get("subject", "No Subject"),
                "content": mail_content.get("content", mail_content),
                "date": mail_content.get("date", "No Date"),
                "starred": mail_content.get("starred", False)
            })
        else:
            # If mail_content is just a string (old format)
            formatted_sent_mails.append({
                "recipient": recipient,
                "subject": "No Subject",
                "content": mail_content,
                "date": "No Date",
                "starred": False
            })
    
    return JSONResponse({
        "username": username,
        "sent_mails": formatted_sent_mails,
        "total_sent": len(formatted_sent_mails)})

@app.post("/movetotrash", status_code=200)
async def move_to_trash(data: MailAction):
    """
    Moves a specified email from a user's inbox or sent folder to their trash.
    """
    username = data.username
    folder = data.folder
    mail_id = data.mail_id

    if username not in bd_data:
        return JSONResponse(content={"message": "User not found"}, status_code=404)
        
    if folder not in ["inbox", "sent"]:
        return JSONResponse(content={"message": "Invalid source folder specified. Use 'inbox' or 'sent'."}, status_code=400)
        
    if mail_id not in bd_data[username]["mails"][folder]:
        return JSONResponse(content={"message": "Mail not found in the specified folder"}, status_code=404)

    # Remove the mail from the source folder and add it to trash
    mail_to_move = bd_data[username]["mails"][folder].pop(mail_id)
    bd_data[username]["mails"]["trash"][mail_id] = mail_to_move
    
    return JSONResponse(content={"message": f"Mail '{mail_id}' moved to trash successfully."})


@app.get("/trash", response_class=JSONResponse)
async def trash(username: str): 
    """
    Retrieves and returns all emails in the specified user's trash folder.
    """
    if username not in bd_data:
        return JSONResponse(content={"message": f"User '{username}' not found."}, status_code=404)
    
    # Safely get the trash content, returning an empty dict if it doesn't exist
    trash_content = bd_data[username]["mails"].get("trash", {})
    
    return JSONResponse(content=trash_content, status_code=200)


@app.get("/allmails",response_class=HTMLResponse)
async def all_mails():
    # taking all mail (sent,inbox) content and returning the DS containg the data
    return JSONResponse({"message": "All mails functionality"})
#mail data ends here
