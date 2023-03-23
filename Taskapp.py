from fastapi import FastAPI,Request,Response,status,HTTPException
from typing import Union
from fastapi.responses import JSONResponse
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.middleware.cors import CORSMiddleware
import time


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

while True:
    try:
       conn= psycopg2.connect(host ='localhost' ,database="fast api demo", user="postgres",
                           password="123321wwe" ,cursor_factory=RealDictCursor)
       cursor=conn.cursor()
       print("DATABASE CONNECTION WAS SUCCESSFULL")
       break
    except Exception as error:
     print("The connection has failed")  
     print("error",error)  
     time.sleep(2)

class posttask(BaseModel) :
    TaskName : str
    done : bool = False
    
#  Get All tasks----------------------------------------------------------------------------------------------#
@app.get("/tasks")
def get_all_tasks():
     header = {"Access-Control-Allow-Origin": "*",
              "Access-Control-Allow-Methods": "GET,PUT,POST,DELETE,PATCH,OPTIONS"
              }
     cursor.execute("SELECT * FROM tasks")
     task = cursor.fetchall()
     if not task :
         print("error :" , error) 
     else :
         print(task)
     
     data = {"data":task}
     
     return(data)
 
#  Get all task--------------------------------------------------------------------------------------------------#
 
 # Post Task name -----------------------------------------------------------------------------------------------#
 
@app.post("/posttaskname" ,status_code=status.HTTP_201_CREATED)
def post_task(post:posttask):
    header = {"Access-Control-Allow-Origin": "*",
              "Access-Control-Allow-Methods": "GET,PUT,POST,DELETE,PATCH,OPTIONS"
              }
    cursor.execute("INSERT INTO tasks (task_name ) VALUES(%s) RETURNING * " , (str(post.TaskName ),) )
    task = cursor.fetchone()
    conn.commit()
    return("data:",task)

 # Post Task name -------------------------------------------------------   ----------------------------------------#

#Put task DONE --------------------------------------------------------------------------------------------------#
@app.put("/taskdone/{id}" ,status_code=status.HTTP_201_CREATED)
def post_task_done(id:int):
    header = {"Access-Control-Allow-Origin": "*",
              "Access-Control-Allow-Methods": "GET,PUT,POST,DELETE,PATCH,OPTIONS"
              }
    
    cursor.execute("UPDATE tasks SET done = true WHERE id = %s RETURNING * ", ( str(id),))

    task = cursor.fetchone()
    conn.commit()
    return("data:",task)

#Put task DONE --------------------------------------------------------------------------------------------------#


# PUT Update task name-------------------------------------------------------------------------------------------#

@app.put("/edittask/{id}" , status_code=status.HTTP_201_CREATED)
def updatePostByid(id:int , task:posttask):
    # index = find_and_delete(id)
    cursor.execute("UPDATE tasks SET task_name = %s  WHERE id = %s RETURNING * ", (task.TaskName , str(id),))
    index=cursor.fetchone()
   
   
    if not index:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f"The {id} was not found")
    
   
    # updated_post = posts.dict()
    # updated_post['id'] = id
    # my_posts[index] = updated_post 
    data = {"data" : index}
    print (data)
    conn.commit()

    return ("data :" , "Task edited succesfully")

# PUT Update task name-------------------------------------------------------------------------------------------#

# Delete Task ---------------------------------------------------------------------------------------------------#

@app.delete("/deletetaskbyid/{id}" , status_code=status.HTTP_200_OK)
def deletePostbyid(id:int ):
   cursor.execute("DELETE FROM tasks WHERE id = %s RETURNING *" , (str(id),))
   index= cursor.fetchone()
   conn.commit()
#    index = find_and_delete(id)
   
   if not index :
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f"The {id} was not found")
  
   
   data={"data":"The Task was succesfully deleted"}
   print(data)
   return (data)


# Delete Task ---------------------------------------------------------------------------------------------------#

