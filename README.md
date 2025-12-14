# 🧑‍🏫 SQL Teacher — Multi-Agent Learning System (Google ADK Project)

## 📘 Overview
**SQL Teacher** is a multi-agent application built with **Google Agent Development Kit (ADK)** that helps users **learn, practice, and understand SQL interactively**.  
Through natural conversation, users can:
- Design and create database schemas
- Execute CRUD operations in a live in-memory database
- Understand SQL queries step-by-step
- Generate quizzes to test their SQL knowledge

Each specialized agent handles a different part of the SQL learning journey, coordinated by a main **TeacherAgent**.

---

## 🧩 Project Structure

```
frontend/
├── helpers/
│ ├── init.py
│ ├── get_conversation.py
│ └── terms.py
├── services/
│ ├── init.py
│ └── adk_service.py
└── ui/
│ ├── components/
│ │  ├── init.py
│ │  ├── base.py
│ │  ├── components.py
│ │  └── layout.py
├── init.py
└── main.py

backend/
├── teacher_agent/
│ ├── init.py
│ ├── agent.py
│ └── sub_agents/
│ │ ├── memory_agent/
│ │ │ ├── init.py
│ │ │ ├── agent.py
│ │ │ └── prompt.py
│ │ ├── query_explainer_agent/
│ │ │ ├── init.py
│ │ │ ├── agent.py
│ │ │ └── prompt.py
│ │ ├── quiz_agent/
│ │ │ ├── init.py
│ │ │ ├── agent.py
│ │ │ └── prompt.py
│ │ ├── schema_designer_agent/
│ │── init.py
│ ├── agent.py
│ └── prompt.py
├── tools/
│ ├── init.py
│ ├── db_connector.py
│ └── sql_parser.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```


---

## 🧠 Agents and Their Responsibilities

### **1️⃣ TeacherAgent (Main Orchestrator)**
Acts as the **central brain** of the system.  
It receives user input and delegates tasks to the appropriate sub-agents.  
Responsibilities:
- Interprets user intent  
- Routes queries to the correct agent  
- Maintains conversational flow and context  
- Combines sub-agent outputs into coherent responses  

---

### **2️⃣ SchemaDesignerAgent**
Responsible for creating and modifying the database schema.  
Users can describe tables and relationships in natural language, and this agent generates the corresponding `CREATE TABLE` statements.  
Outputs are executed by the `MemoryAgent`.

**Example:**
> User: “Create a database with students and courses.”  
> → Generates:
> ```sql
> CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT);
> CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT);
> ```

---

### **3️⃣ MemoryAgent**
Executes **all SQL commands** within an **in-memory SQLite database**.  
This is the system’s execution layer — it performs all CRUD operations and returns structured results.

Responsibilities:
- Run schema creation, insert, update, delete, and select commands  
- Maintain the in-memory database during a session  
- Return query results or error details in structured JSON format  

**Tool Used:**  
`db_interactions(sql_command: str)` — executes SQL statements using `sqlite3.connect(":memory:")`.

---

### **4️⃣ QueryExplainerAgent**
Explains **how and why** a specific SQL query works.  
It provides step-by-step explanations for each clause (`SELECT`, `FROM`, `WHERE`, `JOIN`, etc.), helping the learner understand query logic and execution order.

**Example:**
> User: “Explain what this query does:  
> ```sql
> SELECT name FROM students WHERE age > 20;
> ```  
> → Agent response:  
> “This query retrieves the names of students older than 20 from the ‘students’ table.”

---

### **5️⃣ QuizAgent**
Generates interactive **SQL quizzes (quizzes)** to test user understanding.  
It creates randomized or adaptive multiple-choice questions based on previous topics discussed with the user.

Responsibilities:
- Generate beginner-to-advanced SQL quizzes  
- Evaluate user answers and provide feedback  
- Adapt difficulty based on performance  
- Cover topics such as schema design, SELECT queries, JOINs, and data manipulation  

**Example Interaction:**
> QuizAgent: “What does the following query return?  
> ```sql
> SELECT COUNT(*) FROM employees WHERE department = 'HR';
> ```  
> A) Lists all HR employees  
> B) Returns the total number of HR employees ✅  
> C) Updates HR department records  
> D) Deletes HR employees”

---

## 🧰 Tools

### `db_connector.py`
Handles database connection logic (using SQLite in-memory DB).

---

## 🚀 How It Works
1. The **user** interacts with the `TeacherAgent`.  
2. The `TeacherAgent` identifies intent and routes the request:
   - Schema creation → `SchemaDesignerAgent`
   - SQL execution → `MemoryAgent`
   - Query explanation → `QueryExplainerAgent`
   - Quiz generation → `QuizAgent`
3. Results are processed, formatted, and returned to the user conversationally.

---

## 🧑‍💻 Run the Project

### **1️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```
2️⃣ Set up environment

Create a .env file in the root directory with this data:
```.env
GOOGLE_GENAI_USE_VERTEXAI=False
GOOGLE_API_KEY=your google API Key
```
3️⃣ Run the application
1. First method - using the built in ADK command
   * Go to your project root directory
   * Open a terminal and type the following command
    ```bash
    adk web
    ```
2. Second method - using the **FastAPI** app object
* Open a terminal
* Run:
  *    ```python main.py``` on Windows 
  * ```python3 main.py``` on MAC or Linux systems

    This will open the backend. After opening the backend
    go to frontend and run:
     *  ```streamlit run main.py```

3. Third method - using the **Docker Compose**
* Open a terminal
* Run:
  * ```docker compose up --build``` to build and start the application (both backend and frontend) 
  * ```docker compose up ``` onloy to start the application (both backend and frontend). This will be usefull when we will do the remote deploy.
* Open the service in browse:
  * [SQL Teacher Streamlit Frontend](http://localhost:8501/)
* Additional Commands:
  * Ctrl + C to stop the application
  * Start in detached mode: ```docker compose up -d```
  * Stop the application: ```docker compose down```


## Build and Deploy (CI/CD)

### Fork this repo on your github space

### Prepare your secrets/credentials

#### Google API KEY
Login to Google CLoud and generate a GOOGLE_API_KEY. 

#### SSH Key Pair
Generate on your machine an ssh key-pair using the command:
```ssh-keygen```
Keep the default options.

### Configure the Secrets in the Github Actions

   * Go to the github fork created and click: 
    ```Settings > Secrets and variables > Actions```

   * Click on the New repository secret to add a new secret. For deploy you will need to add the next secrets:
       * ANSIBLE_SSH_PRIVATE_KEY = set here the content of you PRIVATE key ```cat ~/.ssh/id_rsa```
       * GOOGLE_GENAI_USE_VERTEXAI=False
       * GOOGLE_GENAI_USE_VERTEXAI= The value from Google Cloud 

   * OPTIONAL: If you plan to build and push new version of the application from Github Actions you will need to set:
       * DOCKERHUB_USERNAME
       * DOCKERHUB_TOKEN
       You can get this values from Docker Hub.


### Prepare a VM

#### AWS

##### Import the SSH Key
  ```EC2 > Key Pairs > Actions > Import Key Pair```
  Add a name for your key pair
  cat the public key from your local machine (generated previously and paste it in the text area)
  ```cat ~/.ssh/id_rsa.pub```

##### Create an EC2 Instance
   ```EC2  > Instances > Launch instances```
   * Select OS Ubuntu.
   * Select the key pair previously created.
   * Check the Allow HTTPS and Allow HTTP traffic
   * Set a disk of at least 20 GB
   * Click Launch instance
   * Click on the instance to see the details. The IP is important for us.
   * Verify thet you can ```ssh ubuntu@IP_VM``` from your local machine
   * Update the machines IPs in the `ansible/inventory.ini`:
```
[stage]
aws-1 ansible_host=<PUT_HERE_THE_IP> ansible_user=ubuntu 
```
   * Commit
   * Run the `Install Sql Teacher` github action from Actions annd select the right environment (stage in our case)  

#### NON-AWS
If you created a VM on a different provider be sure that you follow this extra steps before running the Github Actions

##### Setup ansible user
```
wget https://raw.githubusercontent.com/mariusciurea/sql_teacher/refs/heads/master/ansible/setup-ansible-user.sh

chmod +x setup-ansible-user.sh

./setup-ansible-user.sh 'PUBLIC KEY HERE'
```
Check that from your local machine you can:
```
ssh ansible@<IP_VM>
sudo ls
```
The sudo must work without password.

##### Hardening SSH

In `/etc/ssh/sshd_config`
Set:

```
Port 9456 #Set here any port you want but be sure to update also the inventory.ini file
PermitRootLogin no
PasswordAuthentication no
```
And reboot the machine.
You should test that you cannot login via root or username and password.
```ssh -p 9456 ansible@VM_IP``` 



###  Debug

#### Run ansible from local
* Update the machines IPs in the `ansible/inventory.ini` 
* Install Docker ```ansible-playbook -i ansible/inventory.ini ansible/playbooks/install_docker.yaml``` 
* Deploy Sql Teacher
    * ```source .env```
    * ```ansible-playbook -i ansible/inventory.ini ansible/playbooks/deploy_agents.yaml -e "GOOGLE_GENAI_USE_VERTEXAI=$GOOGLE_GENAI_USE_VERTEXAI GOOGLE_API_KEY=$GOOGLE_API_KEY"```
* Open the service in browse:
  * [SQL Teacher Streamlit Frontend](https://itschool.org.ro/)
* Stop Sql Teacher
    * ```ansible-playbook -i ansible/inventory.ini ansible/playbooks/stop_agents.yaml```

#### Docker logs

* Docker see all containers
```sudo docker ps```

* Docker check logs
```
sudo docker logs -f sql-teacher-nginx
sudo docker logs -f sql-teacher-frontend
sudo docker logs -f sql-teacher-backend
```

* Check application logs from disk
```
tail -f sql-teacher/logs/backend/*.log
tail -f sql-teacher/logs/frontend/*.log
```

* Purge the database
```
rm /tmp/storage/session.db
```
restart the application
```
cd sql-teacher
sudo docker compose down
sudo docker compose up -d --pull always
```
